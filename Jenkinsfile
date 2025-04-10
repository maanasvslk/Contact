pipeline {
    agent any

    options {
        timeout(time: 4, unit: 'MINUTES')
    }

    stages {
        stage('Build and Deploy with Docker Compose') {
            steps {
                sh 'docker-compose down'
                sh 'docker-compose build'
                sh 'docker-compose up -d'
            }
        }
        stage('Run Migrations') {
            steps {
                // Ensure the container is started and run migrations in the correct container
                sh 'docker exec cd-project-backend-1 python /app/myproject/manage.py migrate'
                sh 'docker exec -e DJANGO_SETTINGS_MODULE=myproject.settings cd-project-backend-1 python /app/myproject/create_superuser.py'
            }
        }
    }
}
