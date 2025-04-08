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
                    // Build images (rely on cache)
                    sh 'docker-compose build'
                    // Stop and remove existing containers
                    sh 'docker-compose down --remove-orphans || true'
                    // Start containers
                    sh 'docker-compose up -d'
                    // Apply migrations and create superuser in one command
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