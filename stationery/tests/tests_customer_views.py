from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from ..models import Customer


class TestViewCustomer(APITestCase):

    def setUp(self):
        self.client = APIClient()

        Customer.objects.create(
            name='Marcus',
            email='marcus@teste.com',
            phone_number=24999454545
        )

    def test_customer_list_GET(self):
        '''
        Check 
        - Status code for list GET (list)
        - Length data response test, it should be 1
        '''

        url = reverse('customer-list')
        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)

    def test_customer_create_POST(self):
        '''
        Check 
        - Status code for list POST (create)
        - Length data response test, it should be 1
        - Name from object create (id=2) and data sent
        '''

        url = reverse('customer-list')
        data = {
            'name': 'Lucas',
            'email': 'lucas@teste.com',
            'phone_number': 24999505050
        }
        response = self.client.post(url, data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Customer.objects.count(), 2)
        self.assertEquals(Customer.objects.get(id=2).name, data['name'])

    def test_customer_retrieve_GET(self):
        '''
        Check 
        - Status code for detail GET (retrieve)
        - If exists name, email and phone_number
        - If name is Marcus
        '''

        url = reverse('customer-detail', args=[1])
        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('name'))
        self.assertIsNotNone(response.data.get('email'))
        self.assertIsNotNone(response.data.get('phone_number'))
        self.assertEquals(response.data.get('name'), 'Marcus')

    def test_customer_update_PUT(self):
        '''
        Check 
        - Status code for detail PUT (update)
        - If name change      
        '''

        url = reverse('customer-detail', args=[1])
        data = {
            'name': 'Marcus PUT',
            'email': 'marcus@teste.com',
            'phone_number': 24999454545
        }

        response = self.client.put(url, data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Customer.objects.get(id=1).name, data['name'])

    def test_customer_partial_update_PATCH(self):
        '''
        Check
        - Status code for detail PATCH (partial update)
        - If name changed   
        '''

        url = reverse('customer-detail', args=[1])
        data = {
            'name': 'Marcus PATCH'
        }

        response = self.client.patch(url, data)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Customer.objects.get(id=1).name, data['name'])

    def test_customer_destroy_PATCH(self):
        '''
        Check
        - Status code for detail DELETE (destroy)
        - If object id=1 exists  
        '''

        url = reverse('customer-detail', args=[1])
        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Customer.objects.filter(id=1).exists())
