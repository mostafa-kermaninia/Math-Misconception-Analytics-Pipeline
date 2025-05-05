import pandas as pd
from sqlalchemy import create_engine, text
from database_connection import get_db_engine

def reset_database():
    """Reset the entire database schema"""
    engine = get_db_engine()
    with engine.begin() as conn:
        # غیرفعال کردن بررسی کلیدهای خارجی
        conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
        
        # حذف تمام جداول با ترتیب صحیح
        conn.execute(text("DROP TABLE IF EXISTS Answers"))
        conn.execute(text("DROP TABLE IF EXISTS Questions"))
        conn.execute(text("DROP TABLE IF EXISTS Misconceptions"))
        
        # ایجاد مجدد دیتابیس
        conn.execute(text("CREATE DATABASE IF NOT EXISTS University_DB"))
        conn.execute(text("USE University_DB"))
        
        # ایجاد جداول با ترتیب صحیح
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS Questions (
                QuestionId INT PRIMARY KEY,
                ConstructId INT NOT NULL,
                ConstructName VARCHAR(255) NOT NULL,
                SubjectId INT NOT NULL,
                SubjectName VARCHAR(255) NOT NULL,
                CorrectAnswer CHAR(1) NOT NULL CHECK (CorrectAnswer IN ('A', 'B', 'C', 'D')),
                QuestionText TEXT NOT NULL,
                INDEX idx_construct (ConstructId),
                INDEX idx_subject (SubjectId)
            ) ENGINE=InnoDB;
        """))
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS Misconceptions (
                MisconceptionId INT PRIMARY KEY,
                MisconceptionName TEXT NOT NULL,
                FULLTEXT INDEX idx_misconception_name (MisconceptionName)
            ) ENGINE=InnoDB;
        """))
        
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS Answers (
                QuestionId INT NOT NULL,
                AnswerType CHAR(1) NOT NULL CHECK (AnswerType IN ('A', 'B', 'C', 'D')),
                AnswerText TEXT NOT NULL,
                MisconceptionId INT DEFAULT NULL,
                PRIMARY KEY (QuestionId, AnswerType),
                FOREIGN KEY (QuestionId) 
                    REFERENCES Questions(QuestionId) 
                    ON DELETE CASCADE,
                FOREIGN KEY (MisconceptionId) 
                    REFERENCES Misconceptions(MisconceptionId) 
                    ON DELETE SET NULL,
                INDEX idx_misconception (MisconceptionId)
            ) ENGINE=InnoDB;
        """))
        
        # فعال کردن مجدد بررسی کلیدهای خارجی
        conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))
    print("✅ Database reset complete!")

def import_misconceptions():
    """Import misconceptions data into the database."""
    engine = get_db_engine()
    df_misconceptions = pd.read_csv("./database/misconception_mapping.csv")
    
    with engine.begin() as conn:
        # حذف داده‌های موجود قبل از وارد کردن
        conn.execute(text("DELETE FROM Misconceptions"))
        
        df_misconceptions.to_sql(
            name="Misconceptions",
            con=conn,
            if_exists="append",
            index=False
        )
    print("✅ Misconceptions imported!")

def import_questions():
    """Import questions data into the database."""
    engine = get_db_engine()
    df_questions = pd.read_csv("./database/train.csv")
    questions_data = df_questions[["QuestionId", "ConstructId", "ConstructName", "SubjectId", "SubjectName", "CorrectAnswer", "QuestionText"]]
    
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM Questions"))
        questions_data.to_sql(
            name="Questions",
            con=conn,
            if_exists="append",
            index=False
        )
    print("✅ Questions imported!")

def import_answers():
    """Import answers data into the database."""
    engine = get_db_engine()
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
    
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM Answers"))
        df_answers_final.to_sql(
            name="Answers",
            con=conn,
            if_exists="append",
            index=False
        )
    print("✅ Answers imported!")

if __name__ == "__main__":
    # ترتیب صحیح اجرا
    reset_database()       # اول: بازسازی کامل دیتابیس
    import_questions()     # دوم: سوالات (پدر جدول Answers)
    import_misconceptions() # سوم: misconceptions (وابسته به Answers)
    import_answers()       # چهارم: پاسخ‌ها (وابسته به هر دو)