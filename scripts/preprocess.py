import pandas as pd
from scripts.load_data import load_data

def preprocess_data(df_questions, df_answers, df_misconceptions):
    """Preprocess the data by handling missing values and normalizing features."""
    
    # Handle missing values (e.g., filling missing misconceptions with 'Unknown')
    df_answers['MisconceptionId'].fillna('Unknown', inplace=True)
    
    # Convert categorical columns to numeric using label encoding
    df_questions['ConstructName'] = df_questions['ConstructName'].astype('category').cat.codes
    df_questions['SubjectName'] = df_questions['SubjectName'].astype('category').cat.codes
    
    # Clean invalid text values in the Misconception column (if any)
    df_misconceptions['MisconceptionName'].fillna('No Misconception', inplace=True)
    
    return df_questions, df_answers, df_misconceptions

if __name__ == "__main__":
    # Load data
    df_questions, df_answers, df_misconceptions = load_data()
    
    # Preprocess data
    df_questions, df_answers, df_misconceptions = preprocess_data(df_questions, df_answers, df_misconceptions)
    
    print("Preprocessing complete!")
    print("Processed Questions DataFrame:", df_questions.head())
    print("Processed Answers DataFrame:", df_answers.head())
    print("Processed Misconceptions DataFrame:", df_misconceptions.head())
