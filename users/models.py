from django.db import models


class ExternalEmployee(models.Model):
    """Represents an employee record from an external database."""

    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=255, blank=True)
    employee_id = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    is_employed = models.BooleanField(default=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.username

