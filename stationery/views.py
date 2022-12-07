from django.shortcuts import render
from django.db.models import Q
from .serializers import ProductSerializer, CustomerSerializer, SellerSerializer
from rest_framework import viewsets
from .models import Product, Customer, Seller
from functools import reduce


class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductSerializer

    # Override get_queryset for filtering purpose
    def get_queryset(self):
        queryset = Product.objects.all()
        search = self.request.query_params.get('description', None)
        if search:
            queryset = queryset.filter(reduce(lambda x, y: x & y, [Q(
                description__icontains=word) for word in search.split(' ')]))
        return queryset


class CustomerViewSet(viewsets.ModelViewSet):

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class SellerViewSet(viewsets.ModelViewSet):

    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
