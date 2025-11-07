# ===============================
# 1️⃣  СТАДИЯ СБОРКИ (builder)
# ===============================
FROM python:3.11-slim AS builder

WORKDIR /app

# Устанавливаем системные зависимости для сборки пакетов
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt .

# Ставим зависимости в отдельную директорию
# (чтобы потом скопировать только готовые библиотеки)
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt


# ===============================
# 2️⃣  СТАДИЯ РАНТАЙМА (final)
# ===============================
FROM python:3.11-slim

# Системные библиотеки, необходимые OpenCV
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Переносим зависимости из builder stage
COPY --from=builder /install /usr/local

# Копируем исходный код
COPY . .

# Открываем порт FastAPI
EXPOSE 8000

# Переменные окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DOCKER_POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}

# Запуск uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
