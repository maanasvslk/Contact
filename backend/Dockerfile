FROM python:3.11-slim
WORKDIR /app/myproject
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY myproject/ .
COPY init-superuser.sh .
RUN chmod +x init-superuser.sh
EXPOSE 8000
# Fix the path to init-superuser.sh (after volume mount, it's in /app/)
CMD ["/bin/bash", "-c", "/app/init-superuser.sh && python manage.py runserver 0.0.0.0:8000"]