FROM python:3.10-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

# Set PYTHONPATH explicitly
ENV PYTHONPATH=/app

WORKDIR /app/myproject

ENTRYPOINT ["/app/entrypoint.sh"]