## Docker-compose commands  
```
docker-compose up -d  
docker-compose ps  
docker-compose exec mysql bash
```

## SQL commands  
```mysql -u root -p```  
 __Note: below -p and password tst are stuck together without space in between__  
```mysql -u dbusr -ptst```

https://devhints.io/mysql  
### DB Level Commands
```
show databases;  
USE database_name;  
show tables;  
describe table_name;  
select version();  
```

### Simple SQL Queries
```
create table price (ticker char(30), eod_date date, close float);  
insert into price(ticker, eod_date, close) values ('GOOG', curdate(), 100.1);  
select * from price;  
```
## SQL Alchemy Reference
https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91  
https://overiq.com/sqlalchemy-101/



