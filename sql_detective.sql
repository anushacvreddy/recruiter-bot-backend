
-- Q1. List all open job postings and their recruiter names.
SELECT
    jp.id AS job_id,
    jp.title AS job_title,
    r.name AS recruiter_name
FROM job_postings AS jp
JOIN recruiters AS r
    ON jp.recruiter_id = r.id
WHERE jp.status = 'open'
ORDER BY jp.id;


-- Q2. Count applicants who reached the Final stage for each job.
SELECT
    jp.id AS job_id,
    jp.title AS job_title,
    COUNT(DISTINCT i.applicant_id) AS final_stage_applicants
FROM job_postings AS jp
LEFT JOIN interviews AS i
    ON jp.id = i.job_posting_id
    AND i.stage = 'Final'
GROUP BY jp.id, jp.title
ORDER BY jp.id;


-- Q3. Find people who effectively applied to more than one job.
-- Normalize email case to identify duplicate applicant records.
WITH normalized_applicants AS (
    SELECT
        id AS applicant_id,
        LOWER(TRIM(email)) AS normalized_email,
        full_name
    FROM applicants
),
person_job_applications AS (
    SELECT DISTINCT
        na.normalized_email,
        na.full_name,
        i.job_posting_id
    FROM normalized_applicants AS na
    JOIN interviews AS i
        ON i.applicant_id = na.applicant_id
)
SELECT
    normalized_email,
    MIN(full_name) AS applicant_name,
    COUNT(DISTINCT job_posting_id) AS jobs_applied_to
FROM person_job_applications
GROUP BY normalized_email
HAVING COUNT(DISTINCT job_posting_id) > 1
ORDER BY jobs_applied_to DESC, applicant_name;


-- Q4. Calculate each recruiter's Final-stage conversion rate.
-- Include only recruiters with at least 3 Final-stage interviews.
SELECT
    r.id AS recruiter_id,
    r.name AS recruiter_name,
    SUM(
        CASE WHEN i.outcome = 'passed' THEN 1 ELSE 0 END
    ) AS final_passed,
    COUNT(i.id) AS total_final_interviews,
    ROUND(
        100.0 * SUM(
            CASE WHEN i.outcome = 'passed' THEN 1 ELSE 0 END
        ) / COUNT(i.id),
        2
    ) AS conversion_rate_percent
FROM recruiters AS r
JOIN job_postings AS jp
    ON jp.recruiter_id = r.id
JOIN interviews AS i
    ON i.job_posting_id = jp.id
WHERE i.stage = 'Final'
GROUP BY r.id, r.name
HAVING COUNT(i.id) >= 3
ORDER BY conversion_rate_percent DESC, r.name;


-- Q5. Bonus: Find the recruiter(s) with the most successful
-- Final-stage placements per department, including ties and
-- departments where all recruiters have zero successful placements.
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
