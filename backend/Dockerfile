FROM python:3.10-slim

# Install PostgreSQL client tools
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

WORKDIR /app/myproject

ENTRYPOINT ["/app/entrypoint.sh"]