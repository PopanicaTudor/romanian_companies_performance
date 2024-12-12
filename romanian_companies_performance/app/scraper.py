import csv
import os
import matplotlib
matplotlib.use('Agg')  # Backend non-interactiv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import joblib

def scrape_company_data(company_identifier):
    """
    Citește datele din fișierul CSV și returnează informațiile companiei specificate,
    precum și datele tuturor companiilor pentru comparație.
    """
    # Obținem calea absolută către fișierul CSV
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Directorul `app`
    csv_path = os.path.join(base_dir, '../data/companies.csv')

    all_data = []  # Lista pentru toate companiile
    company_data = None  # Datele companiei căutate

    # Citește datele din fișierul CSV
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convertim cifrele în numere pentru procesare
            row['Turnover'] = float(row['Turnover'])
            row['Profit'] = float(row['Profit'])
            all_data.append(row)

            # Dacă identificatorul se potrivește (CUI sau nume), salvăm datele
            if company_identifier in (row['CUI'], row['Name']):
                company_data = row

    return company_data, all_data

def generate_comparison_chart(company, all_data):
    # Calculăm media cifrei de afaceri și a profitului
    avg_turnover = sum([c['Turnover'] for c in all_data]) / len(all_data)
    avg_profit = sum([c['Profit'] for c in all_data]) / len(all_data)

    # Date pentru grafic în milioane
    categories = ['Cifra de afaceri', 'Profit']
    company_values = [company['Turnover'] / 1_000_000, company['Profit'] / 1_000_000]
    average_values = [avg_turnover / 1_000_000, avg_profit / 1_000_000]

    # Configurăm barele
    x = np.arange(len(categories))
    width = 0.35

    fig, ax = plt.subplots()
    ax.bar(x - width/2, company_values, width, label='Companie', color='blue')
    ax.bar(x + width/2, average_values, width, label='Media concurenței', color='orange')

    # Configurăm axele și titlul
    ax.set_title(f"{company['Name']}")
    ax.set_ylabel('Valoare (mil. RON)')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()

    # Formatter pentru a afișa numerele cu o zecimală
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.1f}'))

    # Salvăm graficul
    base_dir = os.path.dirname(os.path.abspath(__file__))
    chart_path = os.path.abspath(os.path.join(base_dir, '../static/comparison_chart.png'))
    plt.savefig(chart_path)
    plt.close()

    return chart_path

def predict_profit(turnover):
    """
    Prezice profitul pe baza cifrei de afaceri.
    """
    # Încărcăm modelul antrenat
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.abspath(os.path.join(base_dir, '../model/profit_prediction_model.pkl'))
    model = joblib.load(model_path)

    # Prezicem profitul considerând o creștere de 3.5% a cifrei de afaceri, o scădere de 1.5% a costurilor operaționalem și o creștere de 1.2% a datoriilor
    growth_rate = 0.035 # 3.5% creștere
    operational_costs = 0.015 # 1.5% scădere
    debts = 0.012 # 1.2% creștere
    new_turnover = turnover * (1 + growth_rate) # Cifra de afaceri nouă
    new_costs = turnover * operational_costs # Costuri operaționale noi
    new_debts = turnover * debts # Datorii noi

    # Prezicem profitul
    profit = model.predict([[new_turnover, new_costs, growth_rate, new_debts]])[0]
    
    return profit