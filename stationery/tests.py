from django.test import TestCase, Client
from django.urls import reverse
import json
from .models import Product, Seller, Customer, Sale


class TestViewSeller(TestCase):

    def setUp(self):
        self.client = Client()

        # Create seller object on database
        self.data = {
            'name': 'Marcus',
            'email': 'marcus@test.com',
            'phone_number': 24999454545
        }
        self.seller = Seller.objects.create(**self.data)

        # API urls for seller ModelViewSet

        # By default from django restframework DefaultRouter:
        # basaname-list => list method

        self.list_seller = reverse('seller-list')

        # basaname-detail and args=[id] => retrieve, create, update,
        # update_partial and destroy methods

        self.detail_url = reverse('seller-detail', args=[1])

    def test_seller_list_GET(self):
        # Status code for list GET (list) test
        # Length data response test, it should be 1

        response = self.client.get(self.list_seller)
        response_data = response.json()
        sellers = Seller.objects.all()

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response_data), sellers.count())
        self.assertEquals(len(response_data), 1)

    def test_seller_detail_GET(self):
        # Status code for detail GET (retrieve) test
        # Response data test
        # check if exists name, email and phone_number

        response = self.client.get(self.detail_url)
        response_data = response.json()
        seller = Seller.objects.first()

        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(response_data.get('name'))
        self.assertIsNotNone(response_data.get('email'))
        self.assertIsNotNone(response_data.get('phone_number'))

    def test_seller_detail_POST(self):
        # Status code for detail POST (create)
        # Response data create test
        # check if sellers count equals 2

        for_create = {
            'name': 'Lucas',
            'email': 'lucas@teste.com',
            'phone_number': 24999505050
        }
        response = self.client.post(self.list_seller, for_create)

        response_data = response.json()
        sellers = Seller.objects.all()

        self.assertEquals(response.status_code, 201)
        self.assertEquals(sellers.count(), 2)
