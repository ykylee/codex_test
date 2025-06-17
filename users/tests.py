from django.test import Client, TestCase

from .models import ExternalEmployee


class ComparisonViewTests(TestCase):
    def setUp(self):
        ExternalEmployee.objects.create(username="alice", full_name="Alice", is_employed=True)

    def test_comparison_view(self):
        client = Client()
        response = client.get("/compare/")
        self.assertEqual(response.status_code, 200)
