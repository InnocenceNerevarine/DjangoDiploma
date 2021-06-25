from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_email_verified = models.BooleanField(default=False, verbose_name='Аккаунт активирован')
    phone = models.CharField(max_length=20, verbose_name='Телефон', null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, verbose_name='Аватар пользователя', upload_to='avatars')

    def __str__(self):
        return self.email
