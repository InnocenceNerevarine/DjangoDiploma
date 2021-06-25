# Generated by Django 3.2.3 on 2021-06-05 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='avatars', verbose_name='Аватар пользователя'),
        ),
    ]
