#!/bin/bash

# Host and port of Kafka broker
KAFKA_HOST=${KAFKA_HOST}
KAFKA_PORT=${KAFKA_PORT}

# Host and port of ClickHouse node
CLICKHOUSE_HOST=${CLICKHOUSE_HOST}
CLICKHOUSE_PORT=${CLICKHOUSE_PORT}

# Timeout in seconds
TIMEOUT=${TIMEOUT:-60}

# Function to check service availability
check_service() {
  local host=$1
  local port=$2
  local service_name=$3
  local timeout=$4
  
  echo "Waiting for ${service_name} to be available at ${host}:${port}..."

  local start_time=$(date +%s)
  local end_time=$((start_time + timeout))

  while ! nc -z ${host} ${port}; do
    if [ $(date +%s) -ge ${end_time} ]; then
      echo "Timeout reached. ${service_name} is still not available."
      return 1
    fi
    echo "${service_name} is not available yet. Waiting..."
    sleep 2
  done

  echo "${service_name} is available."
  return 0
}

# Check Kafka availability
check_service ${KAFKA_HOST} ${KAFKA_PORT} "Kafka" ${TIMEOUT}
if [ $? -ne 0 ]; then
  exit 1
fi

# Check ClickHouse availability
check_service ${CLICKHOUSE_HOST} ${CLICKHOUSE_PORT} "ClickHouse" ${TIMEOUT}
if [ $? -ne 0 ]; then
  exit 1
fi

echo "Kafka and ClickHouse are available. Starting the application..."
exec poetry run python -m main.app
