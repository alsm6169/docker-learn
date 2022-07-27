# build docker image from Dockerfile
docker build -t docker003 .
docker build -t docker003:v2 .
# force rebuild
docker build --no-cache -t docker003 .

#login into bash shell
docker run -it --rm docker003 bash
#Note: sice WORKDIR /app_base/app, it logs into this shell
#root@8609b5474ac1:/app_base/app# ls -l
#total 4
#-rw-r--r-- 1 root root 3524 Jun 19 21:28 main.py

# run docker default
docker run -it --rm  docker003
docker run -it --rm -v "$PWD":/app_base/output docker003
# NOTE: -w /app_base/app is option as WORKDIR has been set in Dockerfile but if not set, it would be needed for run
docker run -it --rm -w /app_base/app docker003

# run docker input parameter (-it is for interactive, since we run and exit the program it is not needed)
docker run --rm docker003 python main.py AMZN
docker run --rm docker003 python main.py ACN -b 15

# save output in file out.csv but it will not be accessible as volume is not mounted
docker run --rm -w /app_base/app docker003 python main.py MSCI -f out.csv -b 8
cat out.csv
# cat: out.csv: No such file or directory

# save output in file out.csv saved in $PWD folder
docker run --rm -v "$PWD":/app_base/output -w /app_base/app docker003 python main.py GOOG -f out.csv -b 10
cat ./out.csv
# ./out.csv has 10 days of GOOG price
docker run --rm -v /Users/anirudh/Documents/Python/GitHub/docker-learn/output:/app_base/output docker003 python main.py MCO -b 3 -f out.csv
cat /Users/anirudh/Documents/Python/GitHub/docker-learn/output/out.csv
#> docker-learn/output/out.csv has 3 days of MCO price

# remove all running processes
docker rm `docker ps -aq`

