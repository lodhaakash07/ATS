import pandas as pd

def load_commodities_data(file_path):
    # Read the Excel file and load the "Return Indices" sheet
    df = pd.read_excel(file_path, sheet_name='Return Indices')
    return df
