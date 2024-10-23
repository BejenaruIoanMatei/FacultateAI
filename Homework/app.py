import pandas as pd
import os

# Funcție care citește datele și verifică erorile
def load_and_check_data():
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, 'dataset.xlsx')

    # Citirea fișierului Excel
    file = pd.read_excel(filename)
    
    # Afișarea numelor coloanelor din dataset pentru verificare
    print("Coloanele din dataset:", file.columns)

    # Verificarea valorilor lipsă și duplicate
    null_vals = [col for col, val in file.isnull().sum().items() if int(val) != 0]
    dupes = file[file.duplicated()]

    # Afișarea erorilor
    if len(null_vals) != 0:
        for val in null_vals:
            print(f"Coloana '{val}' are valori lipsă.")
    else:
        print("Nu există coloane cu valori lipsă în dataset.")

    if len(dupes) != 0:
        print(f"Există {len(dupes)} intrări duplicate în dataset.")
    else:
        print("Nu există duplicate în dataset.")

    # Returnează dataset-ul pentru a fi folosit în alte funcții
    return file
