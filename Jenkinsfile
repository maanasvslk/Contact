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
                sh '''
                    for i in {1..30}; do
                        if docker ps | grep -q cd-project-backend-1; then
                            echo "Container is running"
                            break
                        fi
                        echo "Waiting for container... ($i/30)"
                        sleep 2
                    done
                    docker ps | grep cd-project-backend-1 || (echo "Container failed to start" && exit 1)
                '''
            }
        }
        stage('Run Superuser Creation') {
            steps {
                sh 'docker exec -e DJANGO_SETTINGS_MODULE=myproject.settings cd-project-backend-1 python /app/myproject/create_superuser.py'
            }
        }
        stage('Post-Deployment') {
            steps {
                script {
                    def APP_VERSION = '1'
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