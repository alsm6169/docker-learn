#!/usr/bin/env bash
# docker-compose -f myapp-docker-compose.yaml -f airflow-docker-compose.yaml -p myapp ps
docker-compose -f airflow-docker-compose.yaml ps
