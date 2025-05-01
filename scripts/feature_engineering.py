import pandas as pd
from scripts.load_data import load_data  # Import load_data function

def feature_engineering(df_questions, df_answers, df_misconceptions):
    """Perform feature engineering on the dataset."""
    
    # Create new features from existing columns (e.g., combining `ConstructName` and `SubjectName`)
    df_questions['Construct_Subject'] = df_questions['ConstructName'].astype(str) + "_" + df_questions['SubjectName'].astype(str)

    # # Aggregate answer data: calculate the total number of answers for each question
    # answer_counts = df_answers.groupby('QuestionId').size().reset_index(name='AnswerCount')
    # df_questions = df_questions.merge(answer_counts, on='QuestionId', how='left')

    # Extract feature from Misconceptions (if needed)
    # df_misconceptions['MisconceptionLength'] = df_misconceptions['MisconceptionName'].apply(len)
    # df_questions = df_questions.merge(df_misconceptions[['MisconceptionId', 'MisconceptionLength']], 
    #                                   left_on='CorrectAnswer', right_on='MisconceptionId', how='left')
    
    # Save processed data to a new CSV or Pickle file
    df_questions.to_csv('./processed_data/processed_questions.csv', index=False)
    df_answers.to_csv('./processed_data/processed_answers.csv', index=False)
    df_misconceptions.to_csv('./processed_data/misconceptions.csv', index=False)
    
    return df_questions, df_answers

if __name__ == "__main__":
    # Load and preprocess data
    df_questions, df_answers, df_misconceptions = load_data()  # Load data using load_data()
    
    # Perform feature engineering
    df_questions, df_answers = feature_engineering(df_questions, df_answers, df_misconceptions)
    
    print("Feature engineering complete!")
