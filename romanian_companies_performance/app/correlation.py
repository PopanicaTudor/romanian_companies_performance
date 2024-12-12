import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv("F:\\Poze Tudor\\Facultate\\An 2\\Sem 1\\TW\\romanian_companies_performance\\romanian_companies_performance\\data\\companies.csv")

# Calculate the correlation matrix, ignoring the first two columns
correlation_matrix = df.iloc[:, 2:].corr()

# Print the correlation matrix
print(correlation_matrix)