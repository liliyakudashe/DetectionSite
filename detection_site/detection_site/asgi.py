"""
ASGI конфигурация для проекта detection_site.

Этот файл определяет конфигурацию ASGI (Asynchronous Server Gateway Interface) для проекта
detection_site.

Он экспортирует вызываемое ASGI приложение под именем application на уровне модуля.

ASGI - это интерфейс асинхронного серверного шлюза, который используется для
обработки асинхронных HTTP запросов,
а также для поддержки WebSocket соединений в Django Channels.

Для получения дополнительной информации о конфигурации ASGI в Django смотрите
официальную документацию:
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/

Модули, импортируемые в этом файле:
- os: для установки переменной окружения DJANGO_SETTINGS_MODULE.
- django.core.asgi.get_asgi_application: функция, которая возвращает ASGI приложение
Django для обработки HTTP запросов.
- channels.routing.ProtocolTypeRouter: класс, используемый для определения маршрутизации
 для различных протоколов (http, websocket).
- channels.routing.URLRouter: класс, который принимает маршруты URL для обработки WebSocket соединений.
- channels.auth.AuthMiddlewareStack: класс, предоставляющий механизмы аутентификации для
 WebSocket соединений.
- object_detection.routing: модуль с определением маршрутов WebSocket для приложения object_detection.
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import object_detection.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            object_detection.routing.websocket_urlpatterns
        )
    ),
})