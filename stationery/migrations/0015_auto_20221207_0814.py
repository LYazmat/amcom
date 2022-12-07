# Generated by Django 3.2.16 on 2022-12-07 11:14

import datetime
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stationery', '0014_auto_20221207_0813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultcomission',
            name='max_comission',
            field=models.DecimalField(decimal_places=2, default=Decimal('10.00'), max_digits=4, verbose_name='Comissão máxima'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='sale_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 7, 8, 14, 20, 497848), verbose_name='Data e Hora da Venda'),
        ),
    ]