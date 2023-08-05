import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-@&_dtkk_71x!fo7%r^*m_ix62u54ginq&+c#_0$2#0i1dcr-5l'

DEBUG = True

ALLOWED_HOSTS = ["*"]

STRIPE_SECRET_KEY = 'sk_test_51IgrwCEbODxaDCK41IuocujM1pRGfMpdmJhRLmJwVlSf6poqKjJlDFZk7O6i2UlTHSUL1Y4ktnaf14NxLhcgUmov00DL8osPQF'
# Приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ShopCore',
    'authentication',
    'import_export',
    'crispy_forms'

]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ProvodkaShop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ProvodkaShop.wsgi.application'
# Подключение БД
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'provodkacoredb',
        'USER': 'root',
        'PASSWORD': 'shigengree',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
        (os.path.join(BASE_DIR, "static"))
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Отправка сообщений пользователем

EMAIL_FROM_USER = 'ilya.sidorov.2014@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'ilya.sidorov.2014@gmail.com'
EMAIL_HOST_PASSWORD = 'khunyrizedypooox'
EMAIL_USE_TLS = 'True'


#Переменная для экспорта и импорта
IMPORT_EXPORT_USE_TRANSACTIONS = True

# Переменная для модели юзера(Абстрактная)
AUTH_USER_MODEL = 'authentication.User'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
ADMIN_SITE_HEADER = "Администрирование ПРОВОДКА РУ"