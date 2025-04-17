#!/bin/bash

# Ensure MongoDB is running
sudo service mongod start

# Ensure Redis is running
sudo service redis-server start

# Ensure PostgreSQL is running
sudo service postgresql start

# Ensure Docker is running
sudo service docker start

# Ensure all necessary services are running
services=("mongod" "redis-server" "postgresql" "docker")
for service in "${services[@]}"; do
  if ! sudo service "$service" status > /dev/null; then
    echo "Error: $service is not running."
    exit 1
  fi
done

echo "All necessary services are running."
