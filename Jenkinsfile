pipeline {
    agent any

    environment {
        VERSION = "v2"  // Hardcode for v2 deployment
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    sh 'docker-compose build --no-cache'
                }
            }
        }

        stage('Deploy Containers') {
            steps {
                script {
                    sh "docker-compose down -v --remove-orphans || true"
                    sh "docker-compose up -d"
                }
            }
        }

        stage('Apply Migrations') {
            steps {
                script {
                    sh 'sleep 10'
                    sh 'docker-compose exec -T backend python manage.py makemigrations'
                    sh 'docker-compose exec -T backend python manage.py migrate --database=default'
                }
            }
        }
    }

    post {
        success {
            echo "Deployment completed successfully for version ${VERSION}."
        }
        failure {
            echo "Deployment failed for version ${VERSION}."
            sh 'docker-compose logs backend'
            sh 'docker-compose logs db'
        }
    }
}