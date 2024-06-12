#!/bin/bash

# Stop and remove the existing container
docker stop tpintrods
docker rm tpintrods

# Remove the volume
docker volume rm tp_intro_db_data

# Rebuild and restart the container
docker-compose up --build
