from flask import Blueprint, render_template, request, send_file
from app.scraper import scrape_company_data, generate_comparison_chart, predict_profit
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Afișează pagina principală.
    """
    return render_template('index.html')

@main.route('/scan', methods=['POST'])
def scan_company():
    """
    Procesează formularul și caută compania specificată.
    """
    # Obținem identificatorul companiei (nume sau CUI)
    company_identifier = request.form.get('company_name_or_id')

    # Căutăm datele companiei
    company_data, all_data = scrape_company_data(company_identifier)

    if company_data is None:
        # Mesaj de eroare dacă identificatorul este invalid
        error_message = "Compania nu a fost găsită. Verifică numele sau codul CUI introdus."
        return render_template('index.html', error_message=error_message)

    # Generăm graficul
    chart_path = generate_comparison_chart(company_data, all_data)

    # Prezicem profitul
    predicted_profit = predict_profit(company_data['Turnover'])

    return render_template(
        'results.html',
        company_data=company_data,
        chart_path=chart_path,
        predicted_profit=predicted_profit
    )

@main.route('/download_report/<company_name>')
def download_report(company_name):
    """
    Endpoint pentru descărcarea raportului PDF al companiei.
    """
    # Găsim datele companiei
    company_data, all_data = scrape_company_data(company_name)

    if company_data is None:
        return "Compania nu a fost găsită."

    # Generăm graficul
    chart_path = generate_comparison_chart(company_data, all_data)

    # Construim calea către PDF
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(base_dir, '../static', f"{company_name}_report.pdf")

    # Importă funcția de generare a PDF-ului
    from app.generate_pdf_report import generate_pdf_report
    generate_pdf_report(pdf_path, company_data, chart_path, all_data)

    # Trimitem fișierul PDF către utilizator
    return send_file(pdf_path, as_attachment=True)