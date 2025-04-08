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
                    // Pre-create db.sqlite3 if it doesn't exist
                    sh 'mkdir -p backend/myproject && touch backend/myproject/db.sqlite3'
                    sh 'docker-compose build'
                    sh 'docker-compose down --remove-orphans || true'
                    sh 'docker-compose up -d'
                    sh '''
                        docker-compose exec -T backend python manage.py migrate
                        docker-compose exec -T backend python manage.py shell -c \
                            "from django.contrib.auth import get_user_model; \
                             User = get_user_model(); \
                             if not User.objects.filter(username='admin').exists(): \
                                 User.objects.create_superuser('admin', 'vslk.maanas@example.com', 'maanas6114')"
                    '''
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
        }
    }
}