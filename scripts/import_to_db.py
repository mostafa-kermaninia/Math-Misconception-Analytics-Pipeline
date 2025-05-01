import pandas as pd
from sqlalchemy import create_engine
from scripts.database_connection import get_db_engine

# Function to import misconceptions
def import_misconceptions():
    df_misconceptions = pd.read_csv("./database/misconception_mapping.csv")
    df_misconceptions.to_sql(name="Misconceptions", con=get_db_engine(), if_exists="append", index=False)
    print("✅ Misconceptions imported!")

# Function to import questions
def import_questions():
    df_questions = pd.read_csv("./database/train.csv")
    questions_data = df_questions[["QuestionId", "ConstructId", "ConstructName", "SubjectId", "SubjectName", "CorrectAnswer", "QuestionText"]]
    questions_data.to_sql(name="Questions", con=get_db_engine(), if_exists="append", index=False)
    print("✅ Questions imported!")

# Function to import answers
def import_answers():
    df_answers = pd.read_csv("./database/train.csv")
    answers_list = []

    for _, row in df_answers.iterrows():
        question_id = row["QuestionId"]
        for answer_type in ['A', 'B', 'C', 'D']:
            answer_text = row[f"Answer{answer_type}Text"]
            misconception_id = row.get(f"Misconception{answer_type}Id") or None
            answers_list.append({
                "QuestionId": question_id,
                "AnswerType": answer_type,
                "AnswerText": answer_text,
                "MisconceptionId": misconception_id
            })

    df_answers_final = pd.DataFrame(answers_list)
    df_answers_final.to_sql(name="Answers", con=get_db_engine(), if_exists="append", index=False)
    print("✅ Answers imported!")
