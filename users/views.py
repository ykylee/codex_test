from django.shortcuts import render

from .crowd import CrowdClient
from .external_db import list_employees


def external_employees_view(request):
    employees = list_employees()
    context = {"employees": employees}
    return render(request, "users/external_employees.html", context)


def crowd_users_view(request):
    client = CrowdClient()
    try:
        active_users = list(client.list_active_users())
    except Exception as exc:
        active_users = []
        error = str(exc)
    else:
        error = None

    employees = {emp["name"]: emp for emp in list_employees()}
    users = []
    for username in active_users:
        name = username.split()[0]
        employed = employees.get(name, {}).get("is_employed", False)
        users.append({"username": username, "employed": employed})

    context = {"users": users, "error": error}
    return render(request, "users/crowd_users.html", context)


def comparison_view(request):
    client = CrowdClient()
    try:
        active_users = set(client.list_active_users())
    except Exception as exc:
        active_users = set()
        error = str(exc)
    else:
        error = None
    employees = list_employees()
    for emp in employees:
        username = f"{emp['name']} {emp['department']}"
        emp["in_crowd"] = username in active_users
    context = {
        "employees": employees,
        "error": error,
    }
    return render(request, "users/comparison.html", context)

