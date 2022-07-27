## Running Airflow in Docker

https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html

_from above link_
### Initializing Environment
```  
mkdir -p ./dags ./logs ./plugins  
echo -e "AIRFLOW_UID=$(id -u)" > .env  
```

### Initialize the database
__NOTE:__ _To remove the sample examples that come with airflow in docker-compose.yaml set:  
AIRFLOW__CORE__LOAD_EXAMPLES: 'false' and then execute the command below_  
```
docker-compose up airflow-init  
```

### Running Airflow  
`docker-compose up`    
`docker-compose down`    

```
$ docker-compose ps
NAME                            COMMAND                  SERVICE             STATUS              PORTS
docker006-airflow-init-1        "/bin/bash -c 'funct…"   airflow-init        exited (0)          
docker006-airflow-scheduler-1   "/usr/bin/dumb-init …"   airflow-scheduler   running (healthy)   8080/tcp
docker006-airflow-triggerer-1   "/usr/bin/dumb-init …"   airflow-triggerer   running (healthy)   8080/tcp
docker006-airflow-webserver-1   "/usr/bin/dumb-init …"   airflow-webserver   running (healthy)   0.0.0.0:8080->8080/tcp
docker006-airflow-worker-1      "/usr/bin/dumb-init …"   airflow-worker      running (healthy)   8080/tcp
docker006-postgres-1            "docker-entrypoint.s…"   postgres            running (healthy)   5432/tcp
docker006-redis-1               "docker-entrypoint.s…"   redis               running (healthy)   6379/tcp
```



### Accessing the web interface
http://localhost:8080

The default account login details:    
__login:__ airflow   
__password:__ airflow

### Accessing the postgress DB
```
docker exec -it docker006-postgres-1  psql -d airflow -U airflow  
```
_NOTE: docker006-postgres-1 came from above above command docker-compose ps_
### Cleaning up
__To stop and delete containers, delete volumes with database data and download images, run:__
````
docker-compose down --volumes --rmi all
````

# ## Few Postgres SQL commands
https://www.postgresqltutorial.com/postgresql-administration/psql-commands/  
_from above link_  
```
login: psql -h host -d database -U user -W  
e.g. 
$ docker exec -it docker006-postgres-1 
$ psql  -d airflow -U airflow -W
list databases: \l  
list tables: \dt  
describe table: \d table_name
quit postgres: \q  
```


