from django.shortcuts import render
from rest_framework.response import Response
from django.db.models import Q
from .serializers import ProductSerializer, CustomerSerializer, SellerSerializer, ReadSaleSerializer, WriteSaleSerializer, SellerCommissionSerializer
from rest_framework import viewsets, mixins
from .models import Product, Customer, Seller, Sale, DefaultCommission
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


class SaleViewSet(viewsets.ModelViewSet):

    queryset = Sale.objects.all().prefetch_related(
        'itemsale_set__product', 'seller', 'customer')
    http_method_names = ['get', 'post', 'put', 'delete']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'destroy']:
            return WriteSaleSerializer
        return ReadSaleSerializer


class SellerCommissionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):

    serializer_class = SellerCommissionSerializer
    queryset = Seller.objects.all().prefetch_related(
        'sale_set__itemsale_set__product')
