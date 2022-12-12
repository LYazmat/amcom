from django.db import models
from decimal import Decimal
from datetime import datetime
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validator_range_commission(value):
    # Method to validate comission range 0|-|10

    if not (Decimal('0.00') <= value <= Decimal('10.00')):
        raise ValidationError(f'A comissão deve ser entre 0,00 e 10,00.')


class Product(models.Model):
    # Products model

    code = models.CharField('Código', max_length=30)
    description = models.CharField('Descrição', max_length=150)
    price = models.DecimalField(
        'Valor Unitário', decimal_places=2, max_digits=30)

    commission = models.DecimalField('Percentual de comissão', decimal_places=2, max_digits=4,
                                     validators=[validator_range_commission])

    created_at = models.DateTimeField('Criado em (UTC)', auto_now_add=True)
    updated_at = models.DateTimeField('Alterado em (UTC)', auto_now=True)

    def __str__(self):
        return f'{self.description} - {self.code }'

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'


class Person(models.Model):
    # Customer and Seller models have same fields
    # thus, using Person model as Abstract model for both

    name = models.CharField('Nome', max_length=150)
    email = models.EmailField('E-mail', max_length=100)
    phone_number = models.IntegerField('Telefone')
    created_at = models.DateTimeField('Criado em (UTC)', auto_now_add=True)
    updated_at = models.DateTimeField('Alterado em (UTC)', auto_now=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        abstract = True


class Customer(Person):
    # Customers model
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'


class Seller(Person):
    # Sellers model
    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'


class DefaultCommission(models.Model):
    # Default weekdays commission model
    # Isoformat weekday: 1 - Monday to 7 - Sunday

    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    ISOWEEKDAYS_CHOICES = [
        (MONDAY, 'Segunda-Feira'),
        (TUESDAY, 'Terça-Feira'),
        (WEDNESDAY, 'Quarta-Feira'),
        (THURSDAY, 'Quinta-Feira'),
        (FRIDAY, 'Sexta-Feira'),
        (SATURDAY, 'Sábado'),
        (SUNDAY, 'Domingo'),
    ]

    day = models.IntegerField(
        'Dia da semana', primary_key=True, choices=ISOWEEKDAYS_CHOICES)

    # Commission range 0|-|10 for min and max values
    min_commission = models.DecimalField(
        'Comissão mínima', decimal_places=2, max_digits=4, default=Decimal('0.00'), validators=[validator_range_commission])
    max_commission = models.DecimalField(
        'Comissão máxima', decimal_places=2, max_digits=4, default=Decimal('10.00'), validators=[validator_range_commission])

    created_at = models.DateTimeField('Criado em (UTC)', auto_now_add=True)
    updated_at = models.DateTimeField('Alterado em (UTC)', auto_now=True)

    def __str__(self) -> str:
        return f'{self.get_day_display()}: {self.min_commission}% - {self.max_commission}%'

    # Overrides clean() and save() methods
    # max_commission must be bigger or equal than min_commission
    def clean(self):
        super(DefaultCommission, self).clean()
        if self.min_commission > self.max_commission:
            raise ValidationError({'min_commission': _(
                'Comissão mínima não pode ser maior que comissão máxima do dia.')})

    # Forces clean() method on save()
    def save(self, **kwargs):
        self.clean()
        return super(DefaultCommission, self).save(**kwargs)

    class Meta:
        verbose_name = 'Comissão Padrão'
        verbose_name_plural = 'Comissões Padrões'
        ordering = ['day']


class Sale(models.Model):
    # Sales model

    invoice = models.CharField('Nota Fiscal', max_length=100)
    sale_datetime = models.DateTimeField(
        'Data e Hora da Venda', default=datetime.today)
    customer = models.ForeignKey(to=Customer, on_delete=models.PROTECT)
    seller = models.ForeignKey(to=Seller, on_delete=models.PROTECT)

    # items = products list, n-n relationship throught model Item
    items = models.ManyToManyField(
        to=Product, through='ItemSale', related_name='sales')

    created_at = models.DateTimeField('Criado em (UTC)', auto_now_add=True)
    updated_at = models.DateTimeField('Alterado em (UTC)', auto_now=True)

    def __str__(self):
        return f'{self.invoice} - {self.sale_datetime} - {self.customer} - {self.seller}'

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'


class ItemSale(models.Model):
    # Sale itens model

    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    amount = models.IntegerField(
        'Quantidade', validators=[MinValueValidator(1)])
    created_at = models.DateTimeField('Criado em (UTC)', auto_now_add=True)
    updated_at = models.DateTimeField('Alterado em (UTC)', auto_now=True)

    def __str__(self) -> str:
        return f'{self.product} - {self.sale}'

    @property
    def total_price(self):
        return self.amount * self.product.price

    class Meta:
        verbose_name = 'Item da Venda'
        verbose_name_plural = 'Itens de Vendas'
