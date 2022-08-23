## What we learned in previous chapter
- launch a MySql database server using docker-compose or from command line
- create tables in the database

## Current Chapter Scope
We will combine here the separate information
- we have a python code that fetches end of day stock prices and writes it to a console/file/database.
- we also create the tables in the database if tables do not exist
- eod_price.py has a starting introduction to SqlAlchemy the pythonic way to interact with databases

### IMPORTANT NOTE
***Use sample.env to create a .env file before running MySQL server. 
For starters, simply copy (or rename) sample.env as .env***

### SQL Alchemy Reference
[Ref1](https://towardsdatascience.com/sqlalchemy-python-tutorial-79a577141a91)  
[Ref2](https://overiq.com/sqlalchemy-101/)

## Start MySQL server, run app and view the output in DB
1. start sql server and build docker image if not already built  
`$ docker-compose up -d`   
**NOTE: We use new flag '--env-file .env' to pass environment variables like DB NAME, USER, PASSWORD to 
python to be able to connect to the database**  
2. docker run with output to db default parameters
`$ docker run -it --env-file .env --rm docker005`
3. docker run with output to db by specifying parameters
`$ docker run -it --env-file .env --rm docker005 python eod_price.py MSFT`
4. check the contents of db
```
$ docker exec -it mysql-inst bash
bash-4.4# mysql -u root -p
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 35
Server version: 8.0.29 MySQL Community Server - GPL

Copyright (c) 2000, 2022, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> use mktdb;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
mysql> select * from eod_price;
+------------+--------+--------+--------+--------+--------+----------+-----------+---------------------+
| Date       | Ticker | High   | Low    | Open   | Close  | Volume   | Adj Close | last_updated        |
+------------+--------+--------+--------+--------+--------+----------+-----------+---------------------+
| 2022-08-15 | TSLA   |  939.4 | 903.69 | 905.36 | 927.96 | 29786400 |    927.96 | 2022-08-20 06:44:35 |
| 2022-08-16 | TSLA   |    944 | 908.65 |    935 | 919.69 | 29378800 |    919.69 | 2022-08-20 06:44:35 |
| 2022-08-17 | TSLA   | 928.97 |  900.1 | 910.19 | 911.99 | 22922000 |    911.99 | 2022-08-20 06:44:35 |
| 2022-08-18 | TSLA   |  919.5 | 905.56 |    918 | 908.61 | 15833500 |    908.61 | 2022-08-20 06:44:35 |
| 2022-08-19 | MSFT   | 289.25 | 285.56 |  288.9 | 286.15 | 20557200 |    286.15 | 2022-08-20 06:52:34 |
| 2022-08-19 | TSLA   | 901.08 |  877.5 |    897 |    890 | 20417900 |       890 | 2022-08-20 06:44:35 |
+------------+--------+--------+--------+--------+--------+----------+-----------+---------------------+
6 rows in set (0.00 sec)

mysql> exit
Bye
bash-4.4# exit
exit
$ 
```
**Alternatively use free tool like TablePlus to inspect DB and its contents**

## Summary
What we learned here is:  
- we combined knowledge from previous chapters and created first version of the application that fetches end-of-day
stock prices and stores it in database.