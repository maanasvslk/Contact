FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Make sure entrypoint is executable
RUN chmod +x entrypoint.sh

WORKDIR /app/myproject

# Use absolute path to entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]