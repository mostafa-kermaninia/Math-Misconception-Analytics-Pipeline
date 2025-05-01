DROP DATABASE IF EXISTS DataScience_DB;
CREATE DATABASE DataScience_DB;
USE DataScience_DB;



-- Table 1: Questions
CREATE TABLE Questions (
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

-- Table 2: Misconceptions
CREATE TABLE Misconceptions (
    MisconceptionId INT AUTO_INCREMENT PRIMARY KEY,
    MisconceptionName TEXT NOT NULL,
    FULLTEXT INDEX idx_misconception_name (MisconceptionName)
) ENGINE=InnoDB;

-- Table 3: Answers
CREATE TABLE Answers (
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