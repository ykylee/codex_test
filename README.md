# User Management Example

This project is a minimal Django application that compares employees from an external database with the active users in Atlassian Crowd.

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
```

## Running

```bash
# Listen on all network interfaces so the site is reachable from other machines
python manage.py runserver 0.0.0.0:8000
```

Visit `/compare/` to view the comparison table.
Additional pages:

- `/employees/` shows the list of external employees.
- `/crowd_users/` lists active Crowd users along with employment status.

## Synchronizing Crowd Users

The `sync_crowd_users` management command disables Crowd accounts that are not present in the external database:

```bash
python manage.py sync_crowd_users
```

## Testing with coverage

```bash
pip install coverage
coverage run manage.py test
coverage report
```
