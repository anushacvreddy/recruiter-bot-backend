
from flask import Flask, jsonify
from database import get_connection, create_tables
from matching import rank_candidates, rank_jobs

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Recruiter Bot API is running",
        "endpoints": [
            "/jobs/<id>/matches",
            "/candidates/<id>/matches"
        ]
    })


@app.route("/jobs/<int:job_id>/matches", methods=["GET"])
def get_job_matches(job_id):
    """Return candidates ranked by their match for a job."""
    connection = get_connection()

    try:
        job = connection.execute(
            "SELECT * FROM jobs WHERE id = ?",
            (job_id,)
        ).fetchone()

        if job is None:
            return jsonify({"error": "Job not found"}), 404

        candidates = connection.execute(
            "SELECT * FROM candidates"
        ).fetchall()

        results = rank_candidates(candidates, job)

        return jsonify({
            "job_id": job["id"],
            "job_title": job["title"],
            "matches": results
        }), 200

    finally:
        connection.close()


@app.route("/candidates/<int:candidate_id>/matches", methods=["GET"])
def get_candidate_matches(candidate_id):
    """Return jobs ranked by their match for a candidate."""
    connection = get_connection()

    try:
        candidate = connection.execute(
            "SELECT * FROM candidates WHERE id = ?",
            (candidate_id,)
        ).fetchone()

        if candidate is None:
            return jsonify({"error": "Candidate not found"}), 404

        jobs = connection.execute(
            "SELECT * FROM jobs"
        ).fetchall()

        results = rank_jobs(candidate, jobs)

        return jsonify({
            "candidate_id": candidate["id"],
            "candidate_name": candidate["name"],
            "matches": results
        }), 200

    finally:
        connection.close()


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)
