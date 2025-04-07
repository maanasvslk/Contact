pipeline {
    agent any

    environment {
        VERSION = "${env.GIT_BRANCH?.split('/')[-1] ?: 'v1'}"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
                sh 'ls -R backend/myproject'
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
                    // Stop and remove existing containers and volumes
                    sh "docker-compose down -v --remove-orphans || true" // Added -v to remove volumes
                    sh "docker-compose up -d"
                }
            }
        }

        stage('Apply Migrations') {
            steps {
                script {
                    sh 'sleep 10'
                    sh 'docker-compose exec -T backend python manage.py makemigrations'
                    sh 'docker-compose exec -T backend python manage.py migrate'
                }
            }
        }

        stage('Test Application') {
            steps {
                script {
                    echo "Running tests..."
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
            sh 'docker-compose logs db'  // Added to show db logs on failure
        }
    }
}