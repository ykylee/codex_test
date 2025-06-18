from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

from .crowd import CrowdClient
from .external_db import list_employees


def external_employees_view(request):
    """Display employees from the external database with Crowd status."""
    employees = list_employees()
    client = CrowdClient()
    try:
        crowd_users = list(client.list_active_users())
    except Exception:
        crowd_users = []

    crowd_map = {u["username"]: u for u in crowd_users}
    for emp in employees:
        user = crowd_map.get(emp["username"])
        if user:
            if user.get("email") == emp.get("email"):
                emp["in_crowd"] = True
                emp["email_mismatch"] = False
            else:
                emp["in_crowd"] = False
                emp["email_mismatch"] = True
        else:
            emp["in_crowd"] = False
            emp["email_mismatch"] = False

    paginator = Paginator(employees, 20)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {"employees": page_obj}
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

    employees_map = {emp["username"]: emp for emp in list_employees()}
    users = []
    for user in active_users:
        username = user.get("username")
        emp = employees_map.get(username)
        employed = emp.get("is_employed", False) if emp else False
        emp_id = emp.get("employee_id") if emp else None
        users.append({"username": username, "employed": employed, "employee_id": emp_id})

    paginator = Paginator(users, 20)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {"users": page_obj, "error": error}
    return render(request, "users/crowd_users.html", context)


def comparison_view(request):
    client = CrowdClient()
    try:
        active_users = list(client.list_active_users())
    except Exception as exc:
        active_users = []
        error = str(exc)
    else:
        error = None

    crowd_map = {u["username"]: u for u in active_users}
    employees = list_employees()
    for emp in employees:
        user = crowd_map.get(emp["username"])
        emp["in_crowd"] = bool(user and user.get("email") == emp.get("email"))

    paginator = Paginator(employees, 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    context = {"employees": page_obj, "error": error}
    return render(request, "users/comparison.html", context)


def employee_detail_view(request, employee_id: str):
    """Display information for a single employee."""
    employees = list_employees()
    employee = next((e for e in employees if e.get("employee_id") == employee_id), None)
    if not employee:
        raise Http404("Employee not found")

    client = CrowdClient()
    try:
        crowd = {u["username"]: u for u in client.list_active_users()}
    except Exception:
        crowd = {}
    user = crowd.get(employee.get("username"))
    in_crowd = bool(user and user.get("email") == employee.get("email"))

    employee["in_crowd"] = in_crowd
    context = {"employee": employee}
    return render(request, "users/employee_detail.html", context)


def search_employees(request):
    """Return employee records matching a query for the navbar search box."""
    query = request.GET.get("q", "").lower()
    results = []
    if query:
        for emp in list_employees():
            if query in emp.get("full_name", "").lower() or query in emp.get("username", "").lower():
                results.append(
                    {
                        "employee_id": emp.get("employee_id"),
                        "full_name": emp.get("full_name"),
                        "department": emp.get("department"),
                    }
                )
            if len(results) >= 5:
                break
    return JsonResponse({"results": results})


@require_POST
def deactivate_user(request):
    """Deactivate a single Crowd user."""
    username = request.POST.get("username")
    if not username:
        return JsonResponse({"status": "error", "message": "username required"}, status=400)
    client = CrowdClient()
    try:
        client.deactivate_user(username)
    except Exception as exc:
        return JsonResponse({"status": "error", "message": str(exc)}, status=500)
    return JsonResponse({"status": "success"})


@require_POST
def deactivate_unemployed(request):
    """Deactivate Crowd accounts not marked as employed."""
    client = CrowdClient()
    employees = {emp["username"] for emp in list_employees() if emp.get("is_employed")}
    try:
        for user in client.list_active_users():
            username = user.get("username")
            if username not in employees:
                client.deactivate_user(username)
    except Exception as exc:
        return JsonResponse({"status": "error", "message": str(exc)}, status=500)
    return JsonResponse({"status": "success"})
