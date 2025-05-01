import pandas as pd
import os

def load_clean_data():
    """
    لود فایل CSV از پوشه data
    """
    current_dir = os.path.dirname(__file__)
    data_path = os.path.join(current_dir, '../data/cleaned_dataset.csv')
    
    # لود داده با pandas
    df = pd.read_csv(data_path)
    return df