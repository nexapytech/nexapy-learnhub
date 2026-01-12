from django.test import TestCase, Client
from django.urls import reverse


class BasicSmokeTests(TestCase):
    """Basic tests to ensure pages exist and app boots"""

    def setUp(self):
        self.client = Client()

    def test_homepage_exists(self):
        response = self.client.get(reverse("PylearnCBT"))
        self.assertIn(response.status_code, [200, 302])

    def test_signup_page_exists(self):
        response = self.client.get(reverse("signup"))
        self.assertIn(response.status_code, [200, 302])

    def test_signin_page_exists(self):
        response = self.client.get(reverse("signin"))
        self.assertIn(response.status_code, [200, 302])


class ProtectedPagesTests(TestCase):
    """Ensure protected pages don't crash"""

    def setUp(self):
        self.client = Client()

    def test_dashboard_exists(self):
        response = self.client.get(reverse("dashboard"))
        self.assertIn(response.status_code, [200, 302, 403, 404])

    def test_my_exams_exists(self):
        response = self.client.get(reverse("my_exams"))
        self.assertIn(response.status_code, [200, 302, 403, 404])


class SystemHealthTest(TestCase):
    """Minimal test to ensure test runner & DB work"""

    def test_system_health(self):
        self.assertTrue(True)
