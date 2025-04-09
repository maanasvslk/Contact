# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# First copy only requirements to cache the pip install step
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Then copy the rest
COPY . .

RUN chmod +x init-superuser.sh

EXPOSE 8000
CMD ["./init-superuser.sh"]