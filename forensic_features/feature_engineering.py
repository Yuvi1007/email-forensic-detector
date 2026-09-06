from forensic_features.url_features import extract_url_features


def extract_domain(email_list):
    if not email_list:
        return None
    try:
        email_address = email_list[0][0]
        domain = email_address.split("@")[1]
        return domain.lower()
    except:
        return None


def authentication_features(header_data):
    spf_fail = 0
    dkim_fail = 0
    dmarc_fail = 0

    received = header_data.get("received", [])

    for hop in received:
        hop_str = str(hop).lower()
        if "spf=fail" in hop_str:
            spf_fail = 1
        if "dkim=fail" in hop_str:
            dkim_fail = 1
        if "dmarc=fail" in hop_str:
            dmarc_fail = 1

    return {
        "spf_fail": spf_fail,
        "dkim_fail": dkim_fail,
        "dmarc_fail": dmarc_fail
    }


def engineer_features(header_data, email_content=""):

    num_received = len(header_data["received"]) if header_data["received"] else 0

    missing_message_id = 1 if not header_data["message_id"] else 0

    subject = header_data["subject"] if header_data["subject"] else ""
    subject = subject.lower()

    suspicious_words = ["free", "win", "offer", "money", "urgent", "click"]

    suspicious_subject = 1 if any(word in subject for word in suspicious_words) else 0

    sender_domain = extract_domain(header_data["from"])

    received_domains = []
    if header_data["received"]:
        for hop in header_data["received"]:
            if "by" in hop:
                received_domains.append(hop["by"])

    domain_mismatch = 0
    if sender_domain and received_domains:
        if not any(sender_domain in str(d).lower() for d in received_domains):
            domain_mismatch = 1

    empty_subject = 1 if subject.strip() == "" else 0

    features = {
        "num_received": num_received,
        "missing_message_id": missing_message_id,
        "suspicious_subject": suspicious_subject,
        "domain_mismatch": domain_mismatch,
        "empty_subject": empty_subject
    }

    auth = authentication_features(header_data)
    features.update(auth)

    url_features = extract_url_features(email_content)
    features.update(url_features)

    return features