pipeline {
    agent any
    options {
        timeout(time: 10, unit: 'MINUTES')  // More generous timeout
    }
    environment {
        APP_VERSION = '1'  // Hardcoded version
    }
    stages {
        stage('Stop Existing Containers') {
            steps {
                sh 'docker-compose down -v || true'  // -v removes volumes but skips image pruning
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
                script {
                    def url = (env.APP_VERSION == '1') ?
                        'http://127.0.0.1:8000/' :
                        'http://127.0.0.1:8000/v2/'
                    echo "Deployed version ${env.APP_VERSION} at ${url}"
                }
            }
        }
        stage('Verify') {
            steps {
                sh '''
                # Check container status
                docker ps -a
                # Get logs
                docker-compose logs --tail=100
                # Check if server is running
                curl -v http://localhost:8000 || true
                # Check files in container
                docker exec -it $(docker-compose ps -q backend) ls -la /app
                docker exec -it $(docker-compose ps -q backend) ls -la /app/myproject
                '''
            }
        }
    }
    post {
        always {
            sh 'docker-compose logs --tail 50 --no-color > docker.log'
            archiveArtifacts artifacts: 'docker.log'
        }
    }
}