# Use a lightweight base image
FROM python:3.10-slim

# Set environment variables to avoid prompts during installation
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Install only necessary tools
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app_api

# Use .dockerignore to exclude unnecessary files (e.g., .git, logs)
COPY requirements.txt /app_api/

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the application code
COPY . /app_api/

# Expose the application port
EXPOSE 8000

# Use a production-ready command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
