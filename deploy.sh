#!/bin/bash

# Переход в директорию проекта (если нужно)
# cd /path/to/your/project

# Активация виртуального окружения (если используется)
if [ -d "_venv" ]; then
    echo "Активация виртуального окружения..."
    source _venv/bin/activate  # Для Linux/macOS
    # source _venv/Scripts/activate  # Для Windows
else
    echo "Создание виртуального окружения..."
    python -m venv _venv
    source _venv/bin/activate  # Для Linux/macOS
    # source _venv/Scripts/activate  # Для Windows
fi

# Установка зависимостей
echo "Установка зависимостей из requirements.txt..."
pip install -r requirements.txt

# Применение миграций (если используется база данных)
if [ -f "DB.py" ]; then
    echo "Применение миграций базы данных..."
    python DB.py  # Замените на команду для миграций, если используется ORM
fi

# Сборка статических файлов (если нужно)
if [ -d "static" ]; then
    echo "Копирование статических файлов..."
    # Если используется Flask, можно использовать команду для сбора статики
    # python main.py collectstatic --noinput
fi

# Запуск приложения
echo "Запуск приложения..."
gunicorn main:app --timeout 60 --workers 4 --bind 0.0.0.0:8000

echo "Развертывание завершено!"