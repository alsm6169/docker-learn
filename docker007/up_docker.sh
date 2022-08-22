#!/usr/bin/env bash
# https://stackoverflow.com/questions/48717646/docker-compose-down-with-a-non-default-yml-file-name
docker-compose -f myapp-docker-compose.yaml -f airflow-docker-compose.yaml -p myapp up
# docker-compose -f airflow-docker-compose.yaml up