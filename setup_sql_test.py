
import sqlite3

DB_NAME = "sql_detective_test.db"

query = """
WITH recruiter_placements AS (
    SELECT
        jp.department,
        r.id AS recruiter_id,
        r.name AS recruiter_name,
        COUNT(
            CASE
                WHEN i.stage = 'Final'
                 AND i.outcome = 'passed'
                THEN 1
            END
        ) AS successful_placements
    FROM job_postings AS jp
    JOIN recruiters AS r
        ON jp.recruiter_id = r.id
    LEFT JOIN interviews AS i
        ON i.job_posting_id = jp.id
    GROUP BY jp.department, r.id, r.name
),
ranked_placements AS (
    SELECT
        department,
        recruiter_id,
        recruiter_name,
        successful_placements,
        DENSE_RANK() OVER (
            PARTITION BY department
            ORDER BY successful_placements DESC
        ) AS placement_rank
    FROM recruiter_placements
)
SELECT
    department,
    recruiter_id,
    recruiter_name,
    successful_placements
FROM ranked_placements
WHERE placement_rank = 1
ORDER BY department, recruiter_name;
"""

connection = sqlite3.connect(DB_NAME)

try:
    for row in connection.execute(query):
        print(row)
finally:
    connection.close()
