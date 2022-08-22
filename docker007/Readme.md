## What we learned in previous chapter
- Launch MySQL server using docker-compose
- Create a docker application that fetches the end of day price and store it in MySQL database
- Setup airflow and launch (and shutdown) airflow docker instance

## Current Chapter Scope
The grand finale where we tie everything together.  
Here we set up a workflow in airflow that runs the python application every evening at 23:00.
The application fetches the eod prices and stores the results in MySQL database.
The docker compose file: 
* launches MySQL server, 
* launches Airflow server,
* creates application docker image if it does not exist

Airflow launches docker instance of application that fetches the eod price of the 
ticker and save the results in MySQL database.

### Explanation of the directory structure
```
$ pwd  
/Users/me/Documents/Python/GitHub/docker-learn/docker007
$ ls -l
total 88
-rw-r--r--@  1 me  staff    647 23 Jul 22:47 Dockerfile <-- create docker container of application
-rw-r--r--   1 me  staff   2628 24 Jul 06:37 Readme.md <-- this file
-rw-r--r--@  1 me  staff  10222 12 Jul 15:54 airflow-docker-compose.yaml <-- compose file for Airflow
-rwxr-xr-x   1 me  staff   1110 12 Jul 14:27 airflow.sh <-- (not used) shell script to start airflow
drwxr-xr-x   3 me  staff     96 23 Jul 22:56 app <-- directory containing the python application code
drwxr-xr-x@  6 me  staff    192 23 Jul 22:26 dags <-- DAG code about the sequence of Airflow steps to carry out
drwxr-xr-x@ 33 me  staff   1056  6 Jul 23:20 db <-- created first time MySQL server is started and has DB files
-rwxr-xr-x   1 me  staff     70 23 Jul 21:59 down_docker.sh <-- shuts down docker
drwxr-xr-x   2 me  staff     64 23 Jul 21:46 input <-- (not used currently) to give input of tickers to download
drwxr-xr-x@ 10 me  staff    320 23 Jul 13:39 logs <-- airflow logs folder 
-rw-r--r--   1 me  staff    646  3 Jul 09:59 myapp-docker-compose.yaml <-- compose file for MySQL + our application
drwxr-xr-x   3 me  staff     96 23 Jul 22:58 output <-- output folder where docker files are stored
drwxr-xr-x@  2 me  staff     64 11 Jul 22:41 plugins <-- airflow directory
-rwxr-xr-x   1 me  staff     68 23 Jul 21:58 ps_docker.sh <-- shell script of docker status
-rw-r--r--@  1 me  staff    119 23 Jul 21:26 requirements.txt <-- python libaries to install 
-rwxr-xr-x   1 me  staff     68 23 Jul 21:58 up_docker.sh <-- shell script of starting docker
```
### Explanation of airflow-docker-compose.yaml & myapp-docker-compose.yaml
There are two docker-compose files instead of one
#### airflow-docker-compose.yaml
The file has been downloaded from the airflow 
[site](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html) using command 
`curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.3.3/docker-compose.yaml'`. It has been renamed 
to airflow-docker-compose.yaml to separate it from the other .yaml file in the directory. By default, 
this file is used to launch only Airflow.    
It has been customized as follows: Under section 'x-airflow-common' --> ' environment', 
environment variables for MySQL server like DB NAME, USER, PASSWORD etc. have been added.  
**NOTE: Another way to pass environment variables or setup DB connection 
is via the Airflow UI (localhost:8080) after starting the server**
* Adding variables connection ![Variables](screenshots/01_airflow_adding_variables.png) 
* Adding DB connection ![DB Connection](screenshots/02_airflow_adding_dbconnection.png) 
#### myapp-docker-compose.yaml
This is our file to do 3 things:
1. Create application docker image if it does not exist
2. 'mysql' service to start MySQL server
3. 'docker-proxy' service to has been added to resolve airflow permission bug that prevents it from running our docker app.   
Background: The Airflow uses 'DockerOperator' to run our docker container containing our docker app 'eod_price'. 
Running from within Airflow gives error 'permission denied'. To fix this problem, 
solution as [link](https://onedevblog.com/how-to-fix-a-permission-denied-when-using-dockeroperator-in-airflow/) is used.
In DAG/load_market_data.py, the docker_url='unix://var/run/docker.sock' has been replaced with docker_url='tcp://docker-proxy:2375'

### Explanation of up, ps and down script
Now we have two docker-compose files instead of one. 
In order to make the starting server, health check and stopping server easy we have 3 simple shell script  
- up_docker.sh
`docker-compose -f myapp-docker-compose.yaml -f airflow-docker-compose.yaml -p myapp up`
- ps_docker.sh
`docker-compose -f myapp-docker-compose.yaml -f airflow-docker-compose.yaml -p myapp ps`
- down_docker.sh
`docker-compose -f myapp-docker-compose.yaml -f airflow-docker-compose.yaml -p myapp down`

## Running Docker App in Airflow
1. Initialize the environment 
```  
$ mkdir -p ./dags ./logs ./plugins  
$ echo -e "AIRFLOW_UID=$(id -u)" > .env  
```
2. Initialize Airflow database 
**Note: setting airflow-docker-compose.yaml in AIRFLOW__CORE__LOAD_EXAMPLES: 'false' (to remove default example)**   
```
$ docker-compose up airflow-init  
```
3. Start Airflow  
```
$ ./up_docker.sh 
```
4. Check Airflow and MySQL server status 
```
$ ./ps_docker.sh 
          Name                         Command                  State                          Ports                    
------------------------------------------------------------------------------------------------------------------------
myapp_airflow-init_1        /bin/bash -c function ver( ...   Exit 0                                                     
myapp_airflow-scheduler_1   /usr/bin/dumb-init -- /ent ...   Up (healthy)   8080/tcp                                    
myapp_airflow-triggerer_1   /usr/bin/dumb-init -- /ent ...   Up (healthy)   8080/tcp                                    
myapp_airflow-webserver_1   /usr/bin/dumb-init -- /ent ...   Up (healthy)   0.0.0.0:8080->8080/tcp                      
myapp_airflow-worker_1      /usr/bin/dumb-init -- /ent ...   Up (healthy)   8080/tcp                                    
myapp_docker-proxy_1        socat TCP4-LISTEN:2375,for ...   Up             0.0.0.0:2376->2375/tcp                      
myapp_docker007_1           python eod_price.py TSLA - ...   Exit 0                                                     
myapp_postgres_1            docker-entrypoint.sh postgres    Up (healthy)   5432/tcp                                    
myapp_redis_1               docker-entrypoint.sh redis ...   Up (healthy)   6379/tcp                                    
myapp_mysql_1                  /entrypoint.sh mysqld            Up (healthy)   0.0.0.0:3306->3306/tcp, 33060/tcp, 33061/tcp
```
### Testing Docker Instance
#### Check docker app 'output to file' by running with -f flag
```
$ docker run -it --env-file .env --rm -v "$PWD"/output:/app_base/output docker007 python eod_price.py MSFT -f out.csv
os.getcwd: /app_base/app
__main__ ticker: MSFT, args.begin_date: None, args.end_date: None, , args.db: False, args.file: out.csv
fetch_price ticker: MSFT, start_date: 2022-08-20, end_date: 2022-08-21, data_src: yahoo, data_out: out.csv
           Ticker    High         Low        Open       Close    Volume  \
Date                                                                      
2022-08-19   MSFT  289.25  285.559998  288.899994  286.149994  20570033   

             Adj Close  
Date                    
2022-08-19  286.149994  
BEFORE>files in ../output/ directory: []
writing output to: /app_base/output/out.csv
AFTER>files in ../output/ directory: ['out.csv']
$ cat output/out.csv 
Date,Ticker,High,Low,Open,Close,Volume,Adj Close
2022-08-19,MSFT,289.25,285.55999755859375,288.8999938964844,286.1499938964844,20570033,286.1499938964844
```
#### Check docker app 'output to database' by running with -d flag
```
$ docker run -it --env-file .env --rm -v "$PWD"/output:/app_base/output docker007 python eod_price.py MMM -b 3 -d
os.getcwd: /app_base/app
__main__ ticker: MMM, args.begin_date: 3, args.end_date: None, , args.db: True, args.file: None
fetch_price ticker: MMM, start_date: 2022-08-18, end_date: 2022-08-21, data_src: yahoo, data_out: db
           Ticker        High         Low        Open       Close      Volume  \
Date                                                                            
2022-08-18    MMM  147.440002  145.380005  147.399994  146.679993   5654300.0   
2022-08-19    MMM  145.649994  143.210007  144.610001  145.199997  12712700.0   

             Adj Close  
Date                    
2022-08-18  145.189987  
2022-08-19  145.199997  
DB connection details DB_NAME: mktdb, DB_USR_NM: dbusr, DB_PORT: 3306
con_str: mysql+mysqlconnector://dbusr:upass@host.docker.internal/mktdb
2022-08-21 20:20:13,744 INFO sqlalchemy.engine.Engine SELECT DATABASE()
2022-08-21 20:20:13,744 INFO sqlalchemy.engine.Engine [raw sql] {}
2022-08-21 20:20:13,759 INFO sqlalchemy.engine.Engine SELECT @@sql_mode
2022-08-21 20:20:13,760 INFO sqlalchemy.engine.Engine [raw sql] {}
2022-08-21 20:20:13,765 INFO sqlalchemy.engine.Engine SELECT @@lower_case_table_names
2022-08-21 20:20:13,765 INFO sqlalchemy.engine.Engine [raw sql] {}
2022-08-21 20:20:13,802 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2022-08-21 20:20:13,814 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2022-08-21 20:20:13,814 INFO sqlalchemy.engine.Engine [generated in 0.00253s] {'table_schema': 'mktdb', 'table_name': 'eod_price'}
2022-08-21 20:20:13,823 INFO sqlalchemy.engine.Engine COMMIT
2022-08-21 20:20:13,851 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2022-08-21 20:20:13,853 INFO sqlalchemy.engine.Engine SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = %(table_schema)s AND table_name = %(table_name)s
2022-08-21 20:20:13,854 INFO sqlalchemy.engine.Engine [cached since 0.04222s ago] {'table_schema': 'mktdb', 'table_name': 'eod_price'}
2022-08-21 20:20:13,860 INFO sqlalchemy.engine.Engine ROLLBACK
2022-08-21 20:20:13,869 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2022-08-21 20:20:13,875 INFO sqlalchemy.engine.Engine INSERT INTO eod_price (`Date`, `Ticker`, `High`, `Low`, `Open`, `Close`, `Volume`, `Adj Close`) VALUES (%(Date)s, %(Ticker)s, %(High)s, %(Low)s, %(Open)s, %(Close)s, %(Volume)s, %(Adj Close)s)
2022-08-21 20:20:13,876 INFO sqlalchemy.engine.Engine [generated in 0.00327s] ({'Date': datetime.date(2022, 8, 18), 'Ticker': 'MMM', 'High': 147.44000244140625, 'Low': 145.3800048828125, 'Open': 147.39999389648438, 'Close': 146.67999267578125, 'Volume': 5654300.0, 'Adj Close': 145.1899871826172}, {'Date': datetime.date(2022, 8, 19), 'Ticker': 'MMM', 'High': 145.64999389648438, 'Low': 143.2100067138672, 'Open': 144.61000061035156, 'Close': 145.1999969482422, 'Volume': 12712700.0, 'Adj Close': 145.1999969482422})
2022-08-21 20:20:13,888 INFO sqlalchemy.engine.Engine COMMIT
```
### Testing Airflow
* login via browser  
> http://localhost:8080
> The default account login details:    
> __login:__ airflow   
> __password:__ airflow
* Running Sample Application by enabling dag     
![Enable the DAG to run](screenshots/01_enable_dag.png)
* Check run status (see description of each step in the image)
![Check the run status](screenshots/02_check_run_status.png)
* Verify output in MySQL Database    
**NOTE: This time using free app TablePlus to connect to database and checking contents**   
![Log window](screenshots/03_TablePlus_DB_output.png)
