import json
from uuid import uuid4
from datetime import (
    datetime,
    timedelta,
)
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from rest_framework import status

from products.models import Product, PriceItem


class GetPriceForPeriodViewTestCase(TestCase):
    def setUp(self) -> None:
        self.product = Product.objects.create(name='Test Product')

        PriceItem.objects.create(product=self.product, date=datetime(2024, 1, 1), price=10)
        PriceItem.objects.create(product=self.product, date=datetime(2024, 1, 2), price=20)
        PriceItem.objects.create(product=self.product, date=datetime(2024, 1, 3), price=30)

    def test_get_average_price_for_period(self):
        query_params = {'start_date': '2024-01-01', 'end_date': '2024-01-03'}
        response = self.client.get(f'/api/v1/prices/products/get-price/{self.product.id}/', query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_average_price = Decimal('20.00')
        self.assertEqual(response.data['average_price'], expected_average_price)

    def test_get_null_average_price_for_period(self):
        query_params = {'start_date': '2024-01-05', 'end_date': '2024-01-08'}
        response = self.client.get(f'/api/v1/prices/products/get-price/{self.product.id}/', query_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_average_price = None
        self.assertEqual(response.data['average_price'], expected_average_price)

    def test_invalid_date_format(self):
        query_params = {'start_date': '2024-01-01', 'end_date': '2024-01'}
        response = self.client.get(f'/api/v1/prices/products/get-price/{self.product.id}/', query_params)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid date format', response.data['error'])

    def test_no_product_found(self):
        query_params = {'start_date': '2024-01-01', 'end_date': '2024-01-03'}
        response = self.client.get(f'/api/v1/prices/products/get-price/{uuid4()}/', query_params)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('not found', response.data['error'])

    def test_end_date_before_start_date(self):
        query_params = {'start_date': '2024-01-03', 'end_date': '2024-01-01'}
        response = self.client.get(f'/api/v1/prices/products/get-price/{self.product.id}/', query_params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('End date must be after start date', response.data['error'])


class SetPriceForPeriodViewTest(TestCase):
    def setUp(self) -> None:
        self.product = Product.objects.create(name='Test Product')

    def test_set_price_for_period_success(self):
        data = {
            'product_id': str(self.product.id),
            'start_date': '2024-04-09',
            'end_date': '2024-04-10',
            'price': '10.00',
        }
        response = self.client.post(
            f'/api/v1/prices/products/set-price/',
            json.dumps(data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertAlmostEquals(self.product.price_items.count(), 2)

    def test_set_price_for_period_invalid_date(self):
        data = {
            # 'product_id': str(self.product.id),
            'start_date': '2024-04-09',
            'end_date': '2024-04-10',
            'price': '10.00',
        }
        response = self.client.post(
            f'/api/v1/prices/products/set-price/',
            json.dumps(data),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.product.price_items.count(), 0)        
