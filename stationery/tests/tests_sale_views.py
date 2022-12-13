from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from ..models import Seller, Customer, Sale, ItemSale, Product
from decimal import Decimal
from django.utils import timezone


class TestViewSale(APITestCase):

    def setUp(self):
        self.client = APIClient()

        seller = Seller.objects.create(
            name='Marcus',
            email='marcus@teste.com',
            phone_number=24999454545
        )

        customer = Customer.objects.create(
            name='Lucas',
            email='lucas@teste.com',
            phone_number=24999505050
        )

        product = Product.objects.create(
            code='AN4587TYU78',
            description='Produto 1',
            price=Decimal('300.00'),
            commission=Decimal('3.2')
        )

        sale = Sale.objects.create(
            invoice='38745887',
            sale_datetime=timezone.now(),
            seller=seller,
            customer=customer
        )

        sale.items.add(product, through_defaults={'amount': 15})

    def test_sale_list_GET(self):
        '''
        Check 
        - Status code for list GET (list)
        - Length data response test, it should be 1
        '''

        url = reverse('sale-list')
        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 1)

    def test_sale_create_POST(self):
        '''
        Check 
        - Status code for list POST (create)
        - Length data response test, it should be 2
        - Invoice from object create (id=2) and data sent
        '''

        url = reverse('sale-list')
        data = {
            "invoice": "789456",
            "sale_datetime": "2022-12-06T15:24:09Z",
            "seller": 1,
            "customer": 1,
            "items": [
                {
                    "product": 1,
                    "amount": 200
                }
            ]
        }
        response = self.client.post(url, data, format='json')

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Sale.objects.count(), 2)
        self.assertEquals(Sale.objects.get(id=2).invoice, data['invoice'])

    def test_sale_retrieve_GET(self):
        '''
        Check 
        - Status code for detail GET (retrieve)
        - If exists invoice, sale_datetime, seller, customer, items
        - If invoice is 38745887
        '''

        url = reverse('sale-detail', args=[1])
        response = self.client.get(url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data.get('invoice'))
        self.assertIsNotNone(response.data.get('sale_datetime'))
        self.assertIsNotNone(response.data.get('seller'))
        self.assertIsNotNone(response.data.get('customer'))
        self.assertIsNotNone(response.data.get('items'))
        self.assertEquals(response.data.get('invoice'), '38745887')

    def test_sale_update_PUT(self):
        '''
        Check 
        - Status code for detail PUT (update)
        - If invoice and first item amoount change
        '''

        url = reverse('sale-detail', args=[1])
        data = {
            "invoice": "123456",
            "sale_datetime": "2022-12-06T15:24:09Z",
            "seller": 1,
            "customer": 1,
            "items": [
                {
                    "product": 1,
                    "amount": 100
                },
                {
                    "product": 1,
                    "amount": 50
                },
            ]
        }

        response = self.client.put(url, data, format='json')

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Sale.objects.get(id=1).invoice, data['invoice'])
        self.assertEquals(Sale.objects.get(
            id=1).itemsale_set.first().amount, data['items'][0]['amount'])

    def test_sale_destroy_PATCH(self):
        '''
        Check
        - Status code for detail DELETE (destroy)
        - If object id=1 exists  
        '''

        url = reverse('sale-detail', args=[1])
        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Sale.objects.filter(id=1).exists())
