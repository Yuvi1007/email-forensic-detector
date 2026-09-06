def calculate_risk_score(features):

    score = 0

    if features["missing_message_id"]:
        score += 15

    if features["suspicious_subject"]:
        score += 20

    if features["domain_mismatch"]:
        score += 20

    if features["spf_fail"]:
        score += 15

    if features["dkim_fail"]:
        score += 10

    if features["dmarc_fail"]:
        score += 10

    if features["ip_url_flag"]:
        score += 10

    if features["shortened_url"]:
        score += 5

    return min(score,100)