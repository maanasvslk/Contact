FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x wait-for-db.sh init-superuser.sh
WORKDIR /app/myproject
EXPOSE 8000
CMD ["/app/wait-for-db.sh", "&&", "/app/init-superuser.sh", "&&", "python", "manage.py", "runserver", "0.0.0.0:8000"]