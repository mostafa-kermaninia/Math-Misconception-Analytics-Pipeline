import pandas as pd
from scripts.load_data import load_data
import re


def preprocess_data(df_questions, df_answers, df_misconceptions):
    """
    Create a dataset for LLM training with enhanced features.
    Args:
        df: Original DataFrame (train.csv).
        misconception_map: DataFrame mapping MisconceptionId to MisconceptionName.
    Returns:
        A DataFrame optimized for LLM training.
    """
    preprocess_data = []

    for _, row in df_questions.iterrows():
        question_id = row["QuestionId"]
        question_text = row["QuestionText"]
        correct_ans = row["CorrectAnswer"]
        construct = row["ConstructName"]
        # construct_subject = row["Construct_Subject"]
        subject = row["SubjectName"]
        correct_text = df_answers.loc[
            (df_answers["AnswerType"] == question_id) &
            (df_answers["QuestionId"] == correct_ans),
            "AnswerText"
        ]

        # Extract all options
        options = {
            'A': df_answers.loc[
                (df_answers["QuestionId"] == question_id)
                & (df_answers["AnswerType"] == "A"),
                "AnswerText"
            ],
            'B': df_answers.loc[
                (df_answers["QuestionId"] == question_id)
                & (df_answers["AnswerType"] == "B"),
                "AnswerText"
            ],
            'C': df_answers.loc[
                (df_answers["QuestionId"] == question_id)
                & (df_answers["AnswerType"] == "C"),
                "AnswerText"
            ],
            'D': df_answers.loc[
                (df_answers["QuestionId"] == question_id)
                & (df_answers["AnswerType"] == "D"),
                "AnswerText"
            ]
        }

        # Process each incorrect option
        for option, text in options.items():
            if option == correct_ans:
                continue

            misconception_id = df_answers.loc[
                (df_answers["QuestionId"] == question_id)
                & (df_answers["AnswerType"] == option),
                "MisconceptionId"
            ]
            misconception_id = misconception_id.iloc[0]
            if pd.isna(misconception_id):
                continue

            # Get misconception description
            misconception_desc = df_misconceptions.loc[
                df_misconceptions["MisconceptionId"] == misconception_id,
                "MisconceptionName"
            ].values[0]

            # Feature engineering for LLM
            preprocess_data.append({
                "question_id": question_id,
                "question_text": question_text,
                "construct": construct,
                "subject": subject,
                "correct_option": correct_ans,
                "correct_text": correct_text,
                "incorrect_option": option,
                "incorrect_text": text,
                "has_math_symbols": bool(re.search(r'[\+\-\×\÷\=\^\√]', question_text)),
                "misconception_id": int(misconception_id),
                "misconception_desc": misconception_desc,
            })

    return pd.DataFrame(preprocess_data)


# def preprocess_data(df_questions, df_answers, df_misconceptions):
#     """Preprocess the data by handling missing values and normalizing features."""

#     # Handle missing values (e.g., filling missing misconceptions with 'Unknown')
#     df_answers['MisconceptionId'].fillna('Unknown', inplace=True)

#     # Convert categorical columns to numeric using label encoding
#     df_questions['ConstructName'] = df_questions['ConstructName'].astype('category').cat.codes
#     df_questions['SubjectName'] = df_questions['SubjectName'].astype('category').cat.codes

#     # Clean invalid text values in the Misconception column (if any)
#     df_misconceptions['MisconceptionName'].fillna('No Misconception', inplace=True)
#     return df_questions, df_answers, df_misconceptions
if __name__ == "__main__":
    # Load data
    df_questions, df_answers, df_misconceptions = load_data()

    # Preprocess data
    preprocessed_data = preprocess_data(
        df_questions, df_answers, df_misconceptions)

    # df_questions, df_answers, df_misconceptions = preprocess_data(df_questions, df_answers, df_misconceptions)

    print("Preprocessing complete!")
    print("Processed Questions DataFrame:", df_questions.head())
    print("Processed Answers DataFrame:", df_answers.head())
    print("Processed Misconceptions DataFrame:", df_misconceptions.head())
