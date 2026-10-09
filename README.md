# Recruiter Bot Backend

A Python-based backend service that matches candidates with job openings using skill overlap, experience fit, and culture alignment.

**Assignment:** RecruiterFlow Engineering — Backend Developer Assignment

## 1. Overview

Recruiter Bot is a backend application designed to rank candidates against job openings and rank jobs for individual candidates. It uses Flask to expose REST API endpoints and SQLite to store candidate and job information.

The project uses fictional candidate profiles and job descriptions supplied with the assignment. The matching algorithm calculates a score for each candidate-job pair and provides a short explanation to make the ranking easier to understand.

## 2. Tech Stack

- Python 3.12
- Flask
- SQLite
- Handwritten SQL
- pytest

No ORM or query-builder library is used for database interactions.

## 3. Features

- Seeds 15 fictional candidate profiles and 6 job openings.
- Creates relational database tables for candidates, jobs, and matches.
- Ranks candidates for a selected job.
- Ranks jobs for a selected candidate.
- Calculates weighted match scores.
- Generates short explanations for matching results.
- Returns HTTP 404 responses for unknown candidate or job IDs.
- Includes automated tests for the matching algorithm.
- Includes the separate SQL Detective challenge with five SQL queries.

## 4. Project Structure

```text
recruiter-bot-backend/
├── app.py
├── database.py
├── seed_data.py
├── matching.py
├── requirements.txt
├── README.md
├── sql_detective.sql
└── tests/
    └── test_matching.py
```

The SQLite database and virtual environment are generated locally and should not be committed to Git.

## 5. Installation and Setup

### Prerequisites

- Python 3.12 or a compatible Python version
- VS Code or another code editor
- Git, if cloning the repository

### Step 1: Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd recruiter-bot-backend
```

Replace `<YOUR_REPOSITORY_URL>` with the repository URL. Alternatively, open the project folder directly in VS Code.

### Step 2: Create and activate a virtual environment

Windows PowerShell:

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### Step 4: Create the database tables

```powershell
python database.py
```

### Step 5: Seed the candidate and job data

```powershell
python seed_data.py
```

The seed script inserts the supplied fictional data. Existing records with the same IDs are ignored when the script is run again.

### Step 6: Start the Flask application

```powershell
python app.py
```

The development server runs at:

`http://127.0.0.1:5000`

Keep the terminal open while testing the API.

## 6. API Endpoints

### Health check

**Endpoint:** `GET /`

```bash
curl http://127.0.0.1:5000/
```

Returns a message confirming that the API is running.

### Get candidates ranked for a job

**Endpoint:** `GET /jobs/<job_id>/matches`

```bash
curl http://127.0.0.1:5000/jobs/1/matches
```

Returns job details and candidates ranked by match score, with an explanation for each result.

### Get jobs ranked for a candidate

**Endpoint:** `GET /candidates/<candidate_id>/matches`

```bash
curl http://127.0.0.1:5000/candidates/1/matches
```

Returns candidate details and jobs ranked by match score, with an explanation for each result.

### Error handling

Requests for unknown job or candidate IDs return HTTP `404 Not Found`.

## 7. Matching Algorithm

The matching algorithm uses three weighted components:

| Component | Weight |
|---|---:|
| Skill overlap | 60% |
| Experience fit | 25% |
| Culture alignment | 15% |
| **Total** | **100%** |

### Skill overlap — 60%

The skill score is the percentage of required job skills that the candidate possesses.

For example, if a job requires four skills and a candidate matches three, the skill score is 75%.

### Experience fit — 25%

Candidates who meet or exceed the job's minimum experience requirement receive a full experience score.

Candidates below the minimum receive a proportional score based on their experience relative to the requirement. They are penalized rather than automatically excluded.

### Culture alignment — 15%

The culture score is calculated from the proportion of job culture keywords that match the candidate's listed personality traits.

### Final score

The final score is calculated as:

`Final Score = (Skill Score × 0.60) + (Experience Score × 0.25) + (Culture Score × 0.15)`

The score is rounded to two decimal places. Results are sorted by descending score, with candidate names or job titles used to break ties deterministically.

## 8. Design Decisions and Trade-offs

Skill overlap receives the highest weight because matching the required skills is central to the assignment. Experience fit receives 25% to account for the job's minimum experience requirement, while culture alignment contributes 15% as an additional signal.

The scoring weights are initial design choices rather than values trained on historical hiring outcomes. Culture matching uses direct keyword comparison, which is easy to understand but may miss semantically similar words. Candidates below the minimum experience requirement are penalized rather than disqualified. Candidate availability is stored but is not included in the current score.

The matching APIs calculate rankings dynamically from candidate and job data. Although the database includes a `matches` table, the current API does not persist each calculated match in that table.

The algorithm is intended to support comparison and should not replace human judgment in recruitment decisions.

## 9. Database Design

The SQLite database contains three main tables:

- **candidates:** candidate names, skills, experience, availability, and traits.
- **jobs:** job titles, required skills, minimum experience, culture keywords, and taglines.
- **matches:** candidate-job associations, scores, and explanations.

Tables and database queries are written using handwritten SQL. Skills, traits, and job keywords are stored as JSON-encoded lists in SQLite text columns.

## 10. Testing

Run the automated matching tests:

```powershell
python -m pytest tests/test_matching.py -v
```

The test suite covers:

- Perfect skill matching.
- Generation of match explanations.
- Candidate ranking.
- Job ranking.
- Match score range validation.

The matching test suite was executed successfully, with **5 tests passing**.

## 11. SQL Detective Challenge

The `sql_detective.sql` file contains five queries based on the separate hiring-operations dataset supplied with the assignment.

The queries cover:

1. Open job postings and their recruiters.
2. Applicants reaching the Final interview stage for each job.
3. People who applied to multiple jobs, accounting for case differences in email addresses.
4. Final-stage conversion rates for recruiters with at least three Final interviews.
5. Recruiters with the most successful Final-stage placements per department, using a window function.

The queries were validated against the supplied challenge data using a separate SQLite test database.

**Interpretation note:** The challenge schema does not contain a separate applications table. For Question 3, interview records are used to infer which jobs a person applied to.

## 12. Learning and Development

Working on this project helped me connect backend development concepts with a practical use case. I gained hands-on experience with Flask routes, relational database design, handwritten SQL, database seeding, REST API responses, weighted scoring, error handling, and automated testing.

I also learned the importance of validating results against actual data rather than assuming a query or algorithm is correct simply because it runs. I explored trade-offs in the matching weights, experience scoring, culture matching, and ranking behavior, then tested the implementation and reviewed the results.

This project strengthened my understanding of how backend components work together and why explainability, testing, and clear documentation matter when building a matching service.

## 13. AI Tools Usage

I used ChatGPT as an AI-assisted learning and development tool to help understand implementation options, reason about the matching algorithm, troubleshoot errors, review SQL queries, and improve documentation.

I ran the application locally, tested the API endpoints, executed the matching tests, loaded the supplied SQL challenge data, and checked the query results. I reviewed AI suggestions and tested them rather than assuming that generated code or explanations were automatically correct.

The process helped me learn more about Flask, SQL, database design, testing, and the trade-offs involved in building an explainable matching algorithm. I can discuss the implementation choices and the validation process during a technical walkthrough.

## 14. Future Improvements

- Add automated API tests for successful requests and invalid IDs.
- Persist calculated matches and refresh them when candidate or job data changes.
- Improve skill matching with normalized skill taxonomies or semantic similarity.
- Incorporate candidate availability as an optional ranking factor.
- Add pagination and filtering for larger datasets.
- Add structured logging and further input validation.

---

**Author:** CV Anusha Reddy
**Project:** RecruiterFlow Backend Developer Assignment  
**Language:** Python
