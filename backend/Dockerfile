FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything except what's in .dockerignore
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Set working directory to Django project
WORKDIR /app/myproject

ENTRYPOINT ["/app/entrypoint.sh"]