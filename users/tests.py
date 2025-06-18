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


class EmployeeDetailViewTests(TestCase):
    def test_employee_detail_view(self):
        client = Client()
        response = client.get("/employee/E001/")
        self.assertEqual(response.status_code, 200)


class SearchEmployeesTests(TestCase):
    def test_search_results(self):
        client = Client()
        response = client.get("/search/?q=Alice")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(any("Alice" in item["full_name"] for item in data["results"]))


class DeactivateUserTests(TestCase):
    def test_deactivate_user(self):
        client = Client()
        response = client.post("/deactivate_user/", {"username": "Bob Engineering"})
        self.assertEqual(response.status_code, 200)


class DeactivateUnemployedTests(TestCase):
    def test_deactivate_unemployed(self):
        client = Client()
        response = client.post("/deactivate_unemployed/")
        self.assertEqual(response.status_code, 200)
