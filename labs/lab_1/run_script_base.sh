#!/bin/bash

# lab1 run.sh script
# Author: xxxxxxxx

# Start Script

# Build docker image
echo "Building Docker Image"
...
echo "========================================="

# Run built docker image
echo "Running Built Docker Image"
...
echo "========================================="

# Test Endpoints
echo "Testing Endpoints"
echo "testing '/hello' endpoint with ?name=Winegar, expectiong (???)"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/hello?name=Winegar"

echo "testing '/' endpoint, expectiong (???) "
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/"

echo "testing '/docs' endpoint, expectiong (???)"
curl -o /dev/null -s -w "%{http_code}\n" -X GET "http://localhost:8000/docs"

echo "========================================="

# Stop and Remove the running container
echo "Stopping the running container"
...

echo "Remove the container"
...

echo "========================================="

# Delete the built image
echo "Deleting built image"
...
