from django.test import TestCase
from .models import Category, Product

class CategoryProductTest(TestCase):
    def test_category_product_creation(self):
        category = Category.objects.create(name="Test Category", slug="test-category")
        product = Product.objects.create(
            name="Test Product",
            slug="test-product",
            category=category,
            price=50.0
        )
        self.assertEqual(product.category.name, "Test Category")
        self.assertEqual(product.price, 50.0)