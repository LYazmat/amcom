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

    product_detail = ProductSerializer(read_only=True, source='product')
    sale = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = ItemSale
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):

    items = ItemSaleSerializer(many=True, source='itemsale_set')
    seller_detail = SellerSerializer(read_only=True, source='seller')
    customer_detail = CustomerSerializer(read_only=True, source='customer')

    class Meta:
        model = Sale
        fields = '__all__'

    def create(self, validated_data):
        items_data = []
        if 'itemsale_set' in validated_data:
            items_data = validated_data.pop('itemsale_set')
        sale = Sale.objects.create(**validated_data)
        for item_data in items_data:
            ItemSale.objects.create(sale=sale, **item_data)
        return sale

    def update(self, instance, validated_data):

        items = validated_data.pop('itemsale_set', None)
        instance.invoice = validated_data.get('invoice', instance.invoice)
        instance.sale_datetime = validated_data.get(
            'sale_datetime', instance.invoice)
        instance.seller = validated_data.get('seller', instance.seller)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.save()

        items_id = []
        if items is not None:
            for item in items:
                item_sale = ItemSale.objects.filter(id=item.get('id')).first()
                if item_sale:
                    item_sale.amount = item.get('amount', item_sale.amount)
                    item_sale.product = item.get('product', item_sale.product)
                    item_sale.save()
                else:
                    item_sale = ItemSale.objects.create(sale=instance, amount=item.get(
                        'amount', 0), product=item.get('product', None))

                items_id.append(item_sale.id)
            ItemSale.objects.filter(sale=instance).exclude(
                id__in=items_id).delete()

        return instance

    def validate_items(self, value):
        if len(value) < 1:
            raise serializers.ValidationError(
                "Venda deve ter pelo menos 1 produto.")
        return value

    def to_internal_value(self, data):
        if 'items' in data:
            if not isinstance(data.get('items', []), list):
                raise serializers.ValidationError({
                    'items': [f'Espera-se uma lista, recebido tipo {type(data.get("items")).__name__}']
                })
        return super().to_internal_value(data)
