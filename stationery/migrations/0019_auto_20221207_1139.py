# Generated by Django 3.2.16 on 2022-12-07 14:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stationery', '0018_auto_20221207_1134'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='defaultcommission',
            options={},
        ),
        migrations.RemoveConstraint(
            model_name='defaultcommission',
            name='Valor deve ser estar entre 0 e 10',
        ),
        migrations.AlterField(
            model_name='sale',
            name='sale_datetime',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 7, 11, 39, 41, 423549), verbose_name='Data e Hora da Venda'),
        ),
    ]
