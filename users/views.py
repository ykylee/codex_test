from django.shortcuts import render

from .crowd import CrowdClient
from .external_db import list_employees


def external_employees_view(request):
    """Display employees from the external database."""
    employees = list_employees()
    context = {"employees": employees}
    return render(request, "users/external_employees.html", context)


def crowd_users_view(request):
    """Show Crowd users and whether they exist in the external DB."""
    client = CrowdClient()
    try:
        active_users = list(client.list_active_users())
    except Exception as exc:
        active_users = []
        error = str(exc)
    else:
        error = None

    employees = {emp["username"]: emp for emp in list_employees()}
    users = []
    for username in active_users:
        employed = employees.get(username, {}).get("is_employed", False)
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
        emp["in_crowd"] = emp["username"] in active_users

    context = {"employees": employees, "error": error}
    return render(request, "users/comparison.html", context)
