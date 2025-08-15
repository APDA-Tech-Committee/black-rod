FROM python:3.8-buster

WORKDIR /app

RUN sed -i 's|deb.debian.org|archive.debian.org|g' /etc/apt/sources.list \
 && sed -i '/security.debian.org/d' /etc/apt/sources.list

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libmemcached-dev \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://deb.nodesource.com/setup_10.x | bash - \
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

COPY bin/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
