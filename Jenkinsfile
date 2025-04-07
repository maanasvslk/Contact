// Jenkinsfile
pipeline {
    agent any

    environment {
        VERSION = 'v2'  // Set to v2 for this deployment
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
                    sh 'docker-compose down --remove-orphans'  // Preserve the volume
                    sh 'docker-compose up -d'
                    // Create versioned databases
                    sh '''
                        # Rename the existing mydb_main to mydb_v1 if this is the first v2 deployment
                        docker-compose exec -T db psql -U postgres -d postgres -c "ALTER DATABASE mydb_main RENAME TO mydb_v1;" || true
                        # Recreate mydb_main for default Django apps
                        docker-compose exec -T db psql -U postgres -d postgres -c "CREATE DATABASE mydb_main;" || true
                        # Create mydb_v2 for the new version
                        docker-compose exec -T db psql -U postgres -d postgres -c "CREATE DATABASE mydb_v2;" || true
                    '''
                }
            }
        }

        stage('Apply Migrations') {
            steps {
                script {
                    sh 'sleep 10'  // Wait for the database to be ready
                    // Generate new migrations if needed
                    sh 'docker-compose exec -T backend python manage.py makemigrations'
                    // Apply migrations to the default database (mydb_main) for Django's built-in apps
                    sh 'docker-compose exec -T backend python manage.py migrate --database=default'
                    // Do NOT apply migrations to mydb_v1 to preserve its schema
                    // Apply migrations to mydb_v2 for the new version
                    sh 'docker-compose exec -T backend python manage.py migrate --database=mydb_v2'
                    // Create superuser in the default database (if not exists)
                    sh '''
                        docker-compose exec -T backend python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'vslk.maanas@example.com', 'maanas6114') if not User.objects.filter(username='admin').exists() else print('Superuser already exists, skipping creation.')"
                    '''
                }
            }
        }

        stage('Test Application') {
            steps {
                script {
                    echo 'Running tests...'
                    // Add test commands if needed
                }
            }
        }
    }

    post {
        success {
            echo "Deployment completed successfully for version ${env.VERSION}."
        }
        failure {
            echo "Deployment failed for version ${env.VERSION}."
        }
    }
}