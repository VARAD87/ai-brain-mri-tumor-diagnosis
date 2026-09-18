from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Image
from reportlab.lib.enums import TA_CENTER
from datetime import datetime
import os


def generate_medical_report(patient, diagnosis, image_path):
    os.makedirs("reports/final", exist_ok=True)

    file_name = f"{patient['name']}_Brain_MRI_Report.pdf"
    file_path = os.path.join("reports/final", file_name)

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    elements = []

    title = Paragraph(
        "<b>AI-Powered Brain MRI Tumor Diagnostic Report</b>",
        styles["Title"]
    )
    elements.append(title)
    elements.append(Spacer(1, 12))

    subtitle = Paragraph(
        "<i>Generated using Deep Learning (CNN + U-Net + GAN)</i>",
        styles["Normal"]
    )
    elements.append(subtitle)
    elements.append(Spacer(1, 20))

    # -------- PATIENT INFO --------
    elements.append(Paragraph("<b>Patient Information</b>", styles["Heading2"]))
    elements.append(Spacer(1, 8))

    patient_info = f"""
    <b>Name:</b> {patient['name']}<br/>
    <b>Age:</b> {patient['age']}<br/>
    <b>Gender:</b> {patient['gender']}<br/>
    <b>Date:</b> {datetime.now().strftime("%d %B %Y")}
    """
    elements.append(Paragraph(patient_info, styles["Normal"]))
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("<b>Clinical Background</b>", styles["Heading2"]))
    elements.append(Spacer(1, 8))

    intro_text = (
        "Magnetic Resonance Imaging (MRI) is a widely used modality for detecting "
        "brain abnormalities. In this report, an AI-based system was used to "
        "automatically analyze the MRI scan, identify the presence of a brain tumor, "
        "and localize the affected region."
    )
    elements.append(Paragraph(intro_text, styles["Normal"]))
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("<b>Diagnostic Findings</b>", styles["Heading2"]))
    elements.append(Spacer(1, 8))

    findings = f"""
    <b>Tumor Type:</b> {diagnosis['tumor']}<br/>
    <b>Prediction Confidence:</b> {diagnosis['confidence']:.2f}%<br/>
    <b>Analysis Method:</b> CNN-based classification with GAN-augmented training data.
    """
    elements.append(Paragraph(findings, styles["Normal"]))
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("<b>Tumor Segmentation Result</b>", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    if os.path.exists(image_path):
        img = Image(image_path, width=12*cm, height=12*cm)
        img.hAlign = "CENTER"
        elements.append(img)
        elements.append(Spacer(1, 10))
    else:
        elements.append(Paragraph("Segmentation image not available.", styles["Normal"]))

    elements.append(Paragraph("<b>Conclusion</b>", styles["Heading2"]))
    elements.append(Spacer(1, 8))

    conclusion = (
        "The AI-based analysis indicates the presence of a brain tumor with high "
        "confidence. The segmentation output highlights the suspected tumor region "
        "to assist clinical interpretation. This report is intended as a decision-"
        "support tool and should be reviewed by a qualified medical professional."
    )
    elements.append(Paragraph(conclusion, styles["Normal"]))
    elements.append(Spacer(1, 20))

    # -------- FOOTER --------
    footer = Paragraph(
        "<i>This report is computer-generated and does not require a signature.</i>",
        styles["Normal"]
    )
    elements.append(footer)

    doc.build(elements)
    return file_path
