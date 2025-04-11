FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend directory
COPY . .

# Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# Set the working directory to your Django project
WORKDIR /app/myproject

ENTRYPOINT ["/app/entrypoint.sh"]