#!/bin/bash

IMAGE_NAME="itu-fastapi-app"

echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# Check if the build was successful
if [ $? -ne 0 ]; then
    echo "Docker build failed. Exiting."
    exit 1
fi

echo "Running Docker container..."
docker run -p 8000:8000 $IMAGE_NAME
