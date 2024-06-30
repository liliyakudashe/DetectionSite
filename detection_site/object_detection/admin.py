"""
Регистрация моделей администратора Django для управления через административный интерфейс.

Этот модуль регистрирует следующие модели для управления ими через административный интерфейс Django:
- ImageFeed: модель для работы с изображениями
- DetectedObject: модель для работы с обнаруженными объектами на изображениях
- DetectionHistory: модель для работы с историей обнаружения объектов

Для получения дополнительной информации о Django административном интерфейсе и регистрации моделей, посетите:
https://docs.djangoproject.com/en/5.0/ref/contrib/admin/
"""

from django.contrib import admin
from .models import ImageFeed, DetectedObject, DetectionHistory

admin.site.register(ImageFeed)
admin.site.register(DetectedObject)
admin.site.register(DetectionHistory)
