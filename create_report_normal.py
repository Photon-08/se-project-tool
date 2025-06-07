import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def save_similarity_report(similarity_dict, output_path):
    """
    Generate a PDF similarity report (excluding No Risk) and include a methodology explanation page.

    Parameters:
    - similarity_dict (dict): Keys are 'Team X and Team Y', values are similarity scores (float).
    - output_path (str): Full path (including filename) where the PDF report should be saved.
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

    # Prepare DataFrame with filtered rows
    df = pd.DataFrame([
        {"Teams": k, "Similarity Score": round(v, 2), "Risk Level": get_risk_label(v)}
        for k, v in similarity_dict.items() if v >= 0.60
    ])

    if df.empty:
        print("No teams with similarity score >= 0.60. No report generated.")
        return

    # Setup PDF
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # --- Page 1: Report Table ---
    elements.append(Paragraph("Team Document Similarity Report", styles["Title"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        "This report includes only team pairs with similarity score ≥ 0.60.<br/>"
        "<b>Legend:</b> Moderate (0.60–0.70), Warning (0.70–0.80), Possible Risk (> 0.80).",
        styles["Normal"]
    ))
    elements.append(Spacer(1, 12))

    # Table
    table_data = [list(df.columns)] + df.values.tolist()
    table = Table(table_data, hAlign='LEFT')

    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
    ])

    for i, row in enumerate(df.itertuples(), start=1):
        risk = row._3
        if risk == "Moderate Similarity":
            bg = colors.lightyellow
        elif risk == "Warning":
            bg = colors.lightcoral
        else:
            bg = colors.red
        style.add("BACKGROUND", (0, i), (-1, i), bg)

    table.setStyle(style)
    elements.append(table)

    # --- Page 2: Methodology ---
    elements.append(PageBreak())
    elements.append(Paragraph("Methodology Behind Similarity Analysis", styles["Title"]))
    elements.append(Spacer(1, 12))

    methodology_text = """
    <b>1. Context-Aware Embedding:</b><br/>
    We used a multilingual transformer model: <i>sentence-transformers/static-similarity-mrl-multilingual-v1</i>.
    This model captures the contextual and semantic meaning of entire sentences, rather than relying on exact word matches.
    It is well-suited for comparing free-text reports across different languages and phrasing variations.<br/><br/>

    <b>2. TF-IDF Based Similarity:</b><br/>
    We also used the traditional TF-IDF (Term Frequency-Inverse Document Frequency) method, which is effective at capturing
    exact word-by-word matches. This method highlights potential cases of direct copying or using large chunks of identical phrases.<br/><br/>

    <b>3. Future Enhancements:</b><br/>
    We are actively working on integrating a paraphrasing-aware model, which will improve the detection of rephrased or partially altered content,
    giving better insights into near-duplicate submissions.<br/><br/>

    <b>4. Composite Scoring:</b><br/>
    The final similarity score used in this report is a composite of both the embedding-based and TF-IDF based similarities.
    This hybrid approach ensures we capture both semantic overlap and lexical duplication from multiple perspectives.
    """

    elements.append(Paragraph(methodology_text, styles["Normal"]))
    doc.build(elements)
