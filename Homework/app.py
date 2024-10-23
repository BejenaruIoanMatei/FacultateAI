from typing import Counter
import pandas as pd
import os
here = os.path.dirname(os.path.abspath(__file__))


filename = os.path.join(here, 'dataset.xlsx')
file = pd.read_excel(filename)


#check errors
def check_errors(file):
    null_vals=[col for col,val in file.isnull().sum().items()if int(val) != 0]
    dupes= [col for col,val in file.duplicated().items() if val=="True"]

    if len(null_vals)!=0:
        for val in null_vals:
            print(f"Column '{val}' has null values")
    else:
        print("There are no columns with null values in the current dataset")

    if len(dupes)!=0:
        print(f"The following entries: {dupes} have duplicates")
    else:
        print("There are no duplicates in the current dataset")

