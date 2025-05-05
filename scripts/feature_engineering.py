import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from load_data import load_data  # Import load_data function
from preprocess import preprocess_data 
import re
from database_operations.import_df_to_db import import_dataframe

def subject_clustering(df_dataset):
    subjects = df_dataset['subject'].unique()
    # Convert subjects into numerical vectors using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(subjects)  # X is the TF-IDF weighted document-term matrix

    # Set number of clusters 
    n_clusters = 8
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)  # Initialize KMeans with fixed random state for reproducibility
    clusters = kmeans.fit(X)  # Fit the model to the data

    # Assign cluster labels to each subject
    subject_cluster_map = dict(zip(subjects, kmeans.labels_))  # Creates a {subject: cluster_label} mapping
        # Create a dictionary to map cluster numbers to human-readable names
    cluster_names = {
        0: "Measurement Units & Conversions",
        1: "Fractions, Decimals & Percentages",
        2: "Graphs & Data Visualization",
        3: "Geometric Shapes & Properties",
        4: "Numerical Sequences & Patterns",
        5: "Lines & Coordinate Geometry",
        6: "Angles & Polygons",
        7: "Core Mathematical Fundamentals",
    }

    # Add new column to dataset mapping subjects to their cluster names
    df_dataset['subject_cluster'] = df_dataset['subject'].map(subject_cluster_map).map(cluster_names)
    # Define the mapping to merge similar subjects
    subject_mapping = {
        # Merge fractions/decimals with measurements
        'Fractions, Decimals & Percentages': 'Fractions, Decimals & Conversions',
        'Measurement Units & Conversions': 'Fractions, Decimals & Conversions',
        
        # Merge geometric concepts
        'Geometric Shapes & Properties': 'Geometry & Shapes',
        'Angles & Polygons': 'Geometry & Shapes',
        
        # Merge visualization and coordinate geometry
        'Graphs & Data Visualization': 'Graphs & Coordinate Geometry',
        'Lines & Coordinate Geometry': 'Graphs & Coordinate Geometry',
        
        # Keep these subjects unchanged
        'Core Mathematical Fundamentals': 'Core Mathematical Fundamentals',
        'Numerical Sequences & Patterns': 'Numerical Sequences & Patterns'
    }

    # Update the subject_cluster column using the mapping
    df_dataset['subject_cluster'] = df_dataset['subject_cluster'].map(subject_mapping)
    return df_dataset

def calculate_difficulty(question):
    # Initialize scores
    operator_score = 0
    length_score = 0
    steps_score = 0
    misconceptions_score = 0
    abstraction_score = 0
    knowledge_score = 0
    
    # 1. Operator Count (Count basic/advanced/complex operators)
    basic_ops = len(re.findall(r'[\+\-\*\/]', question))
    advanced_ops = len(re.findall(r'[\√\^]|log|sin|cos|tan|exp', question, re.IGNORECASE))
    complex_ops = len(re.findall(r'\\int|\\sum|lim|deriv|matrix|d/dx', question, re.IGNORECASE))
    operator_score = basic_ops * 1 + advanced_ops * 2 + complex_ops * 3
    
    # 2. Question Length (Word count)
    word_count = len(question.split())
    if word_count < 15:
        length_score = 1
    elif 15 <= word_count <= 30:
        length_score = 2
    else:
        length_score = 3
    
    # 3. Answer Steps (Estimated steps based on operators/keywords)
    steps_estimate = basic_ops + advanced_ops + complex_ops
    if "solve for" in question.lower() or "find" in question.lower():
        steps_estimate += 2  # Extra steps for equation solving
    if steps_estimate <= 2:
        steps_score = 1
    elif 3 <= steps_estimate <= 5:
        steps_score = 2
    else:
        steps_score = 3
    
    # 4. Type of question 
    misconceptions = 0
    if "simplify" in question.lower() or "expand" in question.lower():
        misconceptions += 1
    misconceptions_score = misconceptions
    
    # 5. Abstraction Level
    if re.search(r'[a-zA-Z]', question):  # Variables present
        abstraction_score = 2
        if "word problem" in question.lower() or "real-world" in question.lower():
            abstraction_score = 3
    else:
        abstraction_score = 1  # Numerical only
    
    # 6. Required Knowledge
    if re.search(r'derivative|integral|limit|matrix', question, re.IGNORECASE):
        knowledge_score = 3
    elif re.search(r'algebra|geometry|equation', question, re.IGNORECASE):
        knowledge_score = 2
    else:
        knowledge_score = 1  # Arithmetic
    
    # Total Score
    total_score = (
        operator_score + length_score + steps_score +
        misconceptions_score + abstraction_score + knowledge_score
    )
    
    # Determine Difficulty Label
    if total_score <= 6:
        return 'Easy'
    elif 7 <= total_score <= 10:
        return 'Medium'
    else:
        return 'Hard'
    # return total_score

def add_hardness_label(df_dataset):
    # Step 1: Extract unique questions from df_dataset
    unique_questions = df_dataset[['question_id', 'question_text']].drop_duplicates()

    # Step 2: Calculate difficulty for each unique question
    unique_questions['difficulty'] = unique_questions['question_text'].apply(calculate_difficulty)

    # Step 3: Merge difficulty back into the original df_dataset
    df_dataset = df_dataset.merge(
        unique_questions[['question_id', 'difficulty']],
        on='question_id',
        how='left'
    )
    return df_dataset

def misconception_clustering(df_dataset):
    misconceptions = df_dataset['misconception_desc'].unique()
    # Convert misconceptions into numerical vectors using TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)  # Limiting features for efficiency
    X = vectorizer.fit_transform(misconceptions)  # Creates TF-IDF weighted document-term matrix

    # Set number of clusters (14 clusters based on prior analysis)
    n_clusters = 14
    kmeans = KMeans(n_clusters=n_clusters, 
                    init='k-means++',  # Better initialization method
                    random_state=42,    # For reproducibility
                    n_init=10)         # Number of initializations to run
    clusters = kmeans.fit(X)  # Fit the model to the data

    # Assign cluster labels to each misconception
    misconception_cluster_map = dict(zip(misconceptions, kmeans.labels_))  # Creates {misconception: cluster_label} mapping
    cluster_names = {
        0: "Ratio & Proportional Reasoning Errors",
        1: "Fraction Operations & Concepts",
        2: "Algebraic Expressions & Sequences",
        3: "Geometric Concepts & Properties",
        4: "Negative Numbers & Inequalities",
        5: "Fundamental Arithmetic Misconceptions", 
        6: "Decimal Operations & Place Value",
        7: "Spatial Reasoning & Estimation",
        8: "Basic Operation Confusions",
        9: "Simplification & Conversion Errors",
        10: "Data Handling & Number Sense",
        11: "Advanced Functions & Graphs",
        12: "Core Mathematical Knowledge Gaps",
        13: "Fraction Arithmetic & Algebra"
    }
    df_dataset['misconception_cluster'] = df_dataset['misconception_desc'].map(misconception_cluster_map).map(cluster_names)
    df_dataset['misconception_clusterId'] = df_dataset['misconception_desc'].map(misconception_cluster_map)

    cluster_mapping = {
        # Fundamental Arithmetic Group
        'Fundamental Arithmetic Misconceptions': 'Fundamental_Arithmetic',
        'Basic Operation Confusions': 'Fundamental_Arithmetic',
        'Core Mathematical Knowledge Gaps': 'Fundamental_Arithmetic',
        'Decimal Operations & Place Value': 'Fundamental_Arithmetic',
        
        # Fractions & Ratios Group
        'Fraction Operations & Concepts': 'Fractions_Ratios',
        'Fraction Arithmetic & Algebra': 'Fractions_Ratios',
        'Ratio & Proportional Reasoning Errors': 'Fractions_Ratios',
        
        # Algebra & Advanced Math Group
        'Advanced Functions & Graphs': 'Algebra_Advanced_Math',
        'Algebraic Expressions & Sequences': 'Algebra_Advanced_Math',
        'Negative Numbers & Inequalities': 'Algebra_Advanced_Math',
        
        # Geometry & Spatial Reasoning Group
        'Spatial Reasoning & Estimation': 'Geometry_Spatial',
        'Geometric Concepts & Properties': 'Geometry_Spatial',
        
        # Data & Conversions Group
        'Simplification & Conversion Errors': 'Data_Conversions',
        'Data Handling & Number Sense': 'Data_Conversions'
    }

    df_dataset['misconception_merged'] = df_dataset['misconception_cluster'].map(cluster_mapping)
    cluster_mapping2num = {
        'Fundamental_Arithmetic': 1,
        'Fractions_Ratios': 2,
        'Algebra_Advanced_Math': 3,
        'Geometry_Spatial': 4,
        'Data_Conversions': 5
    }
    df_dataset['misconception_merged_id'] = df_dataset['misconception_merged'].map(cluster_mapping2num)
    return df_dataset

def feature_engineering(df_dataset):
    """Perform feature engineering on the dataset."""
    df_dataset = subject_clustering(df_dataset)
    df_dataset = add_hardness_label(df_dataset)
    df_dataset = misconception_clustering(df_dataset)
    
    # Save processed data to a new CSV or Pickle file
    df_questions.to_csv('./processed_data/processed_questions.csv', index=False)
    df_answers.to_csv('./processed_data/processed_answers.csv', index=False)
    df_misconceptions.to_csv('./processed_data/misconceptions.csv', index=False)
    df_dataset.to_csv('./processed_data/dataset.csv', index=False)
    # print(df_dataset.head())
    return df_dataset

if __name__ == "__main__":
    # Load and preprocess data
    df_questions, df_answers, df_misconceptions = load_data()  # Load data using load_data()
    
    df_dataset = preprocess_data(df_questions, df_answers, df_misconceptions)
    # Perform feature engineering
    df_dataset = feature_engineering(df_dataset)
    # import_dataframe(df_dataset)
    print("Feature engineering complete!")
