FROM python:3.8-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libmemcached-dev \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

COPY requirements.txt constraints.txt /app/
RUN pip install --no-cache-dir -U -c constraints.txt pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt -c constraints.txt

COPY package*.json /app/
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi

COPY . /app/
RUN npm run build

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=apda.settings.base

RUN python manage.py migrate --noinput
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "apda.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "150"]
