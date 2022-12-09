from rest_framework import serializers
from .models import Product, Customer, Seller, Sale, ItemSale
from .custom_mixins import CUDNestedMixin


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


class ReadItemSaleSerializer(serializers.ModelSerializer):

    product = ProductSerializer(read_only=True)

    class Meta:
        model = ItemSale
        exclude = ['sale']


class ReadSaleSerializer(serializers.ModelSerializer):

    items = ReadItemSaleSerializer(many=True, source='itemsale_set')
    seller = SellerSerializer(read_only=True)
    customer = CustomerSerializer(read_only=True)

    class Meta:
        model = Sale
        fields = '__all__'


class WriteItemSaleSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    sale = serializers.PrimaryKeyRelatedField(
        required=False, queryset=Sale.objects.all())

    class Meta:
        model = ItemSale
        fields = '__all__'


class WriteSaleSerializer(serializers.ModelSerializer, CUDNestedMixin):

    items = WriteItemSaleSerializer(many=True, source='itemsale_set')

    class Meta:
        model = Sale
        fields = '__all__'

    def create(self, validated_data):

        if 'itemsale_set' in validated_data:
            items_data = self.initial_data['items']
            validated_data.pop('itemsale_set')

        sale = Sale.objects.create(**validated_data)

        self.cud_nested(
            queryset=sale.itemsale_set.all(),
            data=items_data,
            serializer=WriteItemSaleSerializer,
            context=self.context,
            related={'sale': sale.id}
        )

        return sale

    def update(self, instance, validated_data):

        instance.invoice = validated_data.get('invoice', instance.invoice)
        instance.sale_datetime = validated_data.get(
            'sale_datetime', instance.invoice)
        instance.seller = validated_data.get('seller', instance.seller)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.save()

        self.cud_nested(
            queryset=instance.itemsale_set.all(),
            data=self.initial_data["items"],
            serializer=WriteItemSaleSerializer,
            context=self.context,
            related={'sale': instance.id}
        )

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


class SellerCommissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = ['id', 'name']
