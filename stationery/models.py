from django.db import models
from decimal import Decimal
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


# Products model
# commission range 0-10
class Product(models.Model):
    code = models.CharField('Código', max_length=30)
    description = models.CharField('Descrição', max_length=150)
    price = models.DecimalField(
        'Valor Unitário', decimal_places=2, max_digits=30)
    commission = models.DecimalField('Percentual de comissão', decimal_places=2, max_digits=4,
                                     validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('10.00'))])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.description} - {self.code }'

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'


# Customers model
class Customer(models.Model):
    name = models.CharField('Nome', max_length=150)
    email = models.EmailField('E-mail', max_length=100)
    telefone = models.IntegerField('Telefone')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


# Customers model
class Seller(models.Model):
    name = models.CharField('Nome', max_length=150)
    email = models.EmailField('E-mail', max_length=100)
    telefone = models.IntegerField('Telefone')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'


# Sales model
# items = products list, n-n relationship throught model Item
class Sale(models.Model):
    invoice = models.CharField('Nota Fiscal', max_length=100)
    sale_datetime = models.DateTimeField(
        'Data e Hora da Venda', default=datetime.today())
    customer = models.ForeignKey(to=Customer, on_delete=models.PROTECT)
    seller = models.ForeignKey(to=Seller, on_delete=models.PROTECT)
    items = models.ManyToManyField(to=Product, through='Item')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.invoice} - {self.sale_datetime} - {self.customer} - {self.seller}'

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'


# Sale itens model
class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    amount = models.IntegerField('Quantidade')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.product} - {self.sale}'

    @property
    def total_price(self):
        return self.sale * self.product.price

    class Meta:
        verbose_name = 'Item da Venda'
        verbose_name_plural = 'Itens da(s) Venda(s)'


# Default weekdays commission
# 0 - Monday to 6 - Sunday
class DefaultComission(models.Model):
    day = models.IntegerField(primary_key=True,
                              validators=[MinValueValidator(0), MaxValueValidator(Decimal(6))])
    name = models.CharField('Dia da Semana', max_length=20)
    min_comission = models.DecimalField(
        'Comissão mínima', decimal_places=2, max_digits=4)
    max_comission = models.DecimalField(
        'Comissão máxima', decimal_places=2, max_digits=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.name}: {self.min_comission}% - {self.max_comission}%'

    # Overriding clean() and save() methods
    # max_commission must be bigegr or equal than min_commission

    def clean(self):
        super(DefaultComission, self).clean()
        if self.min_comission > self.max_comission:
            raise ValidationError({'min_comission': _(
                'Comissão mínima não pode ser maior que comissão máxima do dia.')})

    # Forces clean() method on save()
    def save(self, **kwargs):
        self.clean()
        return super(DefaultComission, self).save(**kwargs)

    class Meta:
        verbose_name = 'Comissão Padrão'
        verbose_name_plural = 'Comissões Padrões'
