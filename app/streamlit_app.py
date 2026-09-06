import streamlit as st

import ipaddress
from forensic_features.ip_analysis import get_ip_geolocation
from parser.header_parser import parse_email_header
from forensic_features.feature_engineering import engineer_features
from model.predict import predict_email
from report.generate_report import generate_forensic_report
from report.export_pdf import export_report_pdf_bytes


st.title("Email Header Forensic Analyzer")

st.write("Upload an email (.eml) file to analyze it.")

# Note: the bundled dataset files often have *no* extension, so we don't
# restrict file types here. The contents are still parsed as RFC822 text.
uploaded_file = st.file_uploader("Upload Email File")


if uploaded_file is not None:

    raw_bytes = uploaded_file.read()
    email_content = raw_bytes.decode("latin-1", errors="replace")

    with st.expander("Preview (raw email text)", expanded=False):
        st.text_area("Email content", value=email_content, height=250)

    # Parse header
    header = parse_email_header(email_content)

    # Feature extraction
    features = engineer_features(header, email_content)

    # ML prediction
    prediction = predict_email(email_content)

    # Generate report
    report = generate_forensic_report(header, features, prediction)

    st.subheader("Classification Result")

    st.write("Prediction:", report["Classification"]["prediction"])

    st.write("Confidence:", report["Classification"]["confidence"], "%")

    st.subheader("Threat Level")

    st.write(report["Threat Level"])

    st.subheader("Risk Score")

    st.write(report["Risk Score"])

    st.subheader("Origin IP")

    origin_ip = report.get("Origin IP")
    st.write(origin_ip if origin_ip else "Not available (no origin IP found in headers)")

    st.subheader("IP Geolocation")

    geo = report.get("IP Geolocation")
    # If the report skipped geo (private IP / no IP), try a best-effort lookup here.
    if not geo and origin_ip:
        geo = get_ip_geolocation(origin_ip)

    if geo:
        st.json(geo)
    else:
        note = "Not available (no public origin IP to look up)"
        if origin_ip:
            try:
                if not ipaddress.ip_address(origin_ip).is_global:
                    note = "Not available (origin IP is private/reserved)"
            except Exception:
                pass
        st.write(note)

    st.subheader("Header Metadata")

    st.json(report["Header Metadata"])

    st.subheader("Indicators")

    st.json(report["Indicators"])

    st.subheader("Download Report")
    try:
        pdf_bytes = export_report_pdf_bytes(report)
        st.download_button(
            label="Download PDF report",
            data=pdf_bytes,
            file_name="forensic_report.pdf",
            mime="application/pdf",
        )
    except Exception as e:
        st.error(f"Could not generate PDF report: {e}")
        st.caption("If you see a missing dependency error, install it with: `pip install reportlab`")
