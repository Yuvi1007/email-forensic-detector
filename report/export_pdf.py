from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def export_report_pdf(report,filename="forensic_report.pdf"):

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("Email Forensic Report",styles["Title"]))

    story.append(Spacer(1,20))

    for section,data in report.items():

        story.append(Paragraph(f"<b>{section}</b>",styles["Heading2"]))

        story.append(Paragraph(str(data),styles["BodyText"]))

        story.append(Spacer(1,15))

    pdf = SimpleDocTemplate(filename)

    pdf.build(story)


def export_report_pdf_bytes(report):
    """
    Build the forensic report PDF in-memory and return bytes (for Streamlit download).
    """

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("Email Forensic Report", styles["Title"]))

    story.append(Spacer(1, 20))

    for section, data in report.items():
        story.append(Paragraph(f"<b>{section}</b>", styles["Heading2"]))
        story.append(Paragraph(str(data), styles["BodyText"]))
        story.append(Spacer(1, 15))

    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer)
    pdf.build(story)
    return buffer.getvalue()
