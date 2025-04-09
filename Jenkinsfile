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

        stage('Build and Deploy') {
            steps {
                timeout(time: 120, unit: 'SECONDS') {
                    script {
                        sh 'docker-compose down --remove-orphans --volumes || true'
                        sh 'docker-compose build --no-cache'
                        sh 'docker-compose up -d'

                        // Health checks
                        sh '''
                            for i in {1..10}; do
                                if curl -s -f http://localhost:8000/admin/; then
                                    echo "Backend is up!"
                                    break
                                fi
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
    }

    post {
        always {
            sh 'docker-compose ps'
        }
        failure {
            sh 'docker-compose logs'
        }
    }
}