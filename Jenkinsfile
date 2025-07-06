pipeline {
    agent any

    environment {
        PROJECT_NAME = 'med-assistant-project'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Github checkout'
                checkout scm
            }
        }

        stage('Build Docker Images') {

            steps {
                script {
                    echo 'Building and starting Docker containers'
                    sh 'docker compose -f docker-compose.yml up --build'
                }
            }
        }
    }
}
