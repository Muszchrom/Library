FROM python:3.10.0-slim AS base
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev gcc
COPY requirements.txt requirements.txt

FROM base AS dev
RUN pip install --no-cache-dir -r requirements.txt
COPY . .