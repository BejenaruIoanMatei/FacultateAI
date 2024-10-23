import pandas as pd
import os
import pprint as pp

races={
    "BEN": "Bengal",
    "SBI": "Birman",
    "BRI": "British Shorthair",
    "CHA": "Chartreux",
    "EUR": "European",
    "MCO": "Maine coon",
    "PER": "Persian",
    "RAG": "Ragdoll",
    "SPH": "Sphynx",
    "ORI": "Siamese",
    "TUV": "Turkish angora",
    "Autre": "Other",
    "NSP": "Unknown",
    "NR":"No race",
    "SAV":"Savannah"
}
def get_data():
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, 'dataset.xlsx')
    file = pd.read_excel(filename)
    return file

def get_file(name, mode='r', content_to_write=None):
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, name)
    with open(filename, mode) as file:
        if 'r' in mode:
            return file.read()
        elif 'w' in mode or 'a' in mode:
            file.write(str(content_to_write))
            return f"Content written to {filename}"

def number_of_instances():
    file=get_data()
    races_count = dict()
    
    for index, line in file.iterrows():
        race=line['Race']
        if races[race] in races_count:
            races_count[races[race]]+=1
        else: 
            races_count[races[race]]=1
    return races_count

def fetch_for_column(column):
    file=get_data()
    col_dict=dict()
    for _, line in file.iterrows():
        col_val=line[column]
        if col_val in col_dict:
            col_dict[col_val]+=1
        else: 
            col_dict[col_val]=1
    return col_dict

def get_attributes():
    file=get_data()
    data_cols=file.columns
    col_arr=[]
    for index, column in enumerate(data_cols):
        if index>1 and index<len(data_cols)-1:
            col_arr.append(column)
    return col_arr

def number_of_unique_instances_races():
    unique_data = dict()
    file = get_data()
    col_arr = get_attributes()  

    for _, line in file.iterrows():
        race = line['Race']
        if race not in unique_data:
            unique_data[race] = {col: dict() for col in col_arr if col != 'Race'}

        for col in col_arr:
            if col != 'Race':
                attribute_value = line[col]
                if attribute_value not in unique_data[race][col]:
                    unique_data[race][col][attribute_value] = 0
                unique_data[race][col][attribute_value] += 1

    return unique_data




def number_of_unique_instances_file():
    unique_attr=dict()
    file=get_data()
    col_arr=get_attributes()


    for _, line in file.iterrows():
        for col in col_arr:
            if col not in unique_attr.keys():
                unique_attr[col]=dict()
            if line[col] not in unique_attr[col].keys():
                unique_attr[col][line[col]]=0
            unique_attr[col][line[col]]+=1
   
    return unique_attr


def load_and_check_data():
    file=get_data()
    
    print("Coloanele din dataset:", file.columns)

    null_vals = [col for col, val in file.isnull().sum().items() if int(val) != 0]
    dupes = file[file.duplicated()]
    
    if len(null_vals) != 0:
        for val in null_vals:
            print(f"Coloana '{val}' are valori lipsa.")
    else:
        print("Nu exista coloane cu valori lipsa in dataset.")

    if len(dupes) != 0:
        print(f"Exista {len(dupes)} intrari duplicate in dataset.")
    else:
        print("Nu exista duplicate in dataset.")

