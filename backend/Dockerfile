# Use a slim Python image for a smaller footprint
FROM python:3.11-slim

# Set the working directory
WORKDIR /app/myproject

# Copy and install dependencies first to leverage Docker caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files
COPY myproject/ .

# Remove any existing db.sqlite3 file to ensure a fresh database
RUN rm -f db.sqlite3

# Run migrations to create a fresh db.sqlite3 file
RUN python manage.py migrate

# Ensure the working directory is writable for the database
RUN chmod -R 777 /app/myproject

# Copy the init-superuser.sh script and make it executable
COPY init-superuser.sh .
RUN chmod +x init-superuser.sh

# Expose the port for the Django server
EXPOSE 8000

# Run the init-superuser script and start the Django server, explicitly binding to 0.0.0.0
CMD ["/bin/bash", "-c", "/app/myproject/init-superuser.sh && python manage.py runserver 0.0.0.0:8000"]