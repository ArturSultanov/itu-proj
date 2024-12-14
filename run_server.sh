#!/bin/bash

IMAGE_NAME="itu-fastapi-app"
CONTAINER_NAME="itu-backend-container"

# Check if a container with the same name already exists
if [ $(docker ps -aq -f name=$CONTAINER_NAME) ]; then
    echo "Stopping and removing existing container with the same name..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# Check if the build was successful
if [ $? -ne 0 ]; then
    echo "Docker build failed. Exiting."
    exit 1
fi

echo "Running Docker container..."
docker run -p 8000:8000 --name $CONTAINER_NAME $IMAGE_NAME
