"""
URL конфигурация для приложения Object Detection.

Этот модуль определяет URL-шаблоны для приложения Object Detection, связывая каждый URL с соответствующей
видовой функцией или классовым представлением, которые обрабатывают запросы.

Attributes:
    urlpatterns (list): Список URL-шаблонов для приложения Object Detection, включая пути к различным видовым функциям.
        Каждый path() ассоциируется с соответствующей функцией представления для обработки запросов.

Примеры использования:
    Для перехода на домашнюю страницу: '/object_detection/'
    Для регистрации пользователя: '/object_detection/register/'
    Для входа пользователя: '/object_detection/login/'
    Для выхода пользователя: '/object_detection/logout/'
    Для отображения панели управления: '/object_detection/dashboard/'
    Для обработки изображения по идентификатору: '/object_detection/process/<int:feed_id>/'
    Для добавления изображения: '/object_detection/add-image-feed/'
    Для удаления изображения по идентификатору: '/object_detection/image/delete/<int:image_id>/'
    Для просмотра истории обработки: '/object_detection/detection_history/'
"""

from django.urls import path

from .views import (home, register, user_login, user_logout, dashboard, process_image_feed, add_image_feed, delete_image, \
    detection_history, detect_objects_other_model)

from django.conf import settings
from django.conf.urls.static import static
app_name = 'object_detection'

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('process/<int:feed_id>/', process_image_feed, name='process_feed'),
    path('add-image-feed/', add_image_feed, name='add_image_feed'),
    path('image/delete/<int:image_id>/', delete_image, name='delete_image'),
    path('detection_history/', detection_history, name='detection_history'),
    path('detect-objects/<int:feed_id>/', detect_objects_other_model, name='detect_objects_other_model'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
