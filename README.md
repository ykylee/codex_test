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

## Table Style Example

The comparison table uses a small CSS file at `users/static/users/table.css` to
improve readability. Below is a sample of how the table renders:

| Username | Full name | Employed | In Crowd |
| -------- | --------- | -------- | -------- |
| alice    | Alice     | True     | Yes      |
| bob      | Bob       | False    | No       |
