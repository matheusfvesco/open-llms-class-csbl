#!/bin/bash
echo "Removing repositories..."
rm -rf open-webui
rm -rf cohere-terrarium

# Remove all Docker containers
echo "Removing all Docker containers..."
docker ps -aq | while read -r container_id; do
  echo "Removing container $container_id"
  docker rm -f "$container_id"
done

# Remove all Docker volumes
echo "Removing all Docker volumes..."
docker volume ls -q | while read -r volume_name; do
  echo "Removing volume $volume_name"
  docker volume rm "$volume_name"
done

echo "All containers and volumes have been removed."
