# Base Python Image
FROM docker.io/python:3.12-slim-bookworm AS python

# Stage 1: Building Dependency Wheels
FROM python AS python-build-stage

ARG BUILD_ENVIRONMENT=local 

# Install build dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Copy requirements files
COPY ./requirements .

# Create wheels directory and build wheels
RUN mkdir -p /usr/src/app/wheels && \
    pip wheel --wheel-dir /usr/src/app/wheels -r ${BUILD_ENVIRONMENT}.txt

# Stage 2: Python Run
FROM python AS python-run-stage

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app/
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV BUILD_ENV=${BUILD_ENVIRONMENT}
WORKDIR ${APP_HOME}

# Install runtime dependencies and setup user
RUN apt-get update && apt-get install --no-install-recommends -y \
    sudo \
    git \
    bash-completion \
    nano \
    ssh \
    libpq-dev \
    gettext \
    # && addgroup --system django \
    # && adduser --system --ingroup django django \
    && mkdir -p ${APP_HOME}/staticfiles \
    # && chown django:django ${APP_HOME}/staticfiles \
    && chmod 775 ${APP_HOME}/staticfiles \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from the build stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels/

# **Install setuptools before other dependencies**
RUN pip install --no-cache-dir setuptools && \
    pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

# Copy and prepare entrypoint and start scripts
COPY  ./docker/local/django/entrypoint.sh /entrypoint
RUN sed -i "s/\r//g" /entrypoint && chmod +x /entrypoint

COPY  ./docker/local/django/start.sh /start
RUN sed -i "s/\r//g" /start && chmod +x /start

COPY  ./docker/local/django/celery/worker/start.sh /start-celeryworker
RUN sed -i "s/\r//g" /start-celeryworker && chmod +x /start-celeryworker

COPY  ./docker/local/django/celery/beat/start.sh /start-celerybeat
RUN sed -i "s/\r//g" /start-celerybeat && chmod +x /start-celerybeat


COPY  ./docker/local/django/celery/flower/start.sh /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower

# Copy application code
COPY  . ${APP_HOME}
# RUN chown django:django ${APP_HOME}

# Switch to non-root user
# USER django

# Set entrypoint
ENTRYPOINT [ "/entrypoint" ]
