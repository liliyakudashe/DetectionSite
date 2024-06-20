"""
Модели для приложения Object Detection.

Этот модуль содержит определения трех моделей Django, используемых в приложении Object Detection:
- ImageFeed: Хранит информацию о загруженных изображениях пользователей.
- DetectedObject: Сохраняет результаты обнаружения объектов на изображениях.
- DetectionHistory: Хранит историю обработки изображений с обнаруженными объектами.

Attributes:
    ImageFeed (models.Model): Модель для хранения информации о загруженных изображениях.
        Связана с пользователем через внешний ключ и содержит поля для основного и обработанного изображений.

    DetectedObject (models.Model): Модель для хранения результатов обнаружения объектов на изображениях.
        Связана с ImageFeed через внешний ключ и содержит поля для типа объекта, уверенности в обнаружении и местоположения.

    DetectionHistory (models.Model): Модель для хранения истории обработки изображений с обнаруженными объектами.
        Связана с пользователем через внешний ключ и содержит поля для оригинального и обработанного изображений,
        текстового поля для сохранения обнаруженных объектов, времени создания записи и флага удаления.
"""

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class ImageFeed(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    processed_image = models.ImageField(upload_to='processed_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.image.name}"


class DetectedObject(models.Model):
    image_feed = models.ForeignKey(ImageFeed, related_name='detected_objects', on_delete=models.CASCADE)
    object_type = models.CharField(max_length=100)
    confidence = models.FloatField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.object_type} ({self.confidence * 100}%) on {self.image_feed.image.name}"


class DetectionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='original_images/')
    processed_image = models.ImageField(upload_to='processed_images/', blank=True, null=True)
    detected_objects = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'DetectionHistory({self.user.username}, {self.created_at})'
