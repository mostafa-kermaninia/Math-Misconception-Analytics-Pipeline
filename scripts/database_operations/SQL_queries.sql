SELECT 
    q.QuestionId, 
    q.QuestionText, 
    a.AnswerType, 
    a.AnswerText, 
    m.MisconceptionName
FROM 
    Questions q
JOIN 
    Answers a ON q.QuestionId = a.QuestionId
LEFT JOIN 
    Misconceptions m ON a.MisconceptionId = m.MisconceptionId;



SELECT 
    q.QuestionId, 
    q.QuestionText, 
    COUNT(DISTINCT m.MisconceptionId) AS MisconceptionCount
FROM 
    Questions q
JOIN 
    Answers a ON q.QuestionId = a.QuestionId
LEFT JOIN 
    Misconceptions m ON a.MisconceptionId = m.MisconceptionId
GROUP BY 
    q.QuestionId, q.QuestionText
ORDER BY 
    MisconceptionCount DESC;


SELECT 
    q.QuestionId, 
    q.QuestionText, 
    a.AnswerType, 
    a.AnswerText, 
    m.MisconceptionName
FROM 
    Questions q
JOIN 
    Answers a ON q.QuestionId = a.QuestionId
LEFT JOIN 
    Misconceptions m ON a.MisconceptionId = m.MisconceptionId
WHERE 
    a.AnswerType != q.CorrectAnswer;


SELECT 
    a.AnswerType, 
    m.MisconceptionName, 
    COUNT(*) AS MisconceptionCount
FROM 
    Answers a
LEFT JOIN 
    Misconceptions m ON a.MisconceptionId = m.MisconceptionId
GROUP BY 
    a.AnswerType, m.MisconceptionName
ORDER BY 
    MisconceptionCount DESC;
