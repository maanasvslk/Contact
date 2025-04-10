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

        stage('Make Migrations') {
            steps {
                sh 'docker exec contact-backend-1 python /app/myproject/manage.py makemigrations'
            }
        }

        stage('Run Migrations') {
            steps {
                sh 'docker exec contact-backend-1 python /app/myproject/manage.py migrate'
                sh 'docker exec -e DJANGO_SETTINGS_MODULE=myproject.settings contact-backend-1 python /app/myproject/create_superuser.py'
            }
        }
    }
}
