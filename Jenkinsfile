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
                    sh 'docker-compose down --remove-orphans --volumes || true'

                    // Build the images
                    sh 'docker-compose build'

                    // Start the services in detached mode
                    sh 'docker-compose up -d'

                    // Wait for backend to be up (check HTTP response)
                    sh '''
                        for i in {1..30}; do
                            STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/admin/ || echo "0")
                            echo "Backend HTTP status: $STATUS"
                            if [ "$STATUS" = "200" ] || [ "$STATUS" = "302" ]; then
                                echo "Backend is up and running!"
                                break
                            fi
                            echo "Waiting for backend to be up..."
                            sleep 5
                        done
                        if [ "$STATUS" != "200" ] && [ "$STATUS" != "302" ]; then
                            echo "Backend failed to start!"
                            docker-compose logs backend
                            exit 1
                        fi
                    '''

                    // Wait for frontend to be up (check HTTP response)
                    sh '''
                        for i in {1..30}; do
                            STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/ || echo "0")
                            echo "Frontend HTTP status: $STATUS"
                            if [ "$STATUS" = "200" ]; then
                                echo "Frontend is up and running!"
                                break
                            fi
                            echo "Waiting for frontend to be up..."
                            sleep 5
                        done
                        if [ "$STATUS" != "200" ]; then
                            echo "Frontend failed to start!"
                            docker-compose logs frontend
                            exit 1
                        fi
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
            sh 'docker-compose logs frontend'
            sh 'ls -la backend/myproject/'
        }
    }
}