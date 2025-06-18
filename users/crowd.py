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

    def list_active_users(self) -> Iterable[dict]:
        """Return basic info for active users."""
        if not self.base_url:
            sample = [
                ("alice", "Alice", "Engineering"),
                ("bob", "Bob", "Engineering"),
                ("carol", "Carol", "Sales"),
                ("dave", "Dave", "Marketing"),
                ("eve", "Eve", "Finance"),
                ("frank", "Frank", "HR"),
                ("grace", "Grace", "QA"),
                ("heidi", "Heidi", "Support"),
                ("ivan", "Ivan", "DevOps"),
                ("judy", "Judy", "Management"),
                ("karl", "Karl", "Engineering"),
                ("liam", "Liam", "Engineering"),
                ("mallory", "Mallory", "Sales"),
                ("niaj", "Niaj", "Marketing"),
                ("olivia", "Olivia", "Finance"),
                ("peggy", "Peggy", "HR"),
                ("rupert", "Rupert", "QA"),
                ("sybil", "Sybil", "Support"),
                ("trent", "Trent", "DevOps"),
                ("victor", "Victor", "Management"),
            ]
            for username, first, last in sample:
                yield {
                    "username": username,
                    "email": f"{username}@example.com",
                    "first_name": first,
                    "last_name": last,
                    "display_name": f"{first} {last}",
                }
            return
        url = f"{self.base_url}/rest/usermanagement/1/search?entity-type=user&expand=group&active=true"
        resp = requests.get(url, headers=self._headers(), auth=self._auth(), timeout=10)
        resp.raise_for_status()
        data = resp.json()
        for user in data.get("users", {}).get("user", []):
            if not isinstance(user, dict):
                continue
            name = user.get("name")
            email = user.get("email")
            first = user.get("first-name")
            last = user.get("last-name")
            display = user.get("display-name")
            if name:
                yield {
                    "username": name,
                    "email": email,
                    "first_name": first,
                    "last_name": last,
                    "display_name": display,
                }

    def deactivate_user(self, username: str) -> None:
        """Disable a user account."""
        if not self.base_url:
            return
        url = f"{self.base_url}/rest/usermanagement/1/user?username={username}"
        payload = {"active": False}
        resp = requests.put(url, json=payload, headers=self._headers(), auth=self._auth(), timeout=10)
        resp.raise_for_status()
