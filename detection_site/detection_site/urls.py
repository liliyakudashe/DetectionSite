"""
URL-конфигурация для проекта Django.

Этот модуль определяет URL-шаблоны для проекта Django, включая интерфейс администратора,
приложение object_detection и URL для статических медиафайлов.

URL-шаблоны:
    - '/admin/': URL для интерфейса администратора Django.
    - '/object_detection/': URL-шаблоны для приложения object_detection.
    - '/': Перенаправляет на URL '/object_detection/'.
    - URL-шаблоны для медиафайлов на основе settings.MEDIA_URL и settings.MEDIA_ROOT.

Для получения дополнительной информации о конфигурации URL в Django посетите:
https://docs.djangoproject.com/en/4.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('object_detection/', include('object_detection.urls')),
    path('', RedirectView.as_view(url='/object_detection/', permanent=True)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
