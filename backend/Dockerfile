# backend/Dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "python myproject/manage.py migrate contact --database=contact_1 && python myproject/manage.py migrate contact_v2 --database=contact_v2 && python myproject/manage.py runserver 0.0.0.0:8000"]