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
                script {
                    // Wait up to 2 minutes for server
                    def healthy = false
                    for (int i = 0; i < 24; i++) { // 24 attempts * 5s = 2 minutes
                        try {
                            sh "curl -sSf http://localhost:8000/ --connect-timeout 5"
                            healthy = true
                            break
                        } catch (Exception e) {
                            echo "Waiting for server... (attempt ${i+1}/24)"
                            sleep(5)
                        }
                    }
                    if (!healthy) {
                        error("Server failed to start within 2 minutes")
                    }
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