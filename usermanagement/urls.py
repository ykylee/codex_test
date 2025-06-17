"""
URL configuration for usermanagement project.
"""

from django.contrib import admin
from django.urls import path

from users.views import (
    comparison_view,
    crowd_users_view,
    employee_detail_view,
    external_employees_view,
    search_employees,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("compare/", comparison_view, name="compare"),
    path("employees/", external_employees_view, name="employees"),
    path("crowd_users/", crowd_users_view, name="crowd_users"),
    path("employee/<str:employee_id>/", employee_detail_view, name="employee_detail"),
    path("search/", search_employees, name="search_employees"),
]
