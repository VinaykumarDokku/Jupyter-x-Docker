#!/usr/bin/env bash
set -euo pipefail

echo "Starting Jupyter container..."
docker compose up --build -d

trap 'docker compose down' EXIT

echo "Waiting for JupyterLab..."

for i in $(seq 1 60); do
    if curl -fsS -L http://127.0.0.1:8888/lab > /dev/null; then
        echo "JupyterLab is available."
        break
    fi

    if [ "$i" -eq 60 ]; then
        echo "JupyterLab failed to start."
        exit 1
    fi

    sleep 5
done

echo "Checking container health..."

for i in $(seq 1 30); do
    STATUS=$(docker inspect --format '{{.State.Health.Status}}' jupyter-docker)

    if [ "$STATUS" = "healthy" ]; then
        break
    fi

    if [ "$i" -eq 30 ]; then
        echo "Container health check failed."
        exit 1
    fi

    sleep 5
done

echo "Testing persistent storage..."

docker compose exec -T jupyter sh -c \
    'echo integration-test > /app/notebooks/.integration-test'

docker compose up -d --force-recreate

docker compose exec -T jupyter sh -c \
    'grep -qx integration-test /app/notebooks/.integration-test && rm /app/notebooks/.integration-test'

echo "All integration tests passed."
