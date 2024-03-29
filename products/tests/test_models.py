from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

from ..models import Category, Product


class TestCategoryModel(TestCase):

    def create_category(self, name="test"):
        return Category.objects.create(name=name)

    def test_category_creation(self):
        c = self.create_category()
        self.assertTrue(isinstance(c, Category))
        self.assertEqual(c.__str__(), c.name)


class TestProductModel(TestCase):
    
    def setUp(self):
        self.category = Category.objects.create(name='fastfood', slug='fastfood')
        User.objects.create(username='vendor')
    
    def create_product(self, name="product"):
        return Product.objects.create(category=self.category, name=name, price='20.00', created=timezone.now(), updated=timezone.now())

    def test_product_creation(self):
        p = self.create_product()
        self.assertTrue(isinstance(p, Product))
        self.assertEqual(str(p), 'product')
