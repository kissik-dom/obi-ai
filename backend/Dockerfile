# Multi-Stage Dockerfile: base -> security -> engineering -> images -> video -> messaging
FROM python:3.11-slim AS base
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl git && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app/backend
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM base AS security
COPY requirements_stages/security.txt /app/requirements_stages/security.txt
RUN pip install --no-cache-dir -r /app/requirements_stages/security.txt || true

FROM security AS engineering
COPY requirements_stages/engineering.txt /app/requirements_stages/engineering.txt
RUN pip install --no-cache-dir -r /app/requirements_stages/engineering.txt || true

FROM engineering AS images
COPY requirements_stages/images.txt /app/requirements_stages/images.txt
RUN pip install --no-cache-dir -r /app/requirements_stages/images.txt || true

FROM images AS video
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg && rm -rf /var/lib/apt/lists/*
COPY requirements_stages/video.txt /app/requirements_stages/video.txt
RUN pip install --no-cache-dir -r /app/requirements_stages/video.txt || true

FROM video AS messaging
COPY requirements_stages/messaging.txt /app/requirements_stages/messaging.txt
RUN pip install --no-cache-dir -r /app/requirements_stages/messaging.txt || true
