from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product, Category

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Shirts", slug="shirts")
        self.product = Product.objects.create(
            name="Classic Shirt",
            category=self.category,
            price=50.00,
            slug="classic-shirt"
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Classic Shirt")
        self.assertEqual(self.product.category.name, "Shirts")