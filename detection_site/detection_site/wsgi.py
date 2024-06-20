"""
WSGI-конфигурация для проекта detection_site.

Этот файл предоставляет WSGI-вызываемый объект в качестве переменной уровня модуля
с именем «application».

Дополнительную информацию о данном файле можно найти по следующему адресу:
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'detection_site.settings')

application = get_wsgi_application()
