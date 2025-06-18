from django.contrib import admin

from .models import ExternalEmployee


@admin.register(ExternalEmployee)
class ExternalEmployeeAdmin(admin.ModelAdmin):
    list_display = ("epuserid", "name", "empid", "deptnm", "is_employed")
    list_filter = ("is_employed", "deptnm")
    search_fields = ("epuserid", "name", "empid", "deptnm")

