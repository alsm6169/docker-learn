## What we learned in previous chapter
- Launch MySQL server using docker-compose
- Create a docker application that fetches the end of day price and store it in MySQL database
- Setup airflow and launch (and shutdown) airflow docker instance

## Current Chapter Scope
The grand finale where we tie everything together.  
We have a workflow setup in airflow that runs the python application every evening at 23:00.
The application fetches the eod prices and stores the results in MySQL database.
The docker compose file launches MySQL server, it launches Airflow which in turn launches docker instance of 
application that fetches the eod price of the ticker and save the results in MySQL database.
```

$ pwd  
/Users/me/Documents/Python/GitHub/docker-learn/docker007
$ ls -l
total 88
-rw-r--r--@  1 me  staff    647 23 Jul 22:47 Dockerfile
-rw-r--r--   1 me  staff   2628 24 Jul 06:37 Readme.md
-rw-r--r--@  1 me  staff  10222 12 Jul 15:54 airflow-docker-compose.yaml
-rwxr-xr-x   1 me  staff   1110 12 Jul 14:27 airflow.sh
drwxr-xr-x   3 me  staff     96 23 Jul 22:56 app
drwxr-xr-x@  6 me  staff    192 23 Jul 22:26 dags
drwxr-xr-x@ 33 me  staff   1056  6 Jul 23:20 db
-rwxr-xr-x   1 me  staff     70 23 Jul 21:59 down_docker.sh
drwxr-xr-x   2 me  staff     64 23 Jul 21:46 input
drwxr-xr-x@ 10 me  staff    320 23 Jul 13:39 logs
-rw-r--r--   1 me  staff    646  3 Jul 09:59 myapp-docker-compose.yaml
drwxr-xr-x   3 me  staff     96 23 Jul 22:58 output
drwxr-xr-x@  2 me  staff     64 11 Jul 22:41 plugins
-rwxr-xr-x   1 me  staff     68 23 Jul 21:58 ps_docker.sh
-rw-r--r--@  1 me  staff    119 23 Jul 21:26 requirements.txt
-rwxr-xr-x   1 me  staff     68 23 Jul 21:58 up_docker.sh
```
### Creating Docker Instance  
docker build -t eod_price .

### Testing Docker Instance  
docker run --rm -v "$PWD"/output:/app_base/output eod_price:latest python eod_price.py ACN -b 7 -f out.csv

### check and remove instance
docker ps -a
docker rmi eod_price


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


