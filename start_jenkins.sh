#!/bin/bash

docker compose -f docker-compose.jenkins.yml up --build -d

echo "Waiting for Jenkins to initialize..."

while ! docker exec jenkins test -f /var/jenkins_home/secrets/initialAdminPassword; do
    echo "Still waiting for Jenkins to be ready..."
    sleep 5
done

echo "Fetching Jenkins initial password:"
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword

xdg-open http://localhost:8080
