from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from atelier.models import Appointment
from users.models import Client
from .models import Invoice
from django.utils import timezone
from datetime import timedelta


class InvoiceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser4", password="pass123")
        self.client_profile = Client.objects.create(user=self.user)
        self.appointment = Appointment.objects.create(
            activity="Tailoring",
            date=timezone.now() + timedelta(days=1),
            duration=timedelta(hours=1),
            client=self.client_profile
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

    def test_invoice_pdf_generation(self):
        response = self.invoice.generate_pdf()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")


class InvoiceViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser5", password="pass123")
        self.client_profile = Client.objects.create(user=self.user)
        self.appointment = Appointment.objects.create(
            activity="Tailoring",
            date=timezone.now() + timedelta(days=1),
            duration=timedelta(hours=1),
            client=self.client_profile
        )
        self.invoice = Invoice.objects.create(
            user=self.user,
            appointment=self.appointment,
            document_type="INVOICE",
            amount=50
        )
        self.client.login(username="testuser5", password="pass123")

    def test_download_invoice_pdf_view(self):
        url = reverse("download_invoice_pdf", args=[self.invoice.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")