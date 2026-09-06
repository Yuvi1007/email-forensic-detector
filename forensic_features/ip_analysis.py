import re
import ipaddress
import requests


_IPV4_RE = re.compile(r"(?:(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)\.){3}(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)")
# Loose IPv6 matcher; we validate candidates via ipaddress.ip_address
_IPV6_RE = re.compile(r"(?i)\b(?:[0-9a-f]{0,4}:){2,7}[0-9a-f]{0,4}\b")


def _extract_ip_candidates(text):
    if not text:
        return []

    candidates = set()
    for match in _IPV4_RE.findall(text):
        candidates.add(match)

    for match in _IPV6_RE.findall(text):
        # Skip common false-positives like time stamps "12:34:56"
        if match.count(":") >= 2:
            candidates.add(match)

    # Validate + normalize
    valid = []
    for c in candidates:
        try:
            valid.append(str(ipaddress.ip_address(c)))
        except Exception:
            pass
    return valid


def _choose_best_ip(ips):
    """
    Prefer globally routable IPs; otherwise return the first valid IP.
    """
    for ip_str in ips:
        try:
            ip_obj = ipaddress.ip_address(ip_str)
            if ip_obj.is_global:
                return ip_str
        except Exception:
            continue

    return ips[0] if ips else None


def extract_origin_ip(header_data):
    """
    Extract the originating IP from the Received headers.
    Usually the earliest server in the chain contains the sender IP.
    """

    # Common explicit headers
    for key in ("x_originating_ip", "x_forwarded_for"):
        raw_val = header_data.get(key) or ""
        ips = _extract_ip_candidates(raw_val)
        best = _choose_best_ip(ips)
        if best:
            return best

    # Prefer scanning the raw Received headers (more reliable than parsed dicts)
    received_raw = header_data.get("received_raw") or []
    if isinstance(received_raw, str):
        received_raw = [received_raw]

    # The earliest hop is usually last in the list; scan from oldest to newest.
    for hop_raw in reversed(received_raw):
        ips = _extract_ip_candidates(hop_raw)
        best = _choose_best_ip(ips)
        if best:
            return best

    # Fallback to structured received entries if present
    received_headers = header_data.get("received", [])
    for hop in reversed(received_headers):
        hop_str = hop.get("raw") if isinstance(hop, dict) else str(hop)
        ips = _extract_ip_candidates(hop_str)
        best = _choose_best_ip(ips)
        if best:
            return best

    return None


def get_ip_geolocation(ip):
    """
    Get geo-location data of the IP using ipinfo API.
    """

    if ip is None:
        return None

    try:
        ip_obj = ipaddress.ip_address(ip)
        if not ip_obj.is_global:
            # Private/loopback/reserved IPs cannot be meaningfully geo-located.
            return None
    except Exception:
        return None

    try:

        url = f"https://ipinfo.io/{ip}/json"

        response = requests.get(url, timeout=8)

        data = response.json()

        if isinstance(data, dict) and data.get("bogon"):
            return None

        geo_data = {
            "IP": ip,
            "City": data.get("city"),
            "Region": data.get("region"),
            "Country": data.get("country"),
            "Organization": data.get("org"),
            "Location": data.get("loc")
        }

        return geo_data

    except Exception as e:
        print("Error retrieving geo info:", e)

    # Fallback provider (no key): ip-api.com
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,lat,lon,org,query"
        response = requests.get(url, timeout=8)
        data = response.json()
        if not isinstance(data, dict) or data.get("status") != "success":
            return None

        loc = None
        if data.get("lat") is not None and data.get("lon") is not None:
            loc = f"{data.get('lat')},{data.get('lon')}"

        return {
            "IP": data.get("query") or ip,
            "City": data.get("city"),
            "Region": data.get("regionName"),
            "Country": data.get("country"),
            "Organization": data.get("org"),
            "Location": loc,
        }
    except Exception as e:
        print("Error retrieving geo info (fallback):", e)
        return None
