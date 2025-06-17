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
                "Alice HR",
                "Bob Sales",
                "Carol Engineering",
                "Dave Marketing",
                "Eve Finance",
                "Frank Support",
                "Grace HR",
                "Heidi Sales",
                "Ivan Engineering",
                "Judy Finance",
                "Mallory HR",
                "Niaj Sales",
                "Olivia Engineering",
                "Peggy Marketing",
                "Rupert Finance",
                "Sybil Support",
                "Trent HR",
                "Uma Sales",
                "Victor Engineering",
                "Wendy Marketing",
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
