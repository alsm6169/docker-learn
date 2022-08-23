# Learn from scratch: Build a Docker + Airflow application to fetch daily stock price
These series of chapters help you build your hands-on docker knowledge from scratch to a full-fledged application 
that uses airflow + mysql database to fetch daily end of day stock price and store it in MySQL database.

These series of lessons are a very good accompaniment to some YouTube tutorial available for Docker and Airflow.   
**One can simply execute the commands described in each chapter's Readme file to get training on docker commands.**   
Each subsequent chapter builds new skills from previous chapter.

**Pre-requisite**    
* Python knowledge 
* Basis Docker knowledge (what is docker and why it's a great idea to build docker based application)
* Basic Airflow knowledge (what is Airflow, what can be achieved with Airflow)

*Note: The python applications created are small and simple, 
no explanation of the code logic has been provided though they should be easy to read and understand.
Same is true for the DAG code (i.e. the Airflow scheduler)
Hence, Python is defined as a pre-requisite*

**Here is an overview of all the chapters. 
The actual commands to execute and more explanation is in the Readme of each chapter**

## docker001
* Get familiar with basic Docker commands e.g. pulling a docker image, running a container, checking status
* Build a custom image on top of ubuntu and install python libaries and save it in a docker image
* User your custom docker image to run your python programs (note: at this stage python program is not part of image itself)

## docker002
* Create an image using Dockerfile
* Build a simple python based docker application that echoes the command line input parameter. 
* Run docker container with different parameter options.  

**Note:** unlike previous chapter here the application is shipped as a part of your docker image.

## docker003
* Build a first version of python application that fetches the end-of-day stock price for input number of days. 
The output is of this python application is displayed on console or written to file based on command line parameters 
* Build a custom docker application containing above end-of-day stock pricer
* Learn to run docker image to save the output to local directory

## docker004
* Download MySQL server docker image. Learn to start and stop the MySQL containers.
* Connect to MySQL DB from command line and create tables manually.   
* Learn about docker-compose.yaml that helps to define and run multi-container Docker applications.

**Note:** Here we take a break from python application and learn only about the MySQL docker container

## docker005
* Enhance the python application to write the fetched end-of-day prices and write to database (besides console and file)
* Create docker-compose.yaml to (download+)run MYSQL server and build python image docker application
* Run docker app that fetches end-of-day stock price and writes to DB
* View the different running configurations and data output
* Learn how to pass environment variables to from .env file to applications via docker-compose

**Note:** docker005 combines and builds upon the learnings of chapters docker003 and docker004.

## docker006
* Download, configure, run and stop Airflow docker container
* Run Airflow examples and understand the output

**Note:** Here we take a break from python application and learn only about Airflow

## docker007
* Use multiple docker compose files that  
  - launches MySQL server, 
  - launches Airflow server,
  - creates application docker image if it does not exist
* Learn to start, check status and stop containers specified in multiple docker-compose images 
* Test the docker application to check output to console, file in a directory and in the database
* Automatically run the docker python application at configured time and verify the output

**Note:** docker007 combines and builds upon the learnings of chapters docker005 (which itself is built upon 003 and 004)
and docker006.   

# What can be done next? 
This application base can be further enhanced as follows:
- Instead of providing a single ticker (e.g. GOOG for google), provide an input file containing list of tickers
- Enhance the program to scrape (or via API) get earnings results and other parameters from company website or other source
- Use business intelligence tools like PowerBI, Tableau to build analytics