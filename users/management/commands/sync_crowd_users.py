from django.core.management.base import BaseCommand

from users.crowd import CrowdClient
from users.models import ExternalEmployee


class Command(BaseCommand):
    help = "Deactivate Crowd users not found in external database"

    def handle(self, *args, **options):
        client = CrowdClient()
        active_users = set(client.list_active_users())
        known_users = set(
            ExternalEmployee.objects.filter(is_employed=True).values_list("epuserid", flat=True)
        )
        to_disable = active_users - known_users
        for username in to_disable:
            self.stdout.write(f"Deactivating {username}")
            try:
                client.deactivate_user(username)
            except Exception as exc:  # pragma: no cover - logging only
                self.stderr.write(f"Failed to deactivate {username}: {exc}")
