# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project
COPY . .

# Expose the port (adjust if your app uses a different port)
EXPOSE 8000

# Run migrations and start the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]