# Generated by Django 3.2.16 on 2022-12-07 14:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stationery', '0020_auto_20221207_1148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='sale_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 7, 11, 51, 19, 338441), verbose_name='Data e Hora da Venda'),
        ),
    ]
