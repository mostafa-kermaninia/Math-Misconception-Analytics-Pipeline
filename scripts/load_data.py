import pandas as pd
from database_connection import get_db_engine

def load_data():
    """Queries data from the database and loads it into pandas DataFrames."""
    
    # Create the database connection
    engine = get_db_engine()
    
    # Query the data from database tables
    query_questions = "SELECT * FROM Questions"
    query_answers = "SELECT * FROM Answers"
    query_misconceptions = "SELECT * FROM Misconceptions"
    
    # Load the data into pandas DataFrames
    df_questions = pd.read_sql(query_questions, engine)
    df_answers = pd.read_sql(query_answers, engine)
    df_misconceptions = pd.read_sql(query_misconceptions, engine)
    
    return df_questions, df_answers, df_misconceptions

if __name__ == "__main__":
    # Load the data and print the first few rows
    df_questions, df_answers, df_misconceptions = load_data()
    print("Questions DataFrame loaded:", df_questions.head())
    print("Answers DataFrame loaded:", df_answers.head())
    print("Misconceptions DataFrame loaded:", df_misconceptions.head())
