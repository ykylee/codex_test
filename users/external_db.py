import os
from typing import Dict, List

try:
    import psycopg2
except Exception:  # pragma: no cover - optional dependency
    psycopg2 = None


def _sample_data() -> List[Dict[str, object]]:
    """Return sample employee records for development."""
    return [
        {"username": "alice", "full_name": "Alice Doe", "is_employed": True},
        {"username": "bob", "full_name": "Bob Smith", "is_employed": True},
        {"username": "carol", "full_name": "Carol Jones", "is_employed": False},
    ]


def list_employees() -> List[Dict[str, object]]:
    """Return employee records from an external PostgreSQL DB or sample data."""
    host = os.environ.get("EXT_DB_HOST")
    name = os.environ.get("EXT_DB_NAME")
    user = os.environ.get("EXT_DB_USER")
    password = os.environ.get("EXT_DB_PASSWORD")
    port = os.environ.get("EXT_DB_PORT", "5432")

    if not (host and name and user and password and psycopg2):
        return _sample_data()

    try:
        conn = psycopg2.connect(
            host=host, port=port, dbname=name, user=user, password=password
        )
        cur = conn.cursor()
        cur.execute(
            "SELECT username, full_name, is_employed FROM employees"
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception:
        return _sample_data()

    employees: List[Dict[str, object]] = []
    for row in rows:
        employees.append(
            {
                "username": row[0],
                "full_name": row[1],
                "is_employed": row[2],
            }
        )
    return employees
