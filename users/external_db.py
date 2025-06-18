import os
from typing import Dict, List

try:
    import psycopg2
except Exception:  # pragma: no cover - optional dependency
    psycopg2 = None


def _sample_data() -> List[Dict[str, object]]:
    """Return sample employee records for development."""
    names = [
        ("Alice", "Engineering"),
        ("Bob", "Engineering"),
        ("Carol", "Sales"),
        ("Dave", "Marketing"),
        ("Eve", "Finance"),
        ("Frank", "HR"),
        ("Grace", "QA"),
        ("Heidi", "Support"),
        ("Ivan", "DevOps"),
        ("Judy", "Management"),
    ]
    data: List[Dict[str, object]] = []
    for idx, (name, dept) in enumerate(names, start=1):
        username = f"{name.lower()}"  # login id
        email = f"{name.lower()}@example.com"
        data.append(
            {
                "username": username,
                "full_name": name,
                "employee_id": f"E{idx:03d}",
                "department": dept,
                "is_employed": True,
                "email": email,
            }
        )
    return data


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
            "SELECT username, full_name, employee_id, department, is_employed, email FROM employees"
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
                "employee_id": row[2],
                "department": row[3],
                "is_employed": row[4],
                "email": row[5],
            }
        )
    return employees
