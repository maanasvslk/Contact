FROM python:3.11-slim

WORKDIR /app/myproject

# Copy only requirements first to cache pip install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only essential project files
COPY myproject/ .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]