pipeline {
    agent any

    environment {
        DOCKER_BUILDKIT = 1
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Files') {
            steps {
                sh 'ls -la backend/'
                sh 'ls -la backend/myproject/'
                sh 'cat backend/init-superuser.sh'
            }
        }

        stage('Build and Deploy') {
            steps {
                timeout(time: 120, unit: 'SECONDS') {
                    script {
                        sh 'docker-compose down --remove-orphans --volumes || true'
                        sh 'docker-compose build --no-cache'
                        sh 'docker-compose up -d'

                     // Health check with retries
                        sh '''
                            for i in {1..20}; do
                                if curl -s -f http://localhost:8001/admin/; then
                                    echo "Backend is up!"
                                    break
                                fi
                                echo "Waiting for backend... (attempt $i)"
                                sleep 5
                            done

                            for i in {1..10}; do
                                if curl -s -f http://localhost:3000; then
                                    echo "Frontend is up!"
                                    exit 0
                                fi
                                sleep 5
                            done
                            echo "Services failed to start!"
                            exit 1
                        '''
                    }
                }
            }
        }

    post {
        always {
            sh 'docker-compose ps'
            sh 'docker-compose logs backend || true'
        }
        failure {
            sh 'docker-compose logs'
            sh 'docker exec contact-backend-1 ls -la /app || true'
        }
    }
}