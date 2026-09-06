from report.threat_score import calculate_risk_score
from forensic_features.ip_analysis import extract_origin_ip, get_ip_geolocation


def generate_forensic_report(header_data, features, prediction_result):

    risk_score = calculate_risk_score(features)

    if risk_score > 70:
        threat = "High Risk Email"

    elif risk_score > 40:
        threat = "Moderate Risk Email"

    else:
        threat = "Low Risk Email"

    # Extract origin IP
    origin_ip = extract_origin_ip(header_data)

    # Get geo-location
    geo_data = get_ip_geolocation(origin_ip)

    report = {}

    report["Header Metadata"] = {
        "From": header_data["from"],
        "To": header_data["to"],
        "Subject": header_data["subject"],
        "Date": header_data["date"],
        "Message-ID": header_data["message_id"]
    }

    report["Origin IP"] = origin_ip

    report["IP Geolocation"] = geo_data

    report["Indicators"] = features

    report["Classification"] = prediction_result

    report["Risk Score"] = risk_score

    report["Threat Level"] = threat

    return report