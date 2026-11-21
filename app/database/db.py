
import sqlite3
import json
from pathlib import Path
from datetime import datetime, timezone


# Store the database inside the project's data folder
DB_PATH = Path(__file__).resolve().parents[2] / "data" / "cynbit.db"


def get_connection():
    """Create and return a database connection."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():
    """Create the PR analysis table if it does not exist."""

    connection = get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS pr_analyses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                files_changed INTEGER NOT NULL,
                lines_added INTEGER NOT NULL,
                lines_deleted INTEGER NOT NULL,
                code TEXT NOT NULL,
                question TEXT,
                risk_level TEXT,
                issue_count INTEGER,
                report_json TEXT NOT NULL
            )
        """)

        connection.commit()

    finally:
        connection.close()


def save_pr_analysis(
    code,
    files_changed,
    lines_added,
    lines_deleted,
    question,
    result
):
    """Save one completed PR analysis."""

    risk_analysis = result.get("risk_analysis", {})
    static_analysis = result.get("static_analysis", {})

    risk_level = risk_analysis.get("predicted_risk", "Unavailable")
    issue_count = static_analysis.get("total_issues", 0)

    connection = get_connection()

    try:
        cursor = connection.execute("""
            INSERT INTO pr_analyses (
                created_at,
                files_changed,
                lines_added,
                lines_deleted,
                code,
                question,
                risk_level,
                issue_count,
                report_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now(timezone.utc).isoformat(),
            files_changed,
            lines_added,
            lines_deleted,
            code,
            question,
            risk_level,
            issue_count,
            json.dumps(result)
        ))

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


def get_pr_analyses(limit=100):
    """Retrieve the most recent PR analyses."""

    connection = get_connection()

    try:
        rows = connection.execute("""
            SELECT *
            FROM pr_analyses
            ORDER BY id DESC
            LIMIT ?
        """, (limit,)).fetchall()

        analyses = []

        for row in rows:
            analysis = dict(row)
            analysis["report"] = json.loads(
                analysis.pop("report_json")
            )
            analyses.append(analysis)

        return analyses

    finally:
        connection.close()



def get_dashboard_stats():
    """Return summary statistics for the dashboard."""

    connection = get_connection()

    try:
        stats = connection.execute("""
            SELECT
                COUNT(*) AS total_analyses,
                SUM(CASE WHEN risk_level = 'High' THEN 1 ELSE 0 END)
                    AS high_risk_prs,
                COALESCE(SUM(issue_count), 0) AS total_issues
            FROM pr_analyses
        """).fetchone()

        return {
            "total_analyses": stats["total_analyses"],
            "high_risk_prs": stats["high_risk_prs"],
            "total_issues": stats["total_issues"]
        }

    finally:
        connection.close()
