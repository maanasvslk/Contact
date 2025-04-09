FROM python:3.11-slim

# Set working directory
WORKDIR /app


# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create and set permissions
RUN mkdir -p /app/myproject && \
    chmod -R 777 /app

# Initialize database
RUN python manage.py migrate

# Make init script executable
RUN chmod +x init-superuser.sh

EXPOSE 8000
CMD ["./init-superuser.sh"]