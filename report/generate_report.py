from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

def generate_pdf(patient_id, ipfs_hash, tx_id):

    file = "medical_report.pdf"

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("Medical MRI Report", styles['Title']))
    elements.append(Spacer(1,20))

    elements.append(Paragraph(f"Patient ID : {patient_id}", styles['Normal']))
    elements.append(Paragraph("Tumor Detection : Completed", styles['Normal']))
    elements.append(Paragraph(f"IPFS Hash : {ipfs_hash}", styles['Normal']))
    elements.append(Paragraph(f"Blockchain Transaction : {tx_id}", styles['Normal']))

    date = datetime.now().strftime("%d-%m-%Y")

    elements.append(Paragraph(f"Date : {date}", styles['Normal']))

    pdf = SimpleDocTemplate(file)

    pdf.build(elements)

    return file