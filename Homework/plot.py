import pandas as pd
import matplotlib.pyplot as plt
from app import get_data
data = get_data()

categorical_columns = ['Sexe', 'Race', 'Zone'] 
data_encoded = pd.get_dummies(data, columns=categorical_columns)

print("Datele după aplicarea One-Hot Encoding:")
print(data_encoded.head())


numeric_columns = data_encoded.select_dtypes(include=['float64', 'int64']).columns

if not numeric_columns.empty:
    plt.figure(figsize=(10, 8))
    data_encoded[numeric_columns].hist(figsize=(10, 8), bins=10)
    plt.suptitle('Histograme pentru atributele numerice', fontsize=16)
    plt.show()
else:
    print("Nu există coloane numerice pentru a genera histograme.")

if not numeric_columns.empty:
    plt.figure(figsize=(12, 8))
    data_encoded[numeric_columns].boxplot()
    plt.title('Boxplot pentru atributele numerice', fontsize=16)
    plt.xticks(rotation=45)  
else:
    print("Nu există coloane numerice pentru a genera boxplot-uri.")
