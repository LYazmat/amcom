# Generated by Django 3.2.16 on 2022-12-07 11:13

import datetime
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stationery', '0013_auto_20221207_0802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultcomission',
            name='min_comission',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=4, verbose_name='Comissão mínima'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='sale_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 7, 8, 13, 22, 751508), verbose_name='Data e Hora da Venda'),
        ),
    ]
