# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim-bookworm


# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SETTINGS_MODULE=config.settings.prod

# Set work directory
WORKDIR /app

# Install system dependencies with retry logic
RUN apt-get update --fix-missing && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    redis-tools \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy requirements first for better Docker layer caching
COPY Backend/requirements/prod.txt /app/
RUN pip install --no-cache-dir -r prod.txt

# Copy the entire project
COPY . /app/

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash django && chown -R django:django /app
USER django

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/admin/ || exit 1

# Default command (can be overridden in docker-compose.yml or render.yaml)
CMD ["python", "Backend/Portafy/manage.py", "runserver", "0.0.0.0:8000"]
