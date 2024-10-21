import pandas as pd
import matplotlib.pyplot as plt

# 1. Citirea datelor dintr-un fișier CSV
# data = pd.read_csv('dataset.csv')  # Înlocuiește cu locația fișierului tău

# Exemplu de DataFrame (pune în locul acestuia dataset-ul tău real)
data = pd.DataFrame({
    'rasă': ['Siamese', 'Bengal', 'Sphynx', 'Bengal', 'Sphynx', 'Siamese'],
    'culoare': ['Alb', 'Negru', 'Alb', 'Maro', 'Maro', 'Negru'],
    'greutate': [4.5, 5.0, 3.8, 4.2, 4.0, 4.7]
})

# 2. Aplicarea One-Hot Encoding pe coloanele non-numerice (de exemplu: 'rasă' și 'culoare')
data_encoded = pd.get_dummies(data, columns=['rasă', 'culoare'])

print("Datele după aplicarea One-Hot Encoding:")
print(data_encoded.head())

# 3. Afișarea grafică a distribuției valorilor folosind histogramă
plt.figure(figsize=(10,8))
data_encoded.hist(figsize=(10,8), bins=10)
plt.suptitle('Histograme pentru atributele one-hot codificate', fontsize=16)
plt.show()

# 4. Afișarea boxplot-urilor pentru fiecare atribut codificat
plt.figure(figsize=(12,8))
data_encoded.boxplot()
plt.title('Boxplot pentru atributele one-hot codificate', fontsize=16)
plt.xticks(rotation=45)  # Rotirea etichetelor pentru claritate
plt.show()
