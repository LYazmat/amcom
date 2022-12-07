from rest_framework import serializers
from .models import Product, Customer, Seller, Sale, ItemSale


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = '__all__'


class SellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = '__all__'


class ItemSaleSerializer(serializers.ModelSerializer):

    product = ProductSerializer()

    class Meta:
        model = ItemSale
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):

    seller = SellerSerializer()
    customer = CustomerSerializer()
    items = ItemSaleSerializer(many=True, source='itemsale_set')

    class Meta:
        model = Sale
        fields = '__all__'
