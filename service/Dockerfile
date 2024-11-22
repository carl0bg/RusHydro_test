FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE service.settings

EXPOSE 8080

CMD ["/wait-for-it.sh", "postgres:5432", "--", "python", "manage.py", "runserver", "0.0.0.0:8080"]
