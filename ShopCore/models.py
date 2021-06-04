from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from autoslug import AutoSlugField
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
import decimal

User = get_user_model()


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Наименование категории')
    slug = AutoSlugField(unique=True, populate_from='name')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):

    category = models.ForeignKey(Category, verbose_name='Категория товара', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование', help_text='Введите наименование товара')
    slug = AutoSlugField(unique=True, populate_from='title')
    image = models.ImageField(verbose_name='Изображение товара', upload_to='products')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    discount_price = models.FloatField(blank=True, null=True, default=0, verbose_name='Процент скидки(в %)',
                                       validators=[MinValueValidator(0), MaxValueValidator(100)])
    is_active = models.BooleanField(default=True, verbose_name='Наличие')
    updated = models.DateTimeField(auto_now=True, verbose_name='Изменён')

    class Meta:
        verbose_name = f'Товар'
        verbose_name_plural = f'Товары'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    def get_discount_price(self):
        return self.price - (self.price / 100 * decimal.Decimal(self.discount_price))


class Contact(models.Model):

    email = models.EmailField(verbose_name='Почта')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = f'Подписку на рассылку'
        verbose_name_plural = f'Подписки на рассылку'


class Commentary(models.Model):

    name = models.CharField(max_length=50, verbose_name='Имя')
    email = models.EmailField(verbose_name='Электронная почта')
    body = models.TextField(verbose_name='Комментарий')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Время публикации')
    update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = f'Комментарий к странице "О нас"'
        verbose_name_plural = f'Комментарии к странице "О нас"'
        ordering = ('created',)

    def __str__(self):
        return 'Комментарий от {} с почтой {}'.format(self.name, self.email)


class OrderProduct(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    ordered = models.BooleanField(default=False, verbose_name='Заказ оформлен')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = f'Корзина пользователя'
        verbose_name_plural = f'Корзины пользователей'

    def get_total_item_price(self):
        if self.product.discount_price == 0 or None:
            return self.quantity * self.product.price
        else:
            return self.quantity * (self.product.price - (self.product.price / 100 * decimal.Decimal(self.product.discount_price)))

    def __str__(self):
        if self.quantity == 1:
            return f'Товар: {self.product.title}, в количестве: {self.quantity} единицы'
        else:
            return f'Товар: {self.product.title}, в количестве: {self.quantity} единиц'


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'
    STATUS_PAYED = 'payed'

    STATUS_CHOICES = (
        (STATUS_PAYED, 'Заказ оплачен'),
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Покупатель')
    products = models.ManyToManyField(OrderProduct, verbose_name='Товары')
    ordered_date = models.DateTimeField(verbose_name='Дата оформления заказа')
    order_receive_date = models.DateField(verbose_name='Дата получения', null=True, blank=True)
    ordered = models.BooleanField(default=False, verbose_name='Заказ оформлен')
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Оплатил')
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказа',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )

    class Meta:
        verbose_name = 'Оформленный заказ'
        verbose_name_plural = 'Оформленные заказы'

    def get_total(self):
        total = 0
        for order_product in self.products.all():
            total += order_product.get_total_item_price()
        return total

    def __str__(self):
        return self.user.email


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                             verbose_name='Покупатель')
    stripe_charge_id = models.CharField(max_length=50, verbose_name='Идентификатор платежа')
    amount = models.IntegerField(verbose_name='Сумма')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return self.user.email