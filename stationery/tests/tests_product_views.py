from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from ..models import Product
from decimal import Decimal


class TestViewProduct(APITestCase):

    def setUp(self):
        self.client = APIClient()

        Product.objects.create(
            code='AN4587TYU78',
            description='Produto 1',
            price=Decimal('300.00'),
            commission=Decimal('3.2')
        )

    def test_product_list_GET(self):
        '''
        Check 
        - Status code for list GET (list)
        - Length data response test, it should be 1
        '''

        url = reverse('product-list')
        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)

    def test_product_create_POST(self):
        '''
        Check 
        - Status code for list POST (create)
        - Length data response test, it should be 2
        - Description from object create (id=2) and data sent
        '''

        url = reverse('product-list')
        data = {
            'code': 'RST7898QV4VC',
            'description': 'Produto 2',
            'price': '47.25',
            'commission': '2.27',
        }
        response = self.client.post(url, data, format='json')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Product.objects.count(), 2)
        self.assertEquals(Product.objects.get(
            id=2).description, data['description'])

    def test_product_retrieve_GET(self):
        '''
        Check 
        - Status code for detail GET (retrieve)
        - If exists code, description, price and commission
        - If name is Marcus
        '''

        url = reverse('product-detail', args=[1])
        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('code'))
        self.assertIsNotNone(response.data.get('description'))
        self.assertIsNotNone(response.data.get('price'))
        self.assertIsNotNone(response.data.get('commission'))
        self.assertEquals(response.data.get('description'), 'Produto 1')

    def test_product_update_PUT(self):
        '''
        Check 
        - Status code for detail PUT (update)
        - If name change      
        '''

        url = reverse('product-detail', args=[1])
        data = {
            'code': 'RST7898QV4VC',
            'description': 'Produto 2 Teste',
            'price': '47.25',
            'commission': '2.27',
        }

        response = self.client.put(url, data, format='json')

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Product.objects.get(
            id=1).description, data['description'])

    def test_product_partial_update_PATCH(self):
        '''
        Check
        - Status code for detail PATCH (partial update)
        - If name changed   
        '''

        url = reverse('product-detail', args=[1])
        data = {
            'description': 'Product 1 PATCH',
        }

        response = self.client.patch(url, data, format='json')

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Product.objects.get(
            id=1).description, data['description'])

    def test_product_destroy_PATCH(self):
        '''
        Check
        - Status code for detail DELETE (destroy)
        - If object id=1 exists  
        '''

        url = reverse('product-detail', args=[1])
        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=1).exists())
