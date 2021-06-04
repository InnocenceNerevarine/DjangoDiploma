# Generated by Django 3.2.3 on 2021-06-03 11:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ShopCore', '0012_auto_20210603_0318'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Оформленный заказ', 'verbose_name_plural': 'Оформленные заказы'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'Платеж', 'verbose_name_plural': 'Платежи'},
        ),
        migrations.RemoveField(
            model_name='order',
            name='start_date',
        ),
        migrations.AddField(
            model_name='order',
            name='order_receive_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата получения'),
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered',
            field=models.BooleanField(default=False, verbose_name='Заказ оформлен'),
        ),
        migrations.AlterField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(verbose_name='Заказ оформлен'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ShopCore.payment', verbose_name='Оплатил'),
        ),
        migrations.AlterField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='ShopCore.OrderProduct', verbose_name='Товары'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Покупатель'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.IntegerField(verbose_name='Сумма'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='stripe_charge_id',
            field=models.CharField(max_length=50, verbose_name='Идентификатор платежа'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Покупатель'),
        ),
    ]
