pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }
        stage('Build and Deploy') {
            steps {
                script {
                    // Clean up any existing containers
                    sh 'docker-compose down --remove-orphans || true'

                    // Build the images
                    sh 'docker-compose build'

                    // Start the services in detached mode
                    sh 'docker-compose up -d'

                    // Wait for backend to be ready
                    sh 'sleep 10'

                    // Run migrations
                    sh '''
                        docker-compose exec backend bash -c \
                            "python manage.py migrate"
                    '''

                    // Create superuser using the init script
                    sh '''
                        docker-compose exec backend bash -c \
                            "chmod +x /app/myproject/init-superuser.sh && \
                            /app/myproject/init-superuser.sh"
                    '''

                    // Verify the database file
                    sh 'ls -la backend/myproject/db.sqlite3'
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
            sh 'docker-compose logs backend'
            sh 'ls -la backend/myproject/'
        }
    }
}