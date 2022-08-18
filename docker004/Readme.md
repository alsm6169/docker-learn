## What we learned in previous chapter
- We created a python application to fetch the close price of the stock ticker and either display 
on screen or write to a file.  

## Current Chapter Scope
In this chapter we will only work with MySQL containter. We will download the MySQL server instance from 
a. command line
b. docker compose file
This will be the first introduction to using docker compose file

## Manually getting the MySQL container, starting it 
### download the mysql server
`$ docker pull mysql/mysql-server:8.0`

### complex way to start mysql server with auto generated password
[reference link](https://dev.mysql.com/doc/refman/8.0/en/docker-mysql-getting-started.html)
```
$ docker run --name=mysql1 --restart on-failure -d mysql/mysql-server
#to get the auto generated password
$ docker logs mysql1 2>&1 | grep GENERATED
```

### easier way to run the mysql server with setting root password at start
```
docker run --name=mysql2 -e MYSQL_ROOT_PASSWORD=rsecret -d mysql/mysql-server:8.0
docker exec -it mysql2 bash
#once inside the container
mysql -uroot -p
#put/paste the password (here it is 'rsecret' as specified above, and once inside MySQL CLI run
#Note: above does not specify volume, so all will be lost
```

### ANOTHER way with both a root user and a non-root user
[reference link](https://citizix.com/how-to-run-mysql-8-with-docker-and-docker-compose/)
```
$ docker run -d \
    --name mysql-inst \
    -p 3306:3306 \
    -v $(pwd)/db:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=rpass \
    -e MYSQL_DATABASE=mktdb \
    -e MYSQL_USER=dbusr \
    -e MYSQL_PASSWORD=upass \
    mysql/mysql-server:8.0
```

## Using docker-compose to get the MySQL container, starting it 
[reference link](https://docs.docker.com/compose/)
### What is docker compose?
(from the reference link above)
> Compose is a tool for defining and running multi-container Docker applications. 
> With Compose, you use a YAML file to configure your application’s services. 
> Then, with a single command, you create and start all the services from your configuration. 

### some useful docker-compose commands
1. starting the servers in compose file  
`$ docker-compose up -d`
2. checking the status of the servers started by docker compose  
`$ docker-compose ps`
3. stopping all the servers in docker compose  
`$ docker-compose exec mysql bash`  

**Long docker commands to start server no longer needs to be typed and 
are stored in a yaml file with the ability to have comments**

## basic sql commands
[reference link](https://devhints.io/mysql)
```
# show databases;   
# USE database_name;   
# show tables;   
# describe table_name;  
# select version();  
# create table price(ticker char(30), eod_date date, close float);  
# insert into price(ticker, eod_date, close) values ('GOOG', curdate(), 100.1);  
# select * from price;  
```

### creating table from sql prompt
1. start the mysql server
Use `docker-compose up` or above `docker run -d \....` to start the mysql server
2. log into the mysql server
`$ docker exec -it mysql-inst bash`
3. log into sql
Option 1
`# mysql -u root -p`
Option 2
**Note: below that -p and password usecret are stuck together without space in between**
`# mysql -u data_usr -prpass`
4. select database --> create table --> insert into table --> view the contents of the table
```
bash-4.4# mysql -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 10
Server version: 8.0.29 MySQL Community Server - GPL

Copyright (c) 2000, 2022, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> create table price(ticker char(30), eod_date date, close float);  
ERROR 1046 (3D000): No database selected
mysql> use mktdb
Database changed
mysql> create table price(ticker char(30), eod_date date, close float);  
Query OK, 0 rows affected (0.05 sec)

mysql> insert into price(ticker, eod_date, close) values ('GOOG', curdate(), 100.1);  
Query OK, 1 row affected (0.02 sec)

mysql> select * from price;  
+--------+------------+-------+
| ticker | eod_date   | close |
+--------+------------+-------+
| GOOG   | 2022-08-18 | 100.1 |
+--------+------------+-------+
1 row in set (0.01 sec)

mysql> 
```

