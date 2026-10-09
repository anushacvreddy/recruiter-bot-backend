
import json
from database import get_connection


CANDIDATES = [
    (1, "Sherlock H.", ["deduction", "pattern-recognition", "forensics"], 8, "Immediate", ["analytical", "blunt"]),
    (2, "Hermione G.", ["research", "time-management", "public-speaking"], 4, "2 weeks", ["detail-oriented", "overachiever"]),
    (3, "Tony S.", ["systems-design", "rapid-prototyping", "leadership"], 12, "Not looking", ["confident", "innovative"]),
    (4, "Leslie K.", ["project-management", "stakeholder-management", "public-speaking"], 6, "Immediate", ["tenacious", "organized"]),
    (5, "Ron S.", ["woodworking", "minimalism", "negotiation"], 15, "Not looking", ["stubborn", "principled"]),
    (6, "Rick S.", ["systems-design", "rapid-prototyping", "chemistry"], 20, "Immediate", ["genius", "reckless"]),
    (7, "Elle W.", ["persuasion", "research", "public-speaking"], 3, "Immediate", ["optimistic", "sharp"]),
    (8, "MacGyver", ["rapid-prototyping", "resourcefulness", "chemistry", "systems-design"], 10, "2 weeks", ["calm", "improviser"]),
    (9, "Sheldon C.", ["theoretical-analysis", "pattern-recognition", "research"], 9, "Immediate", ["rigid", "brilliant"]),
    (10, "Katniss E.", ["precision", "strategy", "crisis-management"], 5, "Immediate", ["resilient", "decisive"]),
    (11, "Michael S.", ["sales", "public-speaking", "team-building"], 11, "Not looking", ["enthusiastic", "chaotic"]),
    (12, "Olivia P.", ["crisis-management", "negotiation", "strategy", "leadership"], 13, "2 weeks", ["decisive", "intense"]),
    (13, "Ted L.", ["team-building", "optimism", "mentorship", "public-speaking"], 7, "Immediate", ["empathetic", "persistent"]),
    (14, "Miranda P.", ["leadership", "negotiation", "stakeholder-management", "precision"], 18, "Not looking", ["demanding", "decisive"]),
    (15, "Dwight S.", ["sales", "negotiation", "security", "loyalty"], 9, "Immediate", ["intense", "loyal"]),
]


JOBS = [
    (1, "Backend Detective", ["deduction", "pattern-recognition", "forensics"], 3, ["analytical", "autonomous"], "We have a bug. We have no leads. We have you."),
    (2, "Rapid Prototyping Engineer", ["rapid-prototyping", "systems-design"], 2, ["innovative", "fast-paced"], "Ship first, document never (kidding — please document)."),
    (3, "Developer Relations Lead", ["public-speaking", "research"], 2, ["energetic", "curious"], "Explain complex things to confused humans, cheerfully."),
    (4, "Engineering Manager, Chaos Team", ["team-building", "stakeholder-management", "leadership"], 5, ["empathetic", "organized"], "Herd cats. The cats are senior engineers."),
    (5, "Incident Commander", ["crisis-management", "strategy", "negotiation"], 4, ["decisive", "calm-under-pressure"], "3am page. You're the one who picks up."),
    (6, "Sales Engineer", ["sales", "public-speaking", "negotiation"], 3, ["enthusiastic", "persistent"], "Sell the vision, then go build it."),
]


def seed_database():
    connection = get_connection()

    try:
        connection.executemany(
            """
            INSERT OR IGNORE INTO candidates
            (id, name, skills, experience_years, availability, traits)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    candidate_id,
                    name,
                    json.dumps(skills),
                    experience,
                    availability,
                    json.dumps(traits),
                )
                for candidate_id, name, skills, experience, availability, traits
                in CANDIDATES
            ],
        )

        connection.executemany(
            """
            INSERT OR IGNORE INTO jobs
            (id, title, required_skills, min_experience, culture_keywords, tagline)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    job_id,
                    title,
                    json.dumps(skills),
                    min_experience,
                    json.dumps(culture),
                    tagline,
                )
                for job_id, title, skills, min_experience, culture, tagline
                in JOBS
            ],
        )

        connection.commit()
        print("Seed data inserted successfully!")
        print(f"Candidates provided: {len(CANDIDATES)}")
        print(f"Jobs provided: {len(JOBS)}")

    finally:
        connection.close()


if __name__ == "__main__":
    seed_database()
