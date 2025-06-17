from django.test import Client, TestCase


class ComparisonViewTests(TestCase):
    def test_comparison_view(self):
        client = Client()
        response = client.get("/compare/")
        self.assertEqual(response.status_code, 200)


class ExternalEmployeesViewTests(TestCase):
    def test_employees_view(self):
        client = Client()
        response = client.get("/employees/")
        self.assertEqual(response.status_code, 200)


class CrowdUsersViewTests(TestCase):
    def test_crowd_users_view(self):
        client = Client()
        response = client.get("/crowd_users/")
        self.assertEqual(response.status_code, 200)
