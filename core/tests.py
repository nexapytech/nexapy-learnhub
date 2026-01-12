from django.test import TestCase, Client
from django.urls import reverse


class PublicPagesTests(TestCase):
    """Publicly accessible pages"""

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

    def test_community_rules_page(self):
        response = self.client.get(reverse("community_rules"))
        self.assertIn(response.status_code, [200, 302])


class ProtectedPagesSmokeTests(TestCase):
    """Pages that may require authentication"""

    def setUp(self):
        self.client = Client()

    def test_accounts_page(self):
        response = self.client.get(reverse("accounts"))
        self.assertIn(response.status_code, [200, 302, 403, 404])

    def test_notifications_page(self):
        response = self.client.get(reverse("notifications"))
        self.assertIn(response.status_code, [200, 302, 403, 404])

    def test_community_page(self):
        response = self.client.get(reverse("community"))
        self.assertIn(response.status_code, [200, 302, 403, 404])

    def test_course_enrollment_page(self):
        response = self.client.get(reverse("course_enrollment"))
        self.assertIn(response.status_code, [200, 302, 403, 404])

    def test_course_task_page(self):
        response = self.client.get(reverse("course_task"))
        self.assertIn(response.status_code, [200, 302, 403, 404])


class ActionEndpointsSmokeTests(TestCase):
    """POST/Action endpoints – ensure they exist"""

    def setUp(self):
        self.client = Client()

    def test_create_post_endpoint(self):
        response = self.client.post(reverse("create_post"))
        self.assertIn(response.status_code, [200, 302, 403, 404])

    def test_create_comment_endpoint(self):
        response = self.client.post(reverse("create_comment"))
        self.assertIn(response.status_code, [200, 302, 403, 404])

    def test_like_post_endpoint(self):
        response = self.client.post(reverse("like_post"))
        self.assertIn(response.status_code, [200, 302, 403, 404])

    def test_delete_post_endpoint(self):
        response = self.client.post(reverse("delete_post"))
        self.assertIn(response.status_code, [200, 302, 403, 404])

    def test_filter_post_endpoint(self):
        response = self.client.get(reverse("filter_post"))
        self.assertIn(response.status_code, [200, 302, 403, 404])

    def test_load_more_endpoint(self):
        response = self.client.get(reverse("loadmore"))
        self.assertIn(response.status_code, [200, 302, 403, 404])


class UrlsWithParamsTests(TestCase):
