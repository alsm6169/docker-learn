# Docker best practices
# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
# https://snyk.io/blog/best-practices-containerizing-python-docker/

# define the base image to use
FROM python:3.10.5-slim
# set the default workind directory
WORKDIR /app_base
# copy the requirements file
COPY requirements.txt .
# install the requirements
RUN pip install -r requirements.txt
# copy the local contents to working directors
COPY . ./
# create a local output directory
RUN mkdir output
# change the working directory
WORKDIR /app_base/app
# default command to execute if no commands are passed
CMD ["python", "eod_price.py", "TSLA", "-b", "5"]