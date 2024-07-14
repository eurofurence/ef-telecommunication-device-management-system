######################################
# Stage 0: Build backend application #
######################################
FROM python:3.11-alpine as build

RUN set -ex && \
    apk add --no-cache curl

# Prevent Python from buffering stdout and stderr, and prevent writing .pyc files
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install poetry
RUN set -ex && \
    curl -sSL https://install.python-poetry.org | \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    python3 -

# Install/build Python dependencies
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN set -ex && \
    /opt/poetry/bin/poetry config virtualenvs.in-project true && \
    /opt/poetry/bin/poetry install --no-dev

# Inject app code and build static files
COPY backend /app/backend
COPY manage.py /app
RUN set -ex && \
    EFTDMS_DJANGO_SECRET_KEY=null \
    EFTDMS_DJANGO_BASE_URL=localhost \
    /opt/poetry/bin/poetry run python manage.py collectstatic --noinput


#######################################
# Stage 1: Django runtime environment #
#######################################
FROM python:3.11-alpine

# Inject application
WORKDIR /app
COPY --from=build /app .
ENV PATH="/app/.venv/bin:$PATH"

# Copy entrypoint into image
COPY docker/backend/docker-entrypoint.sh /docker-entrypoint.sh
RUN set -ex && \
    chmod +x /docker-entrypoint.sh && \
    mkdir -p /mnt/backend_static

# Setup permissions to allow Django to run as unprivileged user
RUN set -ex && \
    addgroup -g 1000 -S django && \
    adduser -u 1000 -S django -G django && \
    chown django:django /app && \
    chown -R django:django /mnt/backend_static

USER django:django

EXPOSE 8000
ENTRYPOINT [ "/docker-entrypoint.sh" ]
CMD [ "daphne", "-b", "0.0.0.0", "-p", "8000", "backend.asgi:application" ]
