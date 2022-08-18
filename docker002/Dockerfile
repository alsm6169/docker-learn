# https://testdriven.io/blog/docker-best-practices/
# Good notes from above link
# It's a good idea to combine the RUN, COPY, and ADD commands as much as possible since they create layers
# Use COPY unless you're sure you need the additional functionality that comes with ADD.
# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
# other useful links
# https://www.docker.com/blog/containerized-python-development-part-1/
# https://www.docker.com/blog/containerized-python-development-part-2/
# https://www.docker.com/blog/containerized-python-development-part-3/

# define the base image to use
FROM python:slim
# update the image
RUN apt-get update
# define your working directory
WORKDIR /usr/src/myapp
# copy contents of local directory to the working directory
# only renaming it to show that we are executing the file from inside container and not the local file
# we could have alternatively done COPY . .
COPY echo.py echo_docker.py
COPY Readme.md .
# default command to execute if no commands are passed
CMD ["python", "echo_docker.py", "passed from dockerfile"]