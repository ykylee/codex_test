from django.shortcuts import render

from .crowd import CrowdClient
from .models import ExternalEmployee


def comparison_view(request):
    client = CrowdClient()
    try:
        active_users = set(client.list_active_users())
    except Exception as exc:
        active_users = set()
        error = str(exc)
    else:
        error = None
    employees = ExternalEmployee.objects.all()
    context = {
        "employees": employees,
        "active_users": active_users,
        "error": error,
    }
    return render(request, "users/comparison.html", context)

