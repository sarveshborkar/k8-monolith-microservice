# Monotlithic implementation of URL Shortener

This is a monolithic URL shortener application built using Python, Flask, Redis, and Docker. The application allows users to shorten URLs and tracks the number of times each shortened URL is accessed.

## Prerequisites

- Docker
- Kubernetes (Kind, or any other Kubernetes cluster)
- kubectl

## Setup

### Step 1: Build and Run with Docker

1. **Build the Docker image:**

    ```sh
    docker build -t url-shortener:v2 .
    ```

2. **Run the Docker container:**

    ```sh
    docker run -d -p 5000:5000 --name url-shortener url-shortener:v2
    ```

3. **Access the application:**

    Open your browser and navigate to `http://localhost:5000`.

### Step 2: Deploy to Kubernetes using Kind

1. **Create a Kind cluster:**

    ```sh
    kind create cluster
    ```

2. **Load the Docker image into the Kind cluster:**

    ```sh
    kind load docker-image url-shortener:v2
    ```

3. **Apply the Redis deployment and service:**

    ```sh
    kubectl apply -f monolith/redis.yaml
    ```

4. **Apply the URL shortener deployment and service:**

    ```sh
    kubectl apply -f monolith/app.yaml
    ```

5. **Get the URL of the URL shortener service:**

    ```sh
    kubectl port-forward service/url-shortener 8080:80
    ```

6. **Access the application:**

    Open your browser and navigate to `http://localhost:8080`.

## Application Structure

- `monolith/app.py`: The main Flask application.
- `monolith/templates/index.html`: The HTML template for the home page.
- `monolith/redis.yaml`: Kubernetes configuration for the Redis deployment and service.
- `monolith/app.yaml`: Kubernetes configuration for the URL shortener deployment and service.
- `monolith/Dockerfile`: Dockerfile to build the Docker image for the application.

## Endpoints

- `GET /`: Home page with the URL shortening form.
- `POST /shorten`: Endpoint to shorten a URL.
- `GET /<short_code>`: Endpoint to redirect to the original URL and track clicks.

## Environment Variables

- `REDIS_HOST`: The hostname of the Redis server (default: `localhost`).
- `REDIS_PORT`: The port of the Redis server (default: `6379`).
