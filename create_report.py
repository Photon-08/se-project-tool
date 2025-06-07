import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def save_similarity_report(similarity_dict, output_path):
    """
    Generate a professional PDF report of team similarity analysis.

    Parameters:
    - similarity_dict (dict): {'Team A and Team B': similarity_score (float)}
    - output_path (str): PDF file path to save
    """

    def get_risk_label(score):
        if score < 0.60:
            return "No Risk"
        elif score < 0.70:
            return "Moderate Similarity"
        elif score < 0.80:
            return "Warning"
        else:
            return "Possible Risk"

    # Filter for scores >= 0.60
    df = pd.DataFrame([
        {"Teams": k, "Similarity Score": round(v, 2), "Risk Level": get_risk_label(v)}
        for k, v in similarity_dict.items() if v >= 0.60
    ])

    if df.empty:
        print("No similarity above threshold. No report generated.")
        return

    # Setup PDF
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # === Title Block Styles ===
    title_style = ParagraphStyle(name="Title", fontSize=20, alignment=1, textColor=colors.HexColor("#003366"), spaceAfter=6)
    subtitle_style = ParagraphStyle(name="Subtitle", fontSize=16, alignment=1, textColor=colors.HexColor("#003366"), spaceAfter=6)
    institute_style = ParagraphStyle(name="Institute", fontSize=12, alignment=1, textColor=colors.black, spaceAfter=10)
    footer_style = ParagraphStyle(name="Footer", fontSize=9, alignment=1, textColor=colors.grey, spaceAfter=20)
    section_header_style = ParagraphStyle(name="SectionHeader", fontSize=14, alignment=0, textColor=colors.darkblue, spaceAfter=8)

    # === Title Block ===
    elements.append(Paragraph("Software Engineering Project Similarity Report", title_style))
    elements.append(Paragraph("June 2025", subtitle_style))
    elements.append(Paragraph("IIT Madras - BS Degree", institute_style))
    elements.append(Paragraph("Generated using hybrid similarity engine (semantic + lexical)", footer_style))

    # === Table Section Header ===
    elements.append(Paragraph("Summary of Teams with Moderate to High Similarity", section_header_style))

    # === Table ===
    table_data = [list(df.columns)] + df.values.tolist()
    table = Table(table_data, hAlign="CENTER", colWidths=[220, 100, 100])
    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ])

    for i, row in enumerate(df.itertuples(), start=1):
        risk = row._3
        bg = colors.whitesmoke
        if risk == "Moderate Similarity":
            bg = colors.lightyellow
        elif risk == "Warning":
            bg = colors.lightcoral
        elif risk == "Possible Risk":
            bg = colors.red
        style.add("BACKGROUND", (0, i), (-1, i), bg)

    table.setStyle(style)
    elements.append(table)
    elements.append(Paragraph("Moderate Similarity: Indicates potential conceptual or keyword-level overlap between submissions."))

    elements.append(Paragraph("High Similarity: Significant textual or structural similarity detected — manual review strongly recommended."))




    # === Page 2: Methodology ===
    elements.append(PageBreak())
    elements.append(Paragraph("Methodology Behind Similarity Analysis", title_style))
    elements.append(Spacer(1, 12))

    methodology_text = """
    <b>1. Context-Aware Embedding:</b><br/>
    We used a multilingual transformer model: <i>sentence-transformers/static-similarity-mrl-multilingual-v1</i>.
    This model captures the contextual and semantic meaning of entire sentences, making it suitable for identifying
    conceptual overlap even when phrasing is changed.<br/><br/>

    <b>2. TF-IDF Based Matching:</b><br/>
    This traditional method highlights surface-level similarity such as identical wording or phrase copying. It excels
    at detecting literal reuse of content.<br/><br/>

    <b>3. Future Work:</b><br/>
    We are working to add paraphrasing-aware comparison to detect rewritten but semantically identical content.<br/><br/>

    <b>4. Composite Score:</b><br/>
    A blended score from both methods provides a robust measure — capturing both deep semantic similarity and shallow copying.
    """
    elements.append(Paragraph(methodology_text, styles["Normal"]))

    # === Build PDF ===
    doc.build(elements)
