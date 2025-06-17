import os
from typing import List, Dict

try:
    import psycopg2
except Exception:  # pragma: no cover - optional dependency
    psycopg2 = None


def _sample_data() -> List[Dict[str, object]]:
    """Return sample employee records for development."""
    return [
        {"name": "Alice", "employee_id": "E001", "department": "HR", "is_employed": True},
        {"name": "Bob", "employee_id": "E002", "department": "Sales", "is_employed": True},
        {"name": "Carol", "employee_id": "E003", "department": "Engineering", "is_employed": True},
        {"name": "Dave", "employee_id": "E004", "department": "Marketing", "is_employed": True},
        {"name": "Eve", "employee_id": "E005", "department": "Finance", "is_employed": True},
        {"name": "Frank", "employee_id": "E006", "department": "Support", "is_employed": True},
        {"name": "Grace", "employee_id": "E007", "department": "HR", "is_employed": False},
        {"name": "Heidi", "employee_id": "E008", "department": "Sales", "is_employed": True},
        {"name": "Ivan", "employee_id": "E009", "department": "Engineering", "is_employed": False},
        {"name": "Judy", "employee_id": "E010", "department": "Finance", "is_employed": True},
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
        conn = psycopg2.connect(host=host, port=port, dbname=name, user=user, password=password)
        cur = conn.cursor()
        cur.execute(
            "SELECT name, employee_id, department, is_employed FROM employees"
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception:
        return _sample_data()

    employees = []
    for row in rows:
        employees.append(
            {
                "name": row[0],
                "employee_id": row[1],
                "department": row[2],
                "is_employed": row[3],
            }
        )
    return employees
