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
        userid = name.lower()
        email = f"{userid}@example.com"
        data.append(
            {
                "empid": f"E{idx:03d}",
                "name": name,
                "enlstnm": name,
                "enfstnm": name,
                "bicd": "B1",
                "binm": "HQ",
                "deptcd": f"D{idx%3+1}",
                "deptnm": dept,
                "jobgrdcd": "J1",
                "jobgrdnm": "Staff",
                "frcd": "F1",
                "frnm": "Engineer",
                "frenm": "Engineer",
                "incumbcd": "AA",
                "pstcd": "P1",
                "epid": f"ID{idx:03d}",
                "epoffice_tel": f"02-0000-{idx:04d}",
                "epmobile": f"010-0000-{idx:04d}",
                "epuserid": userid,
                "epmail": email,
                "eai_dml_type": "",
                "eai_trans_gb": "",
                "eai_trans_dt": "",
            }
        )
    for emp in data:
        emp["is_employed"] = emp.get("incumbcd") == "AA"
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
            "SELECT empid, name, enlstnm, enfstnm, bicd, binm, deptcd, deptnm, jobgrdcd, jobgrdnm, frcd, frnm, frenm, incumbcd, pstcd, epid, epoffice_tel, epmobile, epuserid, epmail, eai_dml_type, eai_trans_gb, eai_trans_dt FROM employees"
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
    except Exception:
        return _sample_data()

    employees: List[Dict[str, object]] = []
    for row in rows:
        (empid, name, enlstnm, enfstnm, bicd, binm, deptcd, deptnm, jobgrdcd, jobgrdnm,
         frcd, frnm, frenm, incumbcd, pstcd, epid, epoffice_tel, epmobile, epuserid,
         epmail, eai_dml_type, eai_trans_gb, eai_trans_dt) = row
        employees.append(
            {
                "empid": empid,
                "name": name,
                "enlstnm": enlstnm,
                "enfstnm": enfstnm,
                "bicd": bicd,
                "binm": binm,
                "deptcd": deptcd,
                "deptnm": deptnm,
                "jobgrdcd": jobgrdcd,
                "jobgrdnm": jobgrdnm,
                "frcd": frcd,
                "frnm": frnm,
                "frenm": frenm,
                "incumbcd": incumbcd,
                "pstcd": pstcd,
                "epid": epid,
                "epoffice_tel": epoffice_tel,
                "epmobile": epmobile,
                "epuserid": epuserid,
                "epmail": epmail,
                "eai_dml_type": eai_dml_type,
                "eai_trans_gb": eai_trans_gb,
                "eai_trans_dt": eai_trans_dt,
            }
        )
    for emp in employees:
        emp["is_employed"] = emp.get("incumbcd") == "AA"
    return employees
