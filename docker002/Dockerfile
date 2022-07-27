# https://testdriven.io/blog/docker-best-practices/
# Good notes from above link
# It's a good idea to combine the RUN, COPY, and ADD commands as much as possible since they create layers
# Use COPY unless you're sure you need the additional functionality that comes with ADD.
# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
# other useful links
# https://www.docker.com/blog/containerized-python-development-part-1/
# https://www.docker.com/blog/containerized-python-development-part-2/
# https://www.docker.com/blog/containerized-python-development-part-3/

FROM python:slim
# RUN apt-get update
WORKDIR /usr/src/myapp
COPY . .
CMD ["python", "eod_price.py", "passed from dockerfile"]