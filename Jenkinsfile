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
                    // Run migrations without  volume mount and copy db.sqlite3 to host
                    sh '''
                        docker run --rm contact-backend python manage.py migrate
                        docker run --rm -v $(pwd)/backend/myproject:/app/myproject contact-backend \
                            bash -c "cp /app/myproject/db.sqlite3 /app/myproject/db.sqlite3.host && mv /app/myproject/db.sqlite3.host /app/myproject/db.sqlite3"
                        chmod 666 backend/myproject/db.sqlite3
                    '''
                    // Create superuser
                    sh '''
                        docker run --rm contact-backend python manage.py shell -c \
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
            sh 'ls -la backend/myproject/'
        }
    }
}