# shop/tests.py
from django.test import TestCase
from .models import Product, Category


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Shirts")
        self.product = Product.objects.create(
            name="Classic Shirt",
            model_name="CSH001",
            color="White",
            price=50.00,
            stock=10,
            category=self.category
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Classic Shirt")
        self.assertEqual(self.product.category.name, "Shirts")
        self.assertEqual(self.product.price, 50.00)
        self.assertEqual(str(self.product), "Classic Shirt (White)")




    