pipeline {
    agent any

    environment {
        VERSION = "${env.GIT_BRANCH?.split('/')[-1] ?: 'v1'}" // Default to 'v1' if no branch
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
                sh 'ls -R backend/myproject'  // Debug: List files in backend/myproject
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
                    // Stop and remove existing containers for this version, then start new ones
                    sh "docker-compose down --remove-orphans || true" // Ignore errors if no containers exist
                    sh "docker-compose up -d" // Run in detached mode
                }
            }
        }

        stage('Apply Migrations') {
            steps {
                script {
                  echo "Migrations are now applied at container startup, skipping this stage."
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
            sh 'docker-compose logs backend'  // Debug: Show backend logs on failure
        }
    }
}