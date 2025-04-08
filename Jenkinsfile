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

                    // Wait for backend to be healthy
                    sh '''
                        for i in {1..30}; do
                            STATUS=$(docker inspect --format='{{.State.Health.Status}}' contact-backend-1 || echo "not_running")
                            echo "Backend status: $STATUS"
                            if [ "$STATUS" = "healthy" ]; then
                                echo "Backend is healthy!"
                                break
                            fi
                            if [ "$STATUS" = "not_running" ]; then
                                echo "Backend container is not running!"
                                docker-compose logs backend
                                exit 1
                            fi
                            echo "Waiting for backend to be healthy..."
                            sleep 5
                        done
                        if [ "$STATUS" != "healthy" ]; then
                            echo "Backend failed to become healthy!"
                            docker-compose logs backend
                            exit 1
                        fi
                    '''

                    // Run migrations
                    sh '''
                        docker-compose exec -T backend bash -c \
                            "python manage.py migrate"
                    '''

                    // Create superuser using the init script
                    sh '''
                        docker-compose exec -T backend bash -c \
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