# Generated by Django 3.2.3 on 2021-06-01 21:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ShopCore', '0003_product_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
    ]
