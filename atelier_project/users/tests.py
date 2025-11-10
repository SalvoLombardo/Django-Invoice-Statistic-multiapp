from django.test import TestCase
from django.contrib.auth.models import User
from .models import Client

class ClientModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.client_profile = Client.objects.create(user=self.user, role="CLIENT")

    def test_client_creation(self):
        self.assertEqual(self.client_profile.user.username, "testuser")
        self.assertEqual(self.client_profile.role, "CLIENT")

class ClientViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser2", password="pass123")
        self.client_profile = Client.objects.create(user=self.user)

    def test_client_dashboard_requires_login(self):
        response = self.client.get("/client_profile_dashboard/")
        self.assertEqual(response.status_code, 302)  # Redirect to login