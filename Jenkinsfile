pipeline {
    agent any
    options {
        timeout(time: 10, unit: 'MINUTES')
    }
    environment {
        COMPOSE_PROJECT_NAME = 'contact-app'
    }
    stages {
        stage('Cleanup') {
            steps {
                sh 'docker-compose down -v || true'
            }
        }
        stage('Build') {
            steps {
                sh 'docker-compose build --no-cache'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose up -d'
                // Wait for container to be ready
                sh '''
                for i in {1..30}; do
                    if docker ps --filter "name=contact-app-backend-1" --format "{{.Status}}" | grep -q "Up"; then
                        echo "Container is running"
                        break
                    fi
                    echo "Waiting for container to start... ($i/30)"
                    sleep 2
                done
                '''
            }
        }
        stage('Verify') {
            steps {
                sh '''
                # Wait for server to respond
                for i in {1..30}; do
                    if curl -sSf http://localhost:8000/ -o /dev/null; then
                        echo "Server is responding"
                        break
                    fi
                    echo "Waiting for server to respond... ($i/30)"
                    sleep 2
                done
                '''
            }
        }
    }
    post {
        always {
            sh 'docker-compose logs --tail 100 --no-color > docker.log'
            archiveArtifacts artifacts: 'docker.log'
        }
        failure {
            echo "Deployment failed - checking container status..."
            sh '''
            docker ps -a > containers.txt
            docker inspect contact-app-backend-1 > inspect.txt
            '''
            archiveArtifacts artifacts: 'containers.txt,inspect.txt'
        }
    }
}