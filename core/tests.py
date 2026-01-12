from django.test import TestCase, Client
from django.urls import reverse


class SmokeTests(TestCase):
    """
    Minimal smoke tests to ensure the app boots
    and core pages exist.
    """

    def setUp(self):
        self.client = Client()

    def test_index_page(self):
        response = self.client.get(reverse("pylab"))
        self.assertIn(response.status_code, [200, 302])

    def test_signup_page(self):
        response = self.client.get(reverse("signup"))
        self.assertIn(response.status_code, [200, 302])

    def test_signin_page(self):
        response = self.client.get(reverse("signin"))
        self.assertIn(response.status_code, [200, 302])

    def test_courses_page(self):
        response = self.client.get(reverse("courses"))
        self.assertIn(response.status_code, [200, 302])

    def test_home_page(self):
        response = self.client.get(reverse("home"))
        self.assertIn(response.status_code, [200, 302])


class SystemHealthTest(TestCase):
    """
    Ensures Django test runner and database work.
    """

    def test_system_health(self):
        self.assertTrue(True)
