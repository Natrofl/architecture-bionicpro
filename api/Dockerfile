# syntax=docker/dockerfile:1

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

COPY requirements.txt /tmp

RUN --mount=type=cache,target=/root/.cache \
    pip install -r /tmp/requirements.txt

WORKDIR /app

COPY app.py app.py

EXPOSE 8000

CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "8000", "--reload", "app.py"]
