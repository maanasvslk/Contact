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
                // Wait for container to be fully up
                sh 'sleep 3'  // Give the container time to start
            }
        }
        stage('Run Migrations and Superuser') {
            steps {
                sh 'docker exec cd-project-backend-1 python /app/myproject/manage.py migrate contact --database=contact_1'
                sh 'docker exec cd-project-backend-1 python /app/myproject/manage.py migrate contact_v2 --database=contact_v2'
                sh 'docker exec -e DJANGO_SETTINGS_MODULE=myproject.settings cd-project-backend-1 python /app/myproject/create_superuser.py'
            }
        }
        stage('Post-Deployment') {
            steps {
                script {
                    def APP_VERSION = '1'  // Hardcoded version
                    if (APP_VERSION == '1') {
                        echo 'Deployment successful! Access the app at: http://127.0.0.1:8000'
                    } else if (APP_VERSION == '2') {
                        echo 'Deployment successful! Access the app at: http://127.0.0.1:8000/v2'
                    }
                }
            }
        }
    }
}