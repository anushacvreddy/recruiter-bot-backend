
import sqlite3

DATABASE_NAME = "recruiter_bot.db"


def get_connection():
    """Create a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def create_tables():
    """Create the tables required for recruiter-candidate matching."""
    connection = get_connection()

    try:
        connection.executescript("""
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                skills TEXT NOT NULL,
                experience_years INTEGER NOT NULL
                    CHECK (experience_years >= 0),
                availability TEXT NOT NULL,
                traits TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL UNIQUE,
                required_skills TEXT NOT NULL,
                min_experience INTEGER NOT NULL
                    CHECK (min_experience >= 0),
                culture_keywords TEXT NOT NULL,
                tagline TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS matches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                candidate_id INTEGER NOT NULL,
                job_id INTEGER NOT NULL,
                score REAL NOT NULL
                    CHECK (score >= 0 AND score <= 100),
                reason TEXT NOT NULL,
                UNIQUE (candidate_id, job_id),
                FOREIGN KEY (candidate_id)
                    REFERENCES candidates(id)
                    ON DELETE CASCADE,
                FOREIGN KEY (job_id)
                    REFERENCES jobs(id)
                    ON DELETE CASCADE
            );
        """)

        connection.commit()
        print("Database tables created successfully!")

    finally:
        connection.close()


def verify_data():
    """Verify the number of candidates and jobs stored in the database."""
    connection = get_connection()

    try:
        candidate_count = connection.execute(
            "SELECT COUNT(*) FROM candidates"
        ).fetchone()[0]

        job_count = connection.execute(
            "SELECT COUNT(*) FROM jobs"
        ).fetchone()[0]

        print(f"Total candidates: {candidate_count}")
        print(f"Total jobs: {job_count}")

    finally:
        connection.close()


if __name__ == "__main__":
    create_tables()
    verify_data()
