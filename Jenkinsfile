pipeline {
    agent any
    options {
        timeout(time: 4, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '5'))
    }
    environment {
        APP_VERSION = '1'  // Hardcoded version
        COMPOSE_PROJECT_NAME = 'cd-project'  // Prevent naming conflicts
    }
    stages {
        stage('Cleanup') {
            steps {
                sh '''
                docker-compose down --remove-orphans --volumes --timeout 1 || true
                docker system prune -f  # Clean up dangling resources
                '''
            }
        }
        stage('Build') {
            steps {
                sh 'docker-compose build --no-cache --pull'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose up -d backend'
                script {
                    def url = (env.APP_VERSION == '1') ?
                        'http://127.0.0.1:8000/' :
                        'http://127.0.0.1:8000/v2/'
                    echo "Deploying version ${env.APP_VERSION} at ${url}"
                }
            }
        }
        stage('Verify Deployment') {
            steps {
                script {
                    def endpoint = (env.APP_VERSION == '1') ? '/' : '/v2/'
                    def healthy = false

                    // Wait for container to be healthy
                    for (int i = 0; i < 30; i++) {
                        def health = sh(
                            script: "docker inspect --format='{{.State.Health.Status}}' cd-project-backend-1",
                            returnStdout: true
                        ).trim()

                        if (health == 'healthy') {
                            healthy = true
                            break
                        }
                        sleep(5)
                    }

                    // Verify endpoint
                    if (healthy) {
                        sh "curl -sSf http://localhost:8000${endpoint} -o /dev/null"
                        echo "Version ${env.APP_VERSION} is responding successfully!"
                    } else {
                        error("Deployment failed - container did not become healthy")
                    }
                }
            }
        }
    }
    post {
        always {
            sh 'docker-compose logs --no-color --tail 100 > docker.log'
            archiveArtifacts artifacts: 'docker.log', fingerprint: true
        }
        success {
            script {
                def url = (env.APP_VERSION == '1') ?
                    'http://127.0.0.1:8000/' :
                    'http://127.0.0.1:8000/v2/'
                echo "SUCCESS: Version ${env.APP_VERSION} deployed to ${url}"
            }
        }
        failure {
            slackSend color: 'danger', message: "Deployment failed: ${env.JOB_NAME} #${env.BUILD_NUMBER}"
        }
    }
}