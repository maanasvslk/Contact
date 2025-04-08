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
                    sh 'docker-compose build'
                    // Run a temporary container to create db.sqlite3
                    sh '''
                        docker-compose run --rm backend python manage.py migrate
                        docker-compose run --rm backend python manage.py shell -c \
                            "from django.contrib.auth import get_user_model; \
                             User = get_user_model(); \
                             if not User.objects.filter(username='admin').exists(): \
                                 User.objects.create_superuser('admin', 'vslk.maanas@example.com', 'maanas6114')"
                    '''
                    sh 'docker-compose down --remove-orphans || true'
                    sh 'docker-compose up -d'
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