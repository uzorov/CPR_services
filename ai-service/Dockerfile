# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Создаем директорию для кеша и устанавливаем переменные окружения
RUN mkdir -p /app/cache
ENV TRANSFORMERS_CACHE=/app/cache
ENV HF_HOME=/app/cache

# Копируем файл зависимостей в контейнер
COPY ./ai-service/requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения в контейнер
COPY ./ai-service/main.py .

# Открываем порт, на котором будет работать приложение
EXPOSE 84

# Запускаем приложение с помощью uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "84", "--reload"]
