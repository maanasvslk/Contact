FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Create and set permissions for database directory
RUN mkdir -p /app/myproject && \
    chmod -R 777 /app

# Initialize database and superuser
RUN python myproject/manage.py migrate && \
    chmod +x init-superuser.sh

EXPOSE 8000
CMD ["./init-superuser.sh"]