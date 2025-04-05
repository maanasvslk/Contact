pipeline {
    agent any

    environment {
        // Dynamically set VERSION based on the Git branch name
        VERSION = "${env.GIT_BRANCH?.split('/')[-1] ?: 'v1'}" // Default to 'v1' if no branch is found
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Pull the latest code from the GitHub repository
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                // Build the Docker images for the frontend, backend, and database services
                script {
                    // Build backend and frontend images using docker-compose build
                    sh 'docker-compose build'
                }
            }
        }

        stage('Run Docker Containers') {
            steps {
                // Start the containers (frontend, backend, database)
                script {
                    sh 'docker-compose up -d'  // Run containers in detached mode
                }
            }
        }

        stage('Apply Migrations') {
            steps {
                script {
                    // Run Django migrations for the correct versioned database
                    sh 'docker-compose exec backend python manage.py makemigrations'  // Create migration files if any changes
                    sh 'docker-compose exec backend python manage.py migrate'  // Apply migrations to the correct database
                }
            }
        }

        stage('Test Application') {
            steps {
                // Test the application after deployment to verify everything is working
                script {
                    // Add your test scripts here (for example, running unit tests, integration tests, etc.)
                    echo "Running tests..."
                }
            }
        }

        stage('Cleanup') {
            steps {
                // Clean up, stop the containers if needed
                script {
                    sh 'docker-compose down'  // Bring the containers down after deployment
                }
            }
        }
    }

    post {
        success {
            echo "Deployment completed successfully."
        }
        failure {
            echo "Deployment failed."
        }
    }
}
