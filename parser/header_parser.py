import email
import email.utils


def parse_email_header(email_content):
    try:
        msg = email.message_from_string(email_content)
    except Exception as e:
        print("Failed to parse email:", e)
        return {}

    def get_addresses(field):
        raw = msg.get_all(field, [])
        result = []
        for entry in raw:
            parsed = email.utils.getaddresses([entry])
            result.extend(parsed)
        return result

    received_raw = msg.get_all("received", [])
    received = []
    for r in received_raw:
        hop = {"raw": r}
        r_lower = r.lower()
        if "from " in r_lower:
            try:
                hop["from"] = r.split()[1]
            except Exception:
                hop["from"] = None
        if " by " in r_lower:
            try:
                hop["by"] = r_lower.split(" by ")[1].split()[0]
            except Exception:
                hop["by"] = None
        hop["spf"] = "spf=fail" in r_lower
        hop["dkim"] = "dkim=fail" in r_lower
        hop["dmarc"] = "dmarc=fail" in r_lower
        received.append(hop)

    return {
        "from": get_addresses("from"),
        "to": get_addresses("to"),
        "subject": msg.get("subject", ""),
        "date": msg.get("date", ""),
        "message_id": msg.get("message-id", ""),
        "received": received,
        "received_raw": received_raw,
        "x_originating_ip": msg.get("x-originating-ip", ""),
        "x_forwarded_for": msg.get("x-forwarded-for", ""),
        "reply_to": get_addresses("reply-to"),
        "return_path": msg.get("return-path", ""),
        "x_mailer": msg.get("x-mailer", ""),
        "content_type": msg.get("content-type", ""),
    }
