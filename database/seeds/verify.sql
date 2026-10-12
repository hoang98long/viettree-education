-- Chỉ đọc; chạy trong database viettree-education sau seed.
SELECT g.grade, s.code, COUNT(DISTINCT t.id) AS topics, COUNT(DISTINCT l.id) FILTER (WHERE l.status='published') AS lessons,
       COUNT(DISTINCT q.id) FILTER (WHERE qv.status='published') AS questions,
       COUNT(DISTINCT a.id) FILTER (WHERE a.status='published') AS assessments
FROM subjects s
CROSS JOIN (VALUES (3), (4)) AS g(grade)
LEFT JOIN topics t ON t.subject_id=s.id AND t.grade=g.grade
LEFT JOIN lessons l ON l.topic_id=t.id
LEFT JOIN questions q ON q.topic_id=t.id AND q.grade=g.grade
LEFT JOIN question_versions qv ON qv.question_id=q.id
LEFT JOIN assessments a ON a.topic_id=t.id AND a.grade=g.grade
WHERE s.code IN ('MATH','VIETNAMESE','ENGLISH') GROUP BY g.grade, s.code ORDER BY g.grade, s.code;

SELECT a.code, COUNT(ai.id) AS valid_items FROM assessments a
JOIN assessment_items ai ON ai.assessment_id=a.id
JOIN question_versions qv ON qv.id=ai.question_version_id
WHERE a.grade IN (3,4) AND a.status='published' AND qv.published_at IS NOT NULL AND qv.status IN ('published','archived')
GROUP BY a.code ORDER BY a.code;

SELECT q.code AS missing_skill FROM questions q
JOIN question_versions qv ON qv.question_id=q.id
LEFT JOIN question_skills qs ON qs.question_version_id=qv.id
WHERE q.grade IN (3,4) AND qv.status='published' AND qs.skill_id IS NULL;
