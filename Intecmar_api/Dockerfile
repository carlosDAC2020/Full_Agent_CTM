# syntax=docker/dockerfile:1
FROM python:3.11-slim

# ---------------------------------------
# 1. Configuración base
# ---------------------------------------
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# ---------------------------------------
# 2. Instalar dependencias del sistema
# ---------------------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    default-libmysqlclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libpng-dev \
    curl \
    wget \
    gnupg \
    git \
    libgl1 \
    libglib2.0-0 \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------------------
# 3. Instalar Node 20 + Marp CLI
# ---------------------------------------
RUN mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key \
       | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg \
    && echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" \
       > /etc/apt/sources.list.d/nodesource.list \
    && apt-get update \
    && apt-get install -y nodejs \
    && npm install -g @marp-team/marp-cli

# ---------------------------------------
# 4. Instalar Google Chrome estable
# ---------------------------------------
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub \
        | gpg --dearmor -o /etc/apt/trusted.gpg.d/google.gpg \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb stable main" \
        > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------------------
# 5. Instalar dependencias Python
# ---------------------------------------
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ---------------------------------------
# 6. Copiar el código fuente y configurar
# ---------------------------------------
COPY . /app

# Directorios para salidas y datos compartidos
RUN mkdir -p /app/outputs /app/backend/shared_data

EXPOSE 8000

ENV PYTHONPATH=/app

# Comando por defecto (se sobreescribe en docker-compose)
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
