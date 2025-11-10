from django.test import TestCase
from django.contrib.auth.models import User
from atelier.models import Appointment
from .models import Invoice
from datetime import timedelta
from django.utils import timezone

class InvoiceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser4", password="pass123")
        self.appointment = Appointment.objects.create(
            activity="Tailoring",
            date=timezone.now() + timedelta(days=1),
            duration=timedelta(hours=1),
            client=self.user.client_profile if hasattr(self.user, 'client_profile') else None
        )
        self.invoice = Invoice.objects.create(
            user=self.user,
            appointment=self.appointment,
            document_type="INVOICE",
            amount=100
        )

    def test_invoice_creation(self):
        self.assertEqual(self.invoice.user.username, "testuser4")
        self.assertEqual(self.invoice.amount, 100)
        self.assertEqual(self.invoice.document_type, "INVOICE")