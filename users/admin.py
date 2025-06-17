from django.contrib import admin

from .models import ExternalEmployee


@admin.register(ExternalEmployee)
class ExternalEmployeeAdmin(admin.ModelAdmin):
    list_display = ("username", "full_name", "employee_id", "department", "is_employed")
    list_filter = ("is_employed", "department")
    search_fields = ("username", "full_name", "employee_id", "department")

