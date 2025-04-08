FROM python:3.11-slim
WORKDIR /app/myproject
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn  # Add gunicorn
COPY myproject/ .
COPY init-superuser.sh .
RUN chmod +x init-superuser.sh
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]