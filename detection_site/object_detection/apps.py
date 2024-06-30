"""
Конфигурация приложения Object Detection для Django.

Этот модуль определяет конфигурацию приложения Object Detection, используемую Django.

Attributes:
    default_auto_field (str): Настройка для определения поля первичного ключа моделей.
    name (str): Имя приложения.

"""

from django.apps import AppConfig


class ObjectDetectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'object_detection'
