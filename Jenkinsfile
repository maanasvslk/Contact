pipeline {
    agent any

    environment {
        VERSION = "${env.GIT_BRANCH?.split('/')[-1] ?: 'v1'}" // Default to 'v1' if no branch
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
                    sh 'docker-compose build'
                }
            }
        }

        stage('Deploy Containers') {
            steps {
                script {
                    // Stop and remove existing containers for this version, then start new ones
                    sh "docker-compose down --remove-orphans || true" // Ignore errors if no containers exist
                    sh "docker-compose up -d" // Run in detached mode
                }
            }
        }

        stage('Apply Migrations') {
            steps {
                script {
                    sh 'docker-compose exec -T backend python manage.py makemigrations'
                    sh 'docker-compose exec -T backend python manage.py migrate'
                }
            }
        }

        stage('Test Application') {
            steps {
                script {
                    echo "Running tests..."
                    // Add test commands here if needed
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
        }
    }
}