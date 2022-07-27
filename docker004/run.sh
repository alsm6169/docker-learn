docker pull mysql/mysql-server:8.0

# complex way with auto set password
# https://dev.mysql.com/doc/refman/8.0/en/docker-mysql-getting-started.html
docker run --name=mysql1 --restart on-failure -d mysql/mysql-server
#to get the auto generated password
docker logs mysql1 2>&1 | grep GENERATED

#easier way with setting root password at start
docker run --name=mysql2 -e MYSQL_ROOT_PASSWORD=rsecret -d mysql/mysql-server:8.0
docker exec -it mysql2 bash
#once inside the container
mysql -uroot -p
#put/paste the password (here it is 'rsecret' as specified above, and once inside MySQL CLI run
#Note: above does not specify volume, so all will be lost

# ANOTHER way with both a root user and a non-root user
# https://citizix.com/how-to-run-mysql-8-with-docker-and-docker-compose/
docker run -d \
    --name mysql3 \
    -p 3306:3306 \
    -v $(pwd)/db:/var/lib/mysql \
    -e MYSQL_ROOT_PASSWORD=rsecret \
    -e MYSQL_DATABASE=data_db \
    -e MYSQL_USER=data_usr \
    -e MYSQL_PASSWORD=usecret \
    mysql/mysql-server:8.0

docker exec -it mysql3 bash

mysql -u root -p
# not below that -p and password usecret are stuck together without space in between
mysql -u data_usr -pusecret

docker volume ls
docker volume rm db

# using docker-compose
docker-compose up -d
docker-compose ps
docker-compose exec mysql bash

# sql commands
# https://devhints.io/mysql
show databases;
USE database_name;
show tables;
describe table_name;
select version();

create table price (ticker char(30), eod_date date, close float);
insert into price(ticker, eod_date, close) values ('GOOG', curdate(), 100.1);
select * from price;


