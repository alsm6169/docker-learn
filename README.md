# Learn from scratch: Docker + Airflow application to fetch daily stock price
These are series of chapters to help you build your hands-on docker knowledge from scratch to a full-fledged application 
that uses airflow + mysql database to fetch daily end of day stock price and store it in MySQL database.

This series of lessons is a very good accompaniment to some YouTube tutorial available for Docker and Airflow.   
**One can simply execute the commands described in each chapter's Readme file to get training on docker commands.**   
Each subsequent chapter builds new skills from previous chapter.

**Pre-requisite**    
* Python knowledge
* Basis Docker knowledge (what is docker and why its a great idea to build docker based application)
* Basic Airflow knowledge (what is Airflow, what can be achieved with Airflow)

## docker001
* Get familiar with basic Docker commands e.g. pulling a docker image, running a container, checking status
* Build a custom image on top of ubuntu and install python libaries and save it image
* User your custom docker image to run your python programs (note: at this stage python program is not part of image itself)
## docker002
* Learn about Dockerfile
* Build a simple python based docker application that echoes the command line input parameter. 
* Learn to run docker image with different parameter options.  
Note: unlike previous chapter here the application is shipped as a part of your docker image. 
## docker003
* Build a first version of python application that fetches the end-of-day stock price for input number of days. 
The output is of this python application is displayed on console or written to file based on command line parameters 
* Build a custom docker application containing above end-of-day stock pricer
* Learn to run docker image to save the output to local directory
## docker004
* Learn to download MySQL server docker image, start and stop the MySQL containers.
* Learn to connect to MySQL DB from command line and create tables manually.   
* Learn about docker-compose.yaml that helps to define and run multi-container Docker applications.  
Note: Here we take a break from python application and learn only about the MySQL database
## docker005
* Enhance the python application to write the fetched end-of-day prices and write to database (besides console and file)
* Create docker-compose to (download+)run MYSQL server and build python image docker application
* Run docker app that fetches end-of-day stock price and writes to DB
* View the different running configurations and data output
* Learn how to pass environment variables to from .env file to applications via docker-compose
Note: docker005 combines and builds upon the learnings of chapters docker003 and docker004.   
## docker006
* Learn to download, configure and run Airflow docker image
* Run Airflow examples and understand the output
Note: Here we take a break from python application and learn only about Airflow
## docker007
* Use multiple docker compose files that  
  - launches MySQL server, 
  - launches Airflow server,
  - creates application docker image if it does not exist
* Learn to start, check status and stop containers specified in multiple docker-compose images 
* Test the docker application to check output to console, file in a directory and in the database
* Automatically run the docker python application at configured time and verify the output
Note: docker007 combines and builds upon the learnings of chapters docker005 (which itself is built upon 003 and 004)
and docker006.   
