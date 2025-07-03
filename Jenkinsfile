pipeline {
    agent any

    environment {
        PROJECT_NAME = 'med-assistant-project'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Images') {
            steps {
                script {
                    sh 'docker compose build'
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh 'docker compose run --rm backend pytest'
                }
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploy step placeholder. Add your deployment logic here."
            }
        }
    }
}
