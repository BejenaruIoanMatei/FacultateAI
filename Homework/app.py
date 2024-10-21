import pandas as pd
import os
here = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(here, 'dataset.xlsx')
file = pd.read_excel(filename)
print(file)