# User Management Example

This project demonstrates a simple Django application that synchronizes an external employee database with Atlassian Crowd.

## Setup

```bash
pip install django requests
python manage.py migrate
```

## Running

```bash
python manage.py runserver
```

Visit `/compare/` to view the comparison page.
