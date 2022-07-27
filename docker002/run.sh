# build docker image from Dockerfile
docker build -t docker002 .
docker build -t docker002:v2 .

# check docker images
docker images
# output
#REPOSITORY             TAG       IMAGE ID       CREATED        SIZE
#docker002              latest    629c3f781f48   4 hours ago    143MB
#ubuntu_python_pip      latest    40ca4d722cd0   16 hours ago   460MB
#ubuntu2204_python310   latest    9f14c3aa8bfd   16 hours ago   142MB
#python                 slim      b59170d6b634   7 days ago     125MB
#python                 latest    6bb8bdb609b6   7 days ago     920MB
#ubuntu                 22.04     27941809078c   8 days ago     77.8MB
#ubuntu                 latest    27941809078c   8 days ago     77.8MB
#ubuntu                 20.04     20fffa419e3a   8 days ago     72.8MB
#busybox                latest    560956ac186f   12 days ago    1.24MB
#hello-world            latest    feb5d9fea6a5   8 months ago   13.3kB

# run docker default
docker run -it --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp docker002
# output
#> passed from dockerfile

# run docker input parameter
docker run -it --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp docker002
# output
# passed from dockerfile
docker run -it --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp docker002 python echo.py "from the command line"
# output
#> from the command line

# passed from dockerfile
docker run -it --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp docker002 python echo.py -f out.txt "from the command line into file"
# output
cat out.txt
#> from the command line into file

#login into bash shell
docker run -it --rm docker002 bash

# remove all running processes
docker rm `docker ps -aq`