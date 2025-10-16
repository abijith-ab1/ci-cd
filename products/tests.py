# app/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product

class ProductAPITestCase(APITestCase):

    def setUp(self):
        # Create a sample product for testing
        self.product = Product.objects.create(
            name="Test Product",
            price=100,
            sku="TESTSKU123"
        )
        self.list_create_url = reverse('product-list-create')  # match your urls.py name

    def test_get_all_products(self):
        """Test retrieving all products"""
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('data', response.data)
        self.assertEqual(response.data['count'], 1)

    def test_create_product_with_name_and_price(self):
        """Test creating a product with name and price (SKU auto-generated)"""
        payload = {
            "name": "New Product",
            "price": 200
        }
        response = self.client.post(self.list_create_url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], payload['name'])
        self.assertEqual(float(response.data['price']), payload['price'])
        self.assertIn('sku', response.data)
        self.assertTrue(len(response.data['sku']) > 0)

    def test_get_product_by_sku(self):
        """Test retrieving a product by SKU"""
        payload = {"sku": self.product.sku}
        response = self.client.post(self.list_create_url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['sku'], self.product.sku)

    def test_patch_product(self):
        """Test partially updating a product"""
        url = reverse('product-detail', args=[self.product.id])
        payload = {"price": 150}
        response = self.client.patch(url, data=payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['price']), payload['price'])

    def test_delete_product(self):
        """Test deleting a product"""
        url = reverse('product-detail', args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())
