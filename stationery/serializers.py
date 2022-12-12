from rest_framework import serializers
from .models import Product, Customer, Seller, Sale, ItemSale, DefaultCommission
from django.db.models import Count
from .custom_mixins import CUDNestedMixin
from decimal import Decimal


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

    count = serializers.SerializerMethodField('count_sales')
    commission = serializers.SerializerMethodField('commission_sales')

    class Meta:
        model = Seller
        fields = ['id', 'name', 'count', 'commission']

    def __init__(self, *args, **kwargs):
        super(SellerCommissionSerializer, self).__init__(*args, **kwargs)

        self.weekcommision = {
            df.day: {'min': df.min_commission,
                     'max': df.max_commission}
            for df in list(DefaultCommission.objects.all())
        }

    def count_sales(self, seller):
        return seller.sale_set.count()

    def check_comission(self, isoweekday: int, item: ItemSale):

        empty_comission = {
            'min': Decimal('0.00'),
            'max': Decimal('10.00')
        }

        daycommission = self.weekcommision.get(isoweekday, empty_comission)
        applied_commission = min(daycommission.get('max'), max(
            daycommission.get('min'), item.product.commission))
        return applied_commission

    def commission_sales(self, seller):
        sales = seller.sale_set.all()

        commissions_sale = []
        for sale in sales:
            isodayweek = sale.sale_datetime.isoweekday()
            itemsales = sale.itemsale_set.all()
            for item in itemsales:
                applied_commission = self.check_comission(isodayweek, item)
                commissions_sale.append(
                    item.total_price * applied_commission / 100)
        return sum(commissions_sale)
