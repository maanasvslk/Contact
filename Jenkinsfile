pipeline {
    agent any
    options {
        timeout(time: 10, unit: 'MINUTES')
    }
    environment {
        APP_VERSION = '1'
        // Define paths (adjust as needed)
        LOCAL_SQLITE_SOURCE = "C:\\Users\\vslkm\\OneDrive\\Desktop\\Maanas\\KLU\\3-2\\Cloud Devops\\Cloud-Devops-Project\\backend\\myproject"
        WORKSPACE_SQLITE_TARGET = "${env.WORKSPACE}\\backend\\myproject"
    }
    stages {
        stage('Prepare SQLite Databases') {
            steps {
                script {

                    // Copy all SQLite files (silently overwrite if exists)
                    sh """
                        cp -f "${LOCAL_SQLITE_SOURCE}"/*.sqlite3 "${WORKSPACE_SQLITE_TARGET}/"
                        echo "Copied SQLite files:"
                        ls -la "${WORKSPACE_SQLITE_TARGET}"/*.sqlite3
                    """
                }
            }
        }

        // Existing stages below (unchanged)
        stage('Stop Existing Containers') {
            steps {
                sh 'docker-compose down || true'
            }
        }
        stage('Build') {
            steps {
                sh 'docker-compose build --no-cache'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose up -d'
                script {
                    def url = (env.APP_VERSION == '1') ?
                        'http://127.0.0.1:8000/' :
                        'http://127.0.0.1:8000/v2/'
                    echo "Deployed version ${env.APP_VERSION} at ${url}"
                }
            }
        }
    }
    post {
        always {
            sh 'docker-compose logs --tail 50 --no-color > docker.log'
            archiveArtifacts artifacts: 'docker.log'
        }
    }
}