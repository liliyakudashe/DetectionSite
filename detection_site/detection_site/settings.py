"""
Настройки Django для проекта detection_site.

Сгенерировано с помощью 'django-admin startproject' с использованием Django 5.0.4.

Дополнительную информацию о данном файле можно найти по следующему адресу:
https://docs.djangoproject.com/en/5.0/topics/settings/

Для полного списка настроек и их значений см. документацию Django:
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
# Определение базовой директории проекта
BASE_DIR = Path(__file__).resolve().parent.parent


# Основные настройки разработки - не подходят для использования в продакшене
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# Ключ сессии, используемый в продакшене должен быть уникальным и сложным
SECRET_KEY = 'django-insecure-*$&@tu^%8hyi@%j2j(zs^vnig4&xz8qy!$n4xgu=#d=mku6cmy'


DEBUG = True

# Разрешенные хосты для проекта
ALLOWED_HOSTS = []


# Установленные приложения Django
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'object_detection',
]

# Промежуточное ПО (middleware) Django
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Основной URL-конфигурации проекта
ROOT_URLCONF = 'detection_site.urls'

# Настройки шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# WSGI-приложение
WSGI_APPLICATION = 'detection_site.wsgi.application'

# ASGI-приложение
ASGI_APPLICATION = 'detection_site.asgi.application'

# Настройки базы данных
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Проверка пароля пользователя
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
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


# Настройки локализации
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Настройки статических файлов
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

# Тип поля для первичных ключей по умолчанию
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки каналов (channels)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    }
}

# URL для входа и выхода из системы
LOGIN_URL = '/object_detection/login/'
LOGOUT_URL = '/object_detection/logout/'

# Настройки для загрузки медиа-файлов
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')