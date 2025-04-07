pipeline {
    agent any

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
                    sh "docker-compose down -v --remove-orphans || true"
                    sh "docker-compose up -d"
                }
            }
        }

        stage('Apply Migrations') {
            steps {
                script {
                    sh 'sleep 10'
                    sh 'docker-compose exec -T backend python manage.py makemigrations'
                    sh 'docker-compose exec -T backend python manage.py migrate'
                    sh 'docker-compose exec -T backend python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(\'admin\', \'vslk.maanas@example.com\', \'maanas6114\') if not User.objects.filter(username=\'admin\').exists() else print(\'Superuser already exists, skipping creation.\')"'
                }
            }
        }

        stage('Test Application') {
            steps {
                script {
                    echo "Running tests..."
                }
            }
        }
    }

    post {
        success {
            echo "Deployment completed successfully for version ${VERSION}."
        }
        failure {
            echo "Deployment failed for version ${VERSION}."
            sh 'docker-compose logs backend'
            sh 'docker-compose logs db'
        }
    }
}