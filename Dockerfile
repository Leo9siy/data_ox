FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off


RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    dos2unix \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && apt clean

RUN python -m pip install --upgrade pip

WORKDIR app/

COPY requirements.txt .

COPY src/ .

RUN pip install -r requirements.txt
