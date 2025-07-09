pipeline {
    agent any

    environment {
        POSTGRES_DB = credentials('POSTGRES_DB')
        POSTGRES_USER = credentials('POSTGRES_USER')
        POSTGRES_PASSWORD = credentials('POSTGRES_PASSWORD')
        POSTGRES_HOST = credentials('POSTGRES_HOST')
        POSTGRES_PORT = credentials('POSTGRES_PORT')
    }

    stages {
        stage('Cloning GitHub repo to Jenkins') {
            steps {
                echo 'Cloning GitHub repo to Jenkins'
                checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-classic-token', url: 'https://github.com/LozinskiMatthew/med-assistant-project.git']])            }
        }

        stage('Generate .env file') {
            steps {
                echo 'Generating .env file from Jenkins credentials'
                sh """
                echo POSTGRES_DB=$POSTGRES_DB > .env
                echo POSTGRES_USER=$POSTGRES_USER >> .env
                echo POSTGRES_PASSWORD=$POSTGRES_PASSWORD >> .env
                echo POSTGRES_HOST=$POSTGRES_HOST >> .env
                echo POSTGRES_PORT=$POSTGRES_PORT >> .env
                cat .env
                """
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
