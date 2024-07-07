from django.test import TestCase
from django.urls import reverse
from .models import User, Product, Advertisement

class ProductTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.product = Product.objects.create(title='Test Product', description='Test Description', price=100.0)
        self.advertisement = Advertisement.objects.create(product=self.product, user=self.user)

    def test_product_creation(self):
        self.assertEqual(self.product.title, 'Test Product')

    def test_advertisement_creation(self):
        self.assertEqual(self.advertisement.product, self.product)
        self.assertEqual(self.advertisement.user, self.user)

    def test_advertisement_list_view(self):
        response = self.client.get(reverse('last_10_advertisements'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Product')
    
