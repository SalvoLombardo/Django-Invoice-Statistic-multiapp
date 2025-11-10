# dashboard/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Client
from shop.models import Category, Product


class CategoryProductTest(TestCase):
    def test_category_product_creation(self):
        category = Category.objects.create(name="Test Category")
        product = Product.objects.create(
            name="Test Product",
            model_name="TP-001",
            color="Blue",
            price=50.0,
            stock=10,
            category=category
        )
        self.assertEqual(product.category.name, "Test Category")
        self.assertEqual(product.price, 50.0)
        self.assertEqual(str(product), "Test Product (Blue)")


class DashboardMenuTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="admin", password="pass123")
        self.client_profile = Client.objects.create(user=self.user)
        self.client.login(username="admin", password="pass123")

    def test_dashboard_home_view(self):
        response = self.client.get(reverse("dashboard_home"))
        self.assertIn(response.status_code, [200, 302])  # 302 se redirect, 200 se accesso diretto

    def test_dashboard_atelier_menu(self):
        response = self.client.get(reverse("dashboard_atelier_menu"))
        self.assertIn(response.status_code, [200, 302])




        