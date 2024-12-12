import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load the CSV file into a DataFrame
df = pd.read_csv("F:\\Poze Tudor\\Facultate\\An 2\\Sem 1\\TW\\romanian_companies_performance\\romanian_companies_performance\\data\\companies.csv")

# Despartim variabilele in caracteristici si variabile tinta
target_variable = 'Profit'
features = ['Turnover', 'Operational Costs', 'Growth Rate', 'Debts']

# Pregatim variabilele de antrenament si variabila tinta
X = df[features]
y = df[target_variable]

# Impartim datele in set de antrenament si set de testare
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Antrenam modelul
model = LinearRegression()

# Antrenam modelul
model.fit(X_train, y_train)

# Facem predictii pe setul de testare
y_pred = model.predict(X_test)

# Evaluam modelul
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Afisam rezultatele
print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')

# Salvam modelul
import joblib
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.abspath(os.path.join(base_dir, '../model/profit_prediction_model.pkl'))
joblib.dump(model, model_path)