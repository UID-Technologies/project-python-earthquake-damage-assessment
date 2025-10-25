#!/bin/bash

# Build and Push Script for Earthquake Damage Assessment Tool
# Usage: ./build-and-push.sh [version]

set -e

DOCKER_USERNAME="varungupta2809"
IMAGE_NAME="earthquake-damage-assessment"
VERSION=${1:-"latest"}

echo "🔨 Building Docker image..."
docker build -t ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION} .

if [ "$VERSION" != "latest" ]; then
    echo "🏷️  Tagging as latest..."
    docker tag ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION} ${DOCKER_USERNAME}/${IMAGE_NAME}:latest
fi

echo "📊 Image size:"
docker images ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}

echo ""
read -p "🚀 Push to Docker Hub? (y/N): " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔐 Logging in to Docker Hub..."
    docker login
    
    echo "📤 Pushing ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}..."
    docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}
    
    if [ "$VERSION" != "latest" ]; then
        echo "📤 Pushing ${DOCKER_USERNAME}/${IMAGE_NAME}:latest..."
        docker push ${DOCKER_USERNAME}/${IMAGE_NAME}:latest
    fi
    
    echo "✅ Successfully pushed to Docker Hub!"
    echo "🔗 View at: https://hub.docker.com/r/${DOCKER_USERNAME}/${IMAGE_NAME}"
else
    echo "⏭️  Skipping push to Docker Hub"
fi

echo ""
echo "🎉 Done! You can now run:"
echo "   docker run -d -p 5000:5000 ${DOCKER_USERNAME}/${IMAGE_NAME}:${VERSION}"

