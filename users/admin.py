from django.contrib import admin

from .models import ExternalEmployee


@admin.register(ExternalEmployee)
class ExternalEmployeeAdmin(admin.ModelAdmin):
    list_display = ("username", "full_name", "is_employed")
    list_filter = ("is_employed",)
    search_fields = ("username", "full_name")

