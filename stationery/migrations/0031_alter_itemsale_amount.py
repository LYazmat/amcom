# Generated by Django 3.2.16 on 2022-12-09 01:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stationery', '0030_alter_itemsale_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemsale',
            name='amount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Quantidade'),
        ),
    ]