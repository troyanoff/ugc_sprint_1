#!/bin/bash

# Host and port of Kafka broker
KAFKA_HOST=${KAFKA_HOST}
KAFKA_PORT=${KAFKA_PORT}

# Timeout in seconds
TIMEOUT=${TIMEOUT:-60}

# Wait until Kafka is available or timeout is reached
echo "Waiting for Kafka to be available at ${KAFKA_HOST}:${KAFKA_PORT}..."

start_time=$(date +%s)
end_time=$((start_time + TIMEOUT))

while ! nc -z ${KAFKA_HOST} ${KAFKA_PORT}; do
  if [ $(date +%s) -ge ${end_time} ]; then
    echo "Timeout reached. Kafka is still not available."
    exit 1
  fi
  echo "Kafka is not available yet. Waiting..."
  sleep 2
done

# echo "Kafka is available. Starting Gunicorn..."
# exec gunicorn -b 0.0.0.0:5000 "src.app:create_app()"

echo "Kafka is available. Starting Gevent..."
exec python pywsgi.py
