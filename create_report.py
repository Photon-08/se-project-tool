import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO


def save_similarity_report(similarity_dict, output_path):
    """
    Generate a professional PDF report of team similarity analysis.

    Parameters:
    - similarity_dict (dict): {'Team A and Team B': similarity_score (float)}
    - output_path (str): PDF file path to save
    """
    print("#########")
    print(similarity_dict)
    print("#########")

    def get_risk_label(score):
        if score < 0.60:
            return "No Risk"
        elif score < 0.70:
            return "Moderate Similarity"
        elif score < 0.80:
            return "Warning"
        else:
            return "Possible Risk"
    # For top-level similarity
    def get_top_n_teams(n=20):
        """
        Get the top N teams based on similarity scores.
        """
        sorted_final_sim = sorted(similarity_dict.items(), key=lambda item: item[1], reverse=True)

        sorted_dict = {}
        for team_pair, score in sorted_final_sim[:n]:
            sorted_dict[team_pair] = score
        return sorted_dict

    top_n_dict = get_top_n_teams(15)
    # Filter for scores >= 0.60
    df = pd.DataFrame([
        {"Teams": k, "Similarity Score": round(v, 2), }
        for k, v in top_n_dict.items() 
    ])
    print(df)

    

    # Setup PDF
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    #doc = SimpleDocTemplate(buffer, pagesize=A4)
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
    elements.append(Paragraph("Generated using a hybrid similarity engine (semantic + lexical + paraphrasing-aware techniques)", footer_style))

    # === Table Section Header ===
    elements.append(Paragraph("Top 20 Project Submission Pairs with Highest Detected Similarity", section_header_style))

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

    """
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
    """

    for i, row in enumerate(df.itertuples(), start=1):
        
        bg = colors.whitesmoke
        
        bg = colors.red
        style.add("BACKGROUND", (0, i), (-1, i), bg)

    table.setStyle(style)
    elements.append(table)
    #elements.append(Paragraph("Moderate Similarity: Indicates potential conceptual or keyword-level overlap between submissions."))

    #elements.append(Paragraph("High Similarity: Significant textual or structural similarity detected — manual review strongly recommended."))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("The following team submissions require manual evaluation for possible similarity concerns."))



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
    methodology_text = """
    <b>1. Context-Aware Embedding:</b><br/>
    We utilized a multilingual transformer model: <i>sentence-transformers/static-similarity-mrl-multilingual-v1</i>. 
    This model effectively captures the semantic meaning and contextual flow of sentences, making it suitable for detecting conceptual overlap even when wording differs significantly.<br/><br/>

    <b>2. TF-IDF Based Matching:</b><br/>
    This traditional lexical approach identifies surface-level similarities such as repeated phrases or identical word usage. 
    It is particularly effective in flagging direct or near-direct copying of textual content.<br/><br/>

    <b>3. Paraphrasing Detection:</b><br/>
    An additional paraphrase-aware component has been introduced to identify submissions that may have been reworded while preserving the same meaning. 
    This helps uncover more nuanced cases of content reuse.<br/><br/>

    <b>4. Composite Similarity Score:</b><br/>
    To ensure a balanced evaluation, we compute a composite score by combining the outputs from each method:<br/>
    • <b>Contextual Similarity:</b> 0.4 weight — emphasizes conceptual overlap and rephrased similarities.<br/>
    • <b>Paraphrasing Detection:</b> 0.4 weight — captures meaning-preserving rewording.<br/>
    • <b>TF-IDF:</b> 0.2 weight — retains sensitivity to exact phrase-level copying.<br/><br/>
    This weighting scheme ensures that the final score reflects both deep semantic similarity and surface-level duplication while avoiding over-penalizing coincidental keyword matches.


    """
    elements.append(Paragraph(methodology_text, styles["Normal"]))

    # === Build PDF ===
    doc.build(elements)
    
    print(f"Report saved to {output_path}")