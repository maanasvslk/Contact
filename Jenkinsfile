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
                    // Clean up any existing containers and volumes
                    sh 'docker-compose down --remove-orphans --volumes || true'

                    // Build the images with no cache to ensure a fresh build
                    sh 'docker-compose build --no-cache'

                    // Start the services in detached mode
                    sh 'docker-compose up -d'

                    // Wait for backend to be up (check HTTP response from within the network)
                    sh '''
                        for i in {1..60}; do
                            # Run curl from a container on the same network
                            STATUS=$(docker run --rm --network contact_mynetwork curlimages/curl:8.10.1 curl -s -o /dev/null -w "%{http_code}" http://contact-backend-1:8000/admin/ || echo "0")
                            echo "Backend HTTP status (contact-backend-1): $STATUS"
                            if [ "$STATUS" = "200" ] || [ "$STATUS" = "302" ]; then
                                echo "Backend is up and running on contact-backend-1!"
                                break
                            fi

                            # Also try localhost:8001
                            STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/admin/ || echo "0")
                            echo "Backend HTTP status (localhost:8001): $STATUS"
                            if [ "$STATUS" = "200" ] || [ "$STATUS" = "302" ]; then
                                echo "Backend is up and running on localhost:8001!"
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
                        for i in {1..60}; do
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

                    // Verify the database file (it should already be in the workspace due to the volume mount)
                    sh 'ls -la backend/myproject/db.sqlite3 || echo "Database file not found."'
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