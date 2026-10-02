# Temporary legacy-runtime reproduction only; do not use this image publicly.
FROM python:3.6.15-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY requirements-dev.txt /app/requirements-dev.txt
ARG INSTALL_DEV_DEPENDENCIES=false
RUN python -m pip install --upgrade 'pip<22' \
    && python -m pip install --no-cache-dir -r /app/requirements.txt \
    && if [ "$INSTALL_DEV_DEPENDENCIES" = "true" ]; then \
        python -m pip install --no-cache-dir \
            -r /app/requirements-dev.txt; \
    fi

COPY demo /app/demo
COPY sre-tools /app/sre-tools
WORKDIR /app/demo

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && exec python manage.py runserver 0.0.0.0:8000"]
