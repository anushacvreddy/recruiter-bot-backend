
import json
import pytest

from matching import calculate_match, rank_candidates, rank_jobs


@pytest.fixture
def candidate():
    return {
        "id": 1,
        "name": "Sherlock H.",
        "skills": json.dumps([
            "deduction",
            "pattern-recognition",
            "forensics",
        ]),
        "experience_years": 8,
        "availability": "Immediate",
        "traits": json.dumps(["analytical", "blunt"]),
    }


@pytest.fixture
def job():
    return {
        "id": 1,
        "title": "Backend Detective",
        "required_skills": json.dumps([
            "deduction",
            "pattern-recognition",
            "forensics",
        ]),
        "min_experience": 3,
        "culture_keywords": json.dumps([
            "analytical",
            "autonomous",
        ]),
        "tagline": "We have a bug. We have no leads. We have you.",
    }


def test_perfect_skill_match(candidate, job):
    result = calculate_match(candidate, job)

    assert result["skill_score"] == 100
    assert result["experience_score"] == 100
    assert result["culture_score"] == 50
    assert result["score"] == 92.5


def test_match_reason_is_generated(candidate, job):
    result = calculate_match(candidate, job)

    assert "Matching skills" in result["reason"]
    assert "Meets experience requirement" in result["reason"]


def test_candidate_ranking(candidate, job):
    second_candidate = {
        "id": 2,
        "name": "Other Candidate",
        "skills": json.dumps(["research"]),
        "experience_years": 1,
        "availability": "Immediate",
        "traits": json.dumps([]),
    }

    ranked = rank_candidates(
        [second_candidate, candidate],
        job,
    )

    assert ranked[0]["candidate_name"] == "Sherlock H."
    assert ranked[0]["score"] >= ranked[1]["score"]


def test_job_ranking(candidate, job):
    second_job = {
        "id": 2,
        "title": "Research Assistant",
        "required_skills": json.dumps(["research"]),
        "min_experience": 2,
        "culture_keywords": json.dumps(["curious"]),
        "tagline": "Explore new ideas.",
    }

    ranked = rank_jobs(candidate, [second_job, job])

    assert len(ranked) == 2
    assert ranked[0]["job_title"] == "Backend Detective"


def test_score_stays_within_range(candidate, job):
    result = calculate_match(candidate, job)

    assert 0 <= result["score"] <= 100

