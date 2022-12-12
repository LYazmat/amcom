from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from ..models import Seller


class TestViewSeller(APITestCase):

    def setUp(self):
        self.client = APIClient()

        Seller.objects.create(
            name='Marcus',
            email='marcus@teste.com',
            phone_number=24999454545
        )

    def test_seller_list_GET(self):
        # Check status code for list GET (list)
        # Check length data response test, it should be 1

        url = reverse('seller-list')
        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)

    def test_seller_create_POST(self):
        '''
        Check status code for list POST (create)
        Check length data response test, it should be 1
        Check name from object create (id=2) and data sent
        '''

        url = reverse('seller-list')
        data = {
            'name': 'Lucas',
            'email': 'lucas@teste.com',
            'phone_number': 24999505050
        }
        response = self.client.post(url, data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Seller.objects.count(), 2)
        self.assertEquals(Seller.objects.get(id=2).name, data['name'])

    def test_seller_retrieve_GET(self):
        '''
        Check status code for detail GET (retrieve)
        Check if exists name, email and phone_number
        Check if name is Marcus
        '''

        url = reverse('seller-detail', args=[1])
        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('name'))
        self.assertIsNotNone(response.data.get('email'))
        self.assertIsNotNone(response.data.get('phone_number'))
        self.assertEquals(response.data.get('name'), 'Marcus')

    def test_seller_update_PUT(self):
        '''
        Check tatus code for detail PUT (update)
        Check if name change      
        '''

        url = reverse('seller-detail', args=[1])
        data = {
            'name': 'Marcus PUT',
            'email': 'marcus@teste.com',
            'phone_number': 24999454545
        }

        response = self.client.put(url, data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Seller.objects.get(id=1).name, data['name'])

    def test_seller_partial_update_PATCH(self):
        '''
        Check status code for detail PATCH (partial update)
        Check if name change      
        '''

        url = reverse('seller-detail', args=[1])
        data = {
            'name': 'Marcus PUT',
            'email': 'marcus@teste.com',
            'phone_number': 24999454545
        }

        response = self.client.put(url, data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Seller.objects.get(id=1).name, data['name'])

    def test_seller_destroy_PATCH(self):
        '''
        Check status code for detail DELETE (destroy)
        Check if object id=1 exists  
        '''

        url = reverse('seller-detail', args=[1])

        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Seller.objects.filter(id=1).exists())
