from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from app.scraper import predict_profit
import os
import glob

def generate_pdf_report(pdf_path, company_data, chart_path, all_data):
    """
    Generează un raport PDF care include datele companiei, comparația cu media și graficul.
    """
    # Șterge toate fișierele .pdf din folderul static
    static_folder = os.path.dirname(pdf_path)
    for pdf_file in glob.glob(os.path.join(static_folder, "*.pdf")):
        os.remove(pdf_file)

    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    normal_style = styles['BodyText']

    # Documentul PDF
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    elements = []

    # Titlu
    elements.append(Paragraph(f"Raport pentru {company_data['Name']}", title_style))
    elements.append(Spacer(1, 12))

    # Detalii despre companie
    elements.append(Paragraph(f"CUI: {company_data['CUI']}", normal_style))
    elements.append(Paragraph(f"Cifra de afaceri: {company_data['Turnover']:,} RON", normal_style))
    elements.append(Paragraph(f"Profit: {company_data['Profit']:,} RON", normal_style))

    # Prezicem profitul
    predicted_profit = predict_profit(company_data['Turnover'])
    elements.append(Paragraph(f"Profit prezis: {predicted_profit:,} RON", normal_style))
    elements.append(Spacer(1, 12))

    # Comparația cu media industriei
    avg_turnover = sum([c['Turnover'] for c in all_data]) / len(all_data)
    avg_profit = sum([c['Profit'] for c in all_data]) / len(all_data)
    elements.append(Paragraph("Comparatie cu media industriei:", title_style))
    elements.append(Paragraph(f"Cifra de afaceri medie: {avg_turnover:,.0f} RON", normal_style))
    elements.append(Paragraph(f"Profit mediu: {avg_profit:,.0f} RON", normal_style))
    elements.append(Spacer(1, 12))

    # Adăugăm graficul
    if os.path.exists(chart_path):
        elements.append(Image(chart_path, width=400, height=300))
    else:
        elements.append(Paragraph("Graficul nu a fost disponibil.", normal_style))

    # Generăm PDF-ul
    doc.build(elements)