# Microservice implementation of URL Shortener

This is a microservices-based URL shortener application built using Python, Flask, Redis, and Docker. The application is divided into two services: a shortening service and an analytics service.

## Prerequisites

- Docker
- Kubernetes (Kind, or any other Kubernetes cluster)
- kubectl

## Setup

### Step 1: Build and Run with Docker

1. **Build the Docker images:**

    ```sh
    docker build -t shortening-service:latest -f Dockerfile.shortening_service .
    docker build -t analytics-service:latest -f Dockerfile.analytics_service .
    ```

2. **Run the Docker containers:**

    ```sh
    docker run -d -p 5001:5001 --name shortening-service shortening-service:latest
    docker run -d -p 5002:5002 --name analytics-service analytics-service:latest
    ```

3. **Access the application:**

    - Shortening Service: Open your browser and navigate to `http://localhost:5001`.
    - Analytics Service: Open your browser and navigate to `http://localhost:5002`.

### Step 2: Deploy to Kubernetes using Kind

1. **Create a Kind cluster:**

    ```sh
    kind create cluster
    ```

2. **Load the Docker images into the Kind cluster:**

    ```sh
    kind load docker-image shortening-service:latest
    kind load docker-image analytics-service:latest
    ```

3. **Apply the Redis deployment and service:**

    ```sh
    kubectl apply -f redis.yaml
    ```

4. **Apply the Shortening Service deployment and service:**

    ```sh
    kubectl apply -f shortening_service.yaml
    ```

5. **Apply the Analytics Service deployment and service:**

    ```sh
    kubectl apply -f analytics_service.yaml
    ```

6. **Get the URL of the Shortening Service:**

    ```sh
    kubectl port-forward service/shortening-service 8081:80
    ```

7. **Get the URL of the Analytics Service:**

    ```sh
    kubectl port-forward service/analytics-service 8082:80
    ```

8. **Access the application:**

    - Shortening Service: Open your browser and navigate to `http://localhost:8081`.
    - Analytics Service: Open your browser and navigate to `http://localhost:8082`.

## Application Structure

- `shortening_service.py`: The Flask application for the shortening service.
- `analytics_service.py`: The Flask application for the analytics service.
- `templates/index.html`: The HTML template for the home page.
- `redis.yaml`: Kubernetes configuration for the Redis deployment and service.
- `shortening_service.yaml`: Kubernetes configuration for the shortening service deployment and service.
- `analytics_service.yaml`: Kubernetes configuration for the analytics service deployment and service.
- `Dockerfile.shortening_service`: Dockerfile to build the Docker image for the shortening service.
- `Dockerfile.analytics_service`: Dockerfile to build the Docker image for the analytics service.

## Endpoints

### Shortening Service

- `POST /shorten`: Endpoint to shorten a URL.

### Analytics Service

- `GET /redirect/<short_code>`: Endpoint to redirect to the original URL and track clicks.

## Environment Variables

- `REDIS_HOST`: The hostname of the Redis server (default: `localhost`).
- `REDIS_PORT`: The port of the Redis server (default: `6379`).