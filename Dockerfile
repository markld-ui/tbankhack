# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

RUN pip install --upgrade pip

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY . .

# Указываем порт, который будет использовать приложение
EXPOSE 8000

# Команда для запуска приложения
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000", "--timeout", "60"]