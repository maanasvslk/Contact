pipeline {
    agent any

    options {
        timeout(time: 4, unit: 'MINUTES')
    }

    stages {
        stage('Build and Deploy with Docker Compose') {
            steps {
                sh 'docker-compose down'
                sh 'docker-compose build'
                sh 'docker-compose up -d'
            }
        }
    }
}
