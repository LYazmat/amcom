# Generated by Django 3.2.16 on 2022-12-07 21:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stationery', '0023_alter_sale_sale_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='sale_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 7, 18, 34, 43, 691527), verbose_name='Data e Hora da Venda'),
        ),
    ]