# Generated by Django 3.2.3 on 2021-06-03 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShopCore', '0013_auto_20210603_1445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(verbose_name='Дата оформления заказа'),
        ),
    ]
