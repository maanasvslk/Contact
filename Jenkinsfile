pipeline {
    agent any

    environment {
        VERSION = 'V2'
    }
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
                sh 'ls -R backend/myproject'
            }
        }
        stage('Build Docker Images') {
            steps {
                script {
                    sh 'docker-compose build --no-cache'
                }
            }
        }
        stage('Deploy Containers') {
            steps {
                script {
                    sh 'docker-compose down -v --remove-orphans' // Reset volume as in current pipeline
                    sh 'docker-compose up -d'
                }
            }
        }
        stage('Apply Migrations') {
            steps {
                script {
                    // Wait for database readiness
                    sh 'sleep 10'
                    // Apply migrations with retry logic
                    sh '''
                        for i in {1..3}; do
                            docker-compose exec -T backend python manage.py migrate && break
                            echo "Migration attempt $i failed, retrying..."
                            sleep 5
                        done
                    '''
                    // Create superuser using createsuperuser --noinput for reliability
                    sh '''
                        docker-compose exec -T backend python manage.py createsuperuser --noinput --username admin --email vslk.maanas@example.com --password maanas6114 || echo "Superuser creation skipped (likely already exists)"
                    '''
                }
            }
        }
        stage('Test Application') {
            steps {
                echo 'Testing application (placeholder)'
                // Add your test commands here if applicable
            }
        }
    }
    post {
        failure {
            echo "Deployment failed for version with phone_number field."
            sh 'docker-compose logs backend'
            sh 'docker-compose logs db'
        }
    }
}