import pandas as pd

def load_commodities_data(file_path):
    # Read the Excel file 
    df = pd.read_excel(file_path, sheet_name='Return Indices')
    df['Dates'] = pd.to_datetime(df['Dates'])
    return df
