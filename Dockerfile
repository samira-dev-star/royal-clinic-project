# Dockerfile - Using official Python image (simpler)
FROM python:3.11-bookworm

# Install Node.js 20 (LTS) - compatible with latest npm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest

# Install system dependencies for mysqlclient, git, and Python build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    netcat-traditional \
    git \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# ✅ Install Python dependencies
COPY royal_clinic/requirements.txt .
RUN pip install --upgrade pip wheel setuptools
RUN pip install -r requirements.txt

# Patch django-jalali to work with Django 5.1
RUN sed -i 's/from django.utils import datetime_safe, formats/from django.utils import formats/g' \
        /usr/local/lib/python3.11/site-packages/django_jalali/forms/widgets.py

# ✅ Install Node dependencies
COPY royal_clinic/package*.json ./
RUN npm install --legacy-peer-deps || npm install

# ✅ Copy project
COPY royal_clinic/ .

# ✅ Compile Tailwind
RUN npm run build-css || echo "⚠️ Tailwind build warning"

# ✅ Create user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app && \
    mkdir -p /app/media /app/staticfiles && \
    chown -R appuser:appuser /app/media /app/staticfiles

USER appuser

# ✅ Entrypoint
COPY --chown=appuser:appuser docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]