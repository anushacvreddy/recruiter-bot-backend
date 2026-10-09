
import json


def calculate_match(candidate, job):
    """
    Calculate a candidate's match score for a job.

    Scoring:
    - Skills: 60%
    - Experience: 25%
    - Culture fit: 15%
    """

    candidate_skills = set(
        json.loads(candidate["skills"])
    )
    required_skills = set(
        json.loads(job["required_skills"])
    )

    candidate_traits = set(
        json.loads(candidate["traits"])
    )
    culture_keywords = set(
        json.loads(job["culture_keywords"])
    )

    # 1. Calculate skill match
    if required_skills:
        matched_skills = candidate_skills & required_skills
        skill_score = (
            len(matched_skills) / len(required_skills)
        ) * 100
    else:
        matched_skills = set()
        skill_score = 100

    # 2. Calculate experience fit
    candidate_experience = candidate["experience_years"]
    minimum_experience = job["min_experience"]

    if candidate_experience >= minimum_experience:
        experience_score = 100
    else:
        experience_score = (
            candidate_experience / minimum_experience
        ) * 100 if minimum_experience > 0 else 100

    # 3. Calculate culture fit
    if culture_keywords:
        matched_traits = candidate_traits & culture_keywords
        culture_score = (
            len(matched_traits) / len(culture_keywords)
        ) * 100
    else:
        matched_traits = set()
        culture_score = 100

    # 4. Calculate final weighted score
    final_score = (
        skill_score * 0.60
        + experience_score * 0.25
        + culture_score * 0.15
    )

    final_score = round(final_score, 2)

    # 5. Generate a short explanation
    reason_parts = []

    if matched_skills:
        reason_parts.append(
            "Matching skills: " + ", ".join(sorted(matched_skills))
        )
    else:
        reason_parts.append("No required skills matched")

    if candidate_experience >= minimum_experience:
        reason_parts.append(
            f"Meets experience requirement ({candidate_experience} years)"
        )
    else:
        reason_parts.append(
            f"Below experience requirement ({candidate_experience} years; "
            f"{minimum_experience} required)"
        )

    if matched_traits:
        reason_parts.append(
            "Culture alignment: " + ", ".join(sorted(matched_traits))
        )

    reason = "; ".join(reason_parts)

    return {
        "score": final_score,
        "reason": reason,
        "matched_skills": sorted(matched_skills),
        "skill_score": round(skill_score, 2),
        "experience_score": round(experience_score, 2),
        "culture_score": round(culture_score, 2),
    }


def rank_candidates(candidates, job):
    """Return candidates ranked from highest to lowest match score."""

    ranked_candidates = []

    for candidate in candidates:
        result = calculate_match(candidate, job)

        ranked_candidates.append({
            "candidate_id": candidate["id"],
            "candidate_name": candidate["name"],
            **result,
        })

    ranked_candidates.sort(
        key=lambda item: (
            -item["score"],
            item["candidate_name"].lower(),
        )
    )

    return ranked_candidates


def rank_jobs(candidate, jobs):
    """Return jobs ranked from highest to lowest match score."""

    ranked_jobs = []

    for job in jobs:
        result = calculate_match(candidate, job)

        ranked_jobs.append({
            "job_id": job["id"],
            "job_title": job["title"],
            **result,
        })

    ranked_jobs.sort(
        key=lambda item: (
            -item["score"],
            item["job_title"].lower(),
        )
    )

    return ranked_jobs
