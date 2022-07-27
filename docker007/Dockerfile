# https://testdriven.io/blog/docker-best-practices/
# Good notes from above link
# It's a good idea to combine the RUN, COPY, and ADD commands as much as possible since they create layers
# Use COPY unless you're sure you need the additional functionality that comes with ADD.
#Other best practices
# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
# https://snyk.io/blog/best-practices-containerizing-python-docker/

FROM python:3.10.5-slim
WORKDIR /app_base
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app app
RUN mkdir output
WORKDIR /app_base/app
CMD ["python", "eod_price.py", "TSLA", "-b", "5"]