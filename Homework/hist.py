import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from app import number_of_unique_instances_file

def non_numeric_values():
    def is_float(string):
        try:
            float(string)
            return True
        except ValueError:
            return False

    def is_integer(string):
        return string.isdigit()
    values = {}
    unique_vals = number_of_unique_instances_file()  
    for attr in unique_vals.keys():
        for key in unique_vals[attr].keys():  
            if not (is_float(str(key)) or is_integer(str(key))):
                if attr not in values:
                    values[attr] = []
                values[attr].append(key)

    return values

def main():
    unique_instances = number_of_unique_instances_file()
    
    non_numeric_attributes = non_numeric_values(unique_instances)
    
    print(non_numeric_attributes)
    
if __name__ == "__main__":
    main()
