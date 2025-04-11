pipeline {
    agent any
    options {
        timeout(time: 4, unit: 'MINUTES')
    }
    environment {
        // Hardcode your version choice here (either '1' or '2')
        APP_VERSION = '1'  // Change this to '2' if you want version 2
    }
    stages {
        stage('Cleanup') {
            steps {
                sh 'docker-compose down --remove-orphans --volumes || true'
            }
        }
        stage('Build') {
            steps {
                sh 'docker-compose build --no-cache'
            }
        }
        stage('Deploy') {
            steps {
                script {
                    if (env.APP_VERSION == '1') {
                        // Deploy version 1
                        sh 'docker-compose up -d backend'
                        echo 'Deploying version 1 at http://127.0.0.1:8000/'
                    } else {
                        // Deploy version 2
                        sh 'docker-compose up -d backend'
                        echo 'Deploying version 2 at http://127.0.0.1:8000/v2/'
                    }
                }
            }
        }
        stage('Verify Deployment') {
            steps {
                script {
                    if (env.APP_VERSION == '1') {
                        sh 'curl -sSf http://localhost:8000/ -o /dev/null || (echo "Version 1 not responding" && exit 1)'
                    } else {
                        sh 'curl -sSf http://localhost:8000/v2/ -o /dev/null || (echo "Version 2 not responding" && exit 1)'
                    }
                }
            }
        }
    }
    post {
        success {
            script {
                if (env.APP_VERSION == '1') {
                    echo 'Deployment successful! Access version 1 at: http://127.0.0.1:8000/'
                } else {
                    echo 'Deployment successful! Access version 2 at: http://127.0.0.1:8000/v2/'
                }
            }
        }
        failure {
            echo 'Deployment failed! Check logs for details.'
            sh 'docker-compose logs --no-color > failure.log'
            archiveArtifacts artifacts: 'failure.log', fingerprint: true
        }
    }
}