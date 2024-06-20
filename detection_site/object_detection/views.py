"""
Представления Django для приложения object_detection.

Этот модуль содержит функции представлений для управления веб-страницами и операциями пользовательского взаимодействия в приложении object_detection.

Атрибуты:
    home(request): Возвращает домашнюю страницу приложения.
    register(request): Предоставляет форму регистрации пользователей и обрабатывает её данные.
    user_login(request): Предоставляет форму входа пользователей и обрабатывает её данные.
    user_logout(request): Выход пользователя из системы.
    dashboard(request): Отображает панель управления пользователя с его загруженными изображениями.
    process_image_feed(request, feed_id): Обрабатывает изображение с заданным feed_id.
    add_image_feed(request): Предоставляет форму загрузки изображения и сохраняет его в базе данных.
    delete_image(request, image_id): Удаляет изображение из базы данных и файловой системы проекта.
    detection_history(request): Отображает историю обработанных изображений текущего пользователя.

Функции для внутреннего использования:
    pathfinder(image): Вспомогательная функция для создания пути к изображениям.
    __del_img(image): Удаляет изображение и его обработанный экземпляр из директории проекта.
    __del_duplicate_img(image): Удаляет дубликат изображения перед его обработкой.

Модули Django:
    render: Функция для рендеринга HTML-шаблонов.
    get_object_or_404: Функция для получения объекта или 404 ошибки, если объект не найден.
    redirect: Функция для перенаправления пользователя на другую страницу.
    login_required: Декоратор для защиты представлений, требующих аутентификации пользователя.

Импорты:
    os: Встроенный модуль для работы с операционной системой.
    ImageFeed, DetectionHistory: Модели данных Django для работы с изображениями и историей обработки.
    process_image: Функция для обработки изображений.
    ImageFeedForm: Форма Django для загрузки изображений.
    AuthenticationForm, UserCreationForm: Формы Django для аутентификации и регистрации пользователей.

"""

import os

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import ImageFeed, DetectionHistory
from .utils import (process_image,process_image_detect_other_model)
from .forms import ImageFeedForm
import unittest
import io
from django.http import HttpResponse


def home(request):
    """Отображает домашнюю страницу приложения."""
    return render(request, 'object_detection/home.html')


def register(request):
    """Предоставляет форму регистрации пользователей и обрабатывает её данные."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('object_detection:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'object_detection/register.html', {'form': form})


def user_login(request):
    """Предоставляет форму входа пользователей и обрабатывает её данные."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('object_detection:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'object_detection/login.html', {'form': form})


@login_required
def user_logout(request):
    """Выход пользователя из системы."""
    logout(request)
    return redirect('object_detection:login')


@login_required
def dashboard(request):
    """Отображает панель управления пользователя с его загруженными изображениями."""
    image_feeds = ImageFeed.objects.filter(user=request.user)
    return render(request, 'object_detection/dashboard.html', {'image_feeds': image_feeds})


@login_required
def process_image_feed(request, feed_id):
    """Обрабатывает изображение с заданным feed_id."""
    image_feed = get_object_or_404(ImageFeed, id=feed_id, user=request.user)
    process_image(feed_id)  # Consider handling this asynchronously
    return redirect('object_detection:dashboard')


@login_required
def detect_objects_other_model(request, feed_id):
    """Совершить классификацию над изображением"""
    image_feed = get_object_or_404(ImageFeed, id=feed_id, user=request.user)

    __del_duplicate_img(image_feed)

    process_image_detect_other_model(feed_id)  # Consider handling this asynchronously
    return redirect('object_detection:dashboard')


@login_required
def add_image_feed(request):
    """Предоставляет форму загрузки изображения и сохраняет его в базе данных."""
    if request.method == 'POST':
        form = ImageFeedForm(request.POST, request.FILES)
        if form.is_valid():
            image_feed = form.save(commit=False)
            image_feed.user = request.user
            image_feed.save()
            return redirect('object_detection:dashboard')
    else:
        form = ImageFeedForm()
    return render(request, 'object_detection/add_image_feed.html', {'form': form})


def pathfinder(image):
    """Функция создания пути для изображений."""
    filename = str(image)
    filename = filename.split('/')[1]
    relative_path = 'media/images/'
    relative_path_2 = 'media/processed_images/processed_images'
    file_path = os.path.join(os.getcwd(), relative_path, filename)
    file_path_2 = os.path.join(os.getcwd(), relative_path_2, filename)
    return file_path, file_path_2, filename


def __del_img(image):
    """Удаляет изображение и его обработанный экземпляр из директории проекта."""
    file_path, file_path_2, filename = pathfinder(image)
    if os.path.isfile(file_path) and os.path.isfile(file_path_2):
        os.remove(file_path)
        os.remove(file_path_2)
    elif os.path.isfile(file_path):
        os.remove(file_path)


def __del_duplicate_img(image):
    """Удаляет дубликат изображения перед его обработкой."""
    _, file_path_2, filename = pathfinder(image)
    if os.path.isfile(file_path_2):
        os.remove(file_path_2)


@login_required
def delete_image(request, image_id):
    """Удаляет изображение из базы данных и файловой системы проекта."""
    image = get_object_or_404(ImageFeed, id=image_id, user=request.user)  # Ensuring only the owner can delete
    __del_img(image)

    DetectionHistory.objects.filter(
        user=request.user,
        image=image.image,
        processed_image=image.processed_image
    ).update(is_deleted=True)

    image.delete()
    return redirect('object_detection:dashboard')


@login_required
def detection_history(request):
    """Отображает историю обработанных изображений текущего пользователя."""
    history = DetectionHistory.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'object_detection/detection_history.html', {'history': history})
