# Temporary legacy-runtime reproduction only; do not use this image publicly.
FROM python:3.6.15-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade 'pip<22' \
    && python -m pip install --no-cache-dir -r /app/requirements.txt

COPY demo /app/demo
COPY sre-tools /app/sre-tools
WORKDIR /app/demo

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && exec python manage.py runserver 0.0.0.0:8000"]
