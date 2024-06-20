#!/usr/bin/env python
"""Утилита командной строки Django для административных задач."""
import os
import sys


def main():
    """Основная функция для запуска административных задач.

    Устанавливает переменную окружения 'DJANGO_SETTINGS_MODULE' на 'detection_site.settings'
    и вызывает выполнение командной строки Django.

    Исключения:
        ImportError: Возникает, если Django не удалось импортировать. Проверьте, что Django
        установлен и доступен через переменную окружения PYTHONPATH. Убедитесь также, что
        активирована виртуальная среда."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'detection_site.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
