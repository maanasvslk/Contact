pipeline {
    agent any
    options {
        timeout(time: 10, unit: 'MINUTES')
    }
    environment {
        APP_VERSION = '1' // Change this to switch versions
    }
    stages {
        stage('Stop and Clean') {
            steps {
                // Remove containers but KEEP volumes
                sh 'docker-compose down || true'

                // Only remove the backend volumes if needed
                sh 'docker volume rm -f cd-project_node_modules || true'
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
                    sleep(time: 10, unit: 'SECONDS')
                }
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