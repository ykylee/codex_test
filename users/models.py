from django.db import models


class ExternalEmployee(models.Model):
    """Represents an employee record from the company directory."""

    empid = models.CharField(max_length=20, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    enlstnm = models.CharField(max_length=255, blank=True, null=True)
    enfstnm = models.CharField(max_length=255, blank=True, null=True)
    bicd = models.CharField(max_length=10, blank=True, null=True)
    binm = models.CharField(max_length=255, blank=True, null=True)
    deptcd = models.CharField(max_length=10, blank=True, null=True)
    deptnm = models.CharField(max_length=255, blank=True, null=True)
    jobgrdcd = models.CharField(max_length=10, blank=True, null=True)
    jobgrdnm = models.CharField(max_length=255, blank=True, null=True)
    frcd = models.CharField(max_length=10, blank=True, null=True)
    frnm = models.CharField(max_length=255, blank=True, null=True)
    frenm = models.CharField(max_length=255, blank=True, null=True)
    incumbcd = models.CharField(max_length=2, blank=True, null=True)
    pstcd = models.CharField(max_length=10, blank=True, null=True)
    epid = models.CharField(max_length=20, blank=True, null=True)
    epoffice_tel = models.CharField(max_length=20, blank=True, null=True)
    epmobile = models.CharField(max_length=20, blank=True, null=True)
    epuserid = models.CharField(max_length=150, unique=True, blank=True, null=True)
    epmail = models.CharField(max_length=255, blank=True, null=True)
    eai_dml_type = models.CharField(max_length=20, blank=True, null=True)
    eai_trans_gb = models.CharField(max_length=20, blank=True, null=True)
    eai_trans_dt = models.CharField(max_length=20, blank=True, null=True)
    is_employed = models.BooleanField(default=True)

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.epuserid or ""
