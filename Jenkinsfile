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
                    timeout(time: 35, unit: 'SECONDS') {
                        sh 'docker-compose down --remove-orphans --volumes || true'
                        sh 'docker-compose build --no-cache'
                        sh 'docker-compose up -d'

                        // Quicker health check
                        sh '''
                            for i in {1..7}; do  # 7 tries * 3s = 21s max
                                if curl -s -f http://localhost:8000/admin/; then
                                    echo "Backend is up!"
                                    exit 0
                                fi
                                sleep 3
                            done
                            echo "Backend failed to start!"
                            exit 1
                        '''
                    }
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