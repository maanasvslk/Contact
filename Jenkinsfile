pipeline {
    agent any

    options {
        timeout(time: 4, unit: 'MINUTES')
    }

    stages {
        stage('Build and Deploy with Docker Compose') {
            steps {
                // Shutdown any existing containers
                sh 'docker-compose down'

                // Build the services
                sh 'docker-compose build'

                // Start the services in detached mode
                sh 'docker-compose up -d'

                // Run migrations inside the backend container
                sh 'docker exec backend python /app/myproject/manage.py migrate'

                // Optionally, run other tasks like creating the superuser or tests
                // sh 'docker exec backend python /app/myproject/manage.py shell < create_superuser.py'
            }
        }
    }
}
