FROM python:3.10-slim

RUN apt-get update && apt-get install -y git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app_api
COPY . /app_api

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--log-level", "debug"]
