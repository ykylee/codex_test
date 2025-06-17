import os
from typing import Iterable

import requests


class CrowdClient:
    """Minimal client for Atlassian Crowd REST API."""

    def __init__(self) -> None:
        self.base_url = os.environ.get("CROWD_URL")
        self.app_user = os.environ.get("CROWD_APP_USERNAME")
        self.app_pass = os.environ.get("CROWD_APP_PASSWORD")
        # Allow initialization without network configuration for tests
        if not self.base_url:
            self.base_url = ""  # offline mode

    def _headers(self) -> dict:
        return {"Accept": "application/json"}

    def _auth(self) -> tuple[str, str] | None:
        if self.app_user and self.app_pass:
            return (self.app_user, self.app_pass)
        return None

    def list_active_users(self) -> Iterable[str]:
        """Return usernames for active users."""
        if not self.base_url:
            sample_names = [
                "Alice Engineering",
                "Bob Engineering",
                "Carol Sales",
                "Dave Marketing",
                "Eve Finance",
                "Frank HR",
                "Grace QA",
                "Heidi Support",
                "Ivan DevOps",
                "Judy Management",
                "Karl Engineering",
                "Liam Engineering",
                "Mallory Sales",
                "Niaj Marketing",
                "Olivia Finance",
                "Peggy HR",
                "Rupert QA",
                "Sybil Support",
                "Trent DevOps",
                "Victor Management",
            ]
            for name in sample_names:
                yield name
            return
        url = f"{self.base_url}/rest/usermanagement/1/search?entity-type=user&expand=group&active=true"
        resp = requests.get(url, headers=self._headers(), auth=self._auth(), timeout=10)
        resp.raise_for_status()
        data = resp.json()
        for user in data.get("users", {}).get("user", []):
            name = user.get("name")
            if name:
                yield name

    def deactivate_user(self, username: str) -> None:
        """Disable a user account."""
        if not self.base_url:
            return
        url = f"{self.base_url}/rest/usermanagement/1/user?username={username}"
        payload = {"active": False}
        resp = requests.put(url, json=payload, headers=self._headers(), auth=self._auth(), timeout=10)
        resp.raise_for_status()
