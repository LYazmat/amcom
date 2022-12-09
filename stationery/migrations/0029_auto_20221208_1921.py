# Generated by Django 3.2.16 on 2022-12-08 22:21

from decimal import Decimal
from django.db import migrations, models
import stationery.models


class Migration(migrations.Migration):

    dependencies = [
        ('stationery', '0028_auto_20221208_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='defaultcommission',
            name='max_commission',
            field=models.DecimalField(decimal_places=2, default=Decimal('10.00'), max_digits=4, validators=[stationery.models.validator_range_commission], verbose_name='Comissão máxima'),
        ),
        migrations.AlterField(
            model_name='defaultcommission',
            name='min_commission',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=4, validators=[stationery.models.validator_range_commission], verbose_name='Comissão mínima'),
        ),
        migrations.AlterField(
            model_name='product',
            name='commission',
            field=models.DecimalField(decimal_places=2, max_digits=4, validators=[stationery.models.validator_range_commission], verbose_name='Percentual de comissão'),
        ),
    ]
