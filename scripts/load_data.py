import pandas as pd

def load_misconceptions():
    return pd.read_csv("./database/misconception_mapping.csv")

def load_questions():
    return pd.read_csv("./database/train.csv")
