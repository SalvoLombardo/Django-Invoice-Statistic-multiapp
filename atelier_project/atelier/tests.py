from django.test import TestCase
from django.contrib.auth.models import User
from .models import Appointment
from users.models import Client
from datetime import datetime, timedelta
from django.utils import timezone

class AppointmentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser3", password="pass123")
        self.client_profile = Client.objects.create(user=self.user)
        self.appointment = Appointment.objects.create(
            activity="Tailoring",
            date=timezone.now() + timedelta(days=1),
            duration=timedelta(hours=1),
            client=self.client_profile
        )

    def test_appointment_creation(self):
        self.assertEqual(self.appointment.activity, "Tailoring")
        self.assertFalse(self.appointment.is_completed)