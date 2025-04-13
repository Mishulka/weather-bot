FROM python:3.9-slim

WORKDIR /app

# Устанавливаем ТОЛЬКО необходимые зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем зависимости отдельным слоем
COPY requirements.txt .
RUN pip install --no-cache-dir \
    aiogram==2.25.1 \
    aiohttp==3.8.4 \
    requests==2.28.1

# Копируем основной код
COPY . .

CMD ["python", "main.py"]