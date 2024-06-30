"""
Форма для загрузки изображений в приложении Object Detection.

Этот модуль определяет форму ImageFeedForm, используемую для загрузки изображений
в приложении Object Detection.

Attributes:
    ImageFeedForm (forms.ModelForm): Форма для загрузки изображений.
        Определяет модель ImageFeed и указывает на использование поля 'image'.
        Имеет виджет для выбора файлов типа изображений и текст помощи для пользователей.
"""

from django import forms
from .models import ImageFeed


class ImageFeedForm(forms.ModelForm):
    class Meta:
        model = ImageFeed
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}),
        }
        help_texts = {
            'image': 'Upload an image file.',
        }
