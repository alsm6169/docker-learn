# run echo.py after mounting current directory and later removing the instance from memory
#for running with full python image
docker run -it --rm --name docker001 -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:latest python main.py

#for running with slim python image
docker run -it --rm --name docker001 -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:slim python main.py

# running with arguments # 1
docker run -it --rm --name docker001 -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:slim python main.py ' how are you doing?'
# running with arguments # 2, since volume is mounted, we can see the output file in PWD
docker run -it --rm --name docker001 -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:slim python main.py 'how are you doing?' -f echo.txt

#login into bash shell
docker run -it --rm python:latest bash
docker run -it --rm python:slim bash

#login into bash shell in a specific directory
docker run -it --rm -w /usr/src/myapp python:slim bash
# check files after login into bash
ls -l
# output
# total 0

#login into bash shell in a specific directory after mounting volume
docker run -it --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:slim bash
# check files after login into bash
ls -l
#output
#total 8
#drwxr-xr-x 3 root root   96 Jun 14 13:08 __pycache__
#-rw-r--r-- 1 root root  691 Jun 15 07:42 echo.py
#-rw-r--r-- 1 root root 2842 Jun 15 07:52 run.sh

#manually update an image. example: install python in ubuntu and commit that image
docker run -it  ubuntu:22.04 bash
#now inside the bash shell of the image
#update ubuntu
apt-get update
#install python
apt-get install -y python3
#check python version
python3 -V
#install the pip package
apt-get install -y python3-pip
#exit and see the difference
# use command docker ps -a to get the container_id
exit
docker ps -a
docker diff container_id

# docker commit (create new image)
# example: docker commit fa23a07792da ubuntu_python_pip
docker commit container_id new_image_name
# comparing different python images
docker images
#output
#REPOSITORY             TAG       IMAGE ID       CREATED          SIZE
#ubuntu_python_pip      latest    40ca4d722cd0   32 minutes ago   460MB
#ubuntu2204_python310   latest    9f14c3aa8bfd   53 minutes ago   142MB
#python                 slim      b59170d6b634   7 days ago       125MB
#python                 latest    6bb8bdb609b6   7 days ago       920MB
#ubuntu                 22.04     27941809078c   8 days ago       77.8MB
#ubuntu                 latest    27941809078c   8 days ago       77.8MB
#ubuntu                 20.04     20fffa419e3a   8 days ago       72.8MB
#busybox                latest    560956ac186f   12 days ago      1.24MB
#hello-world            latest    feb5d9fea6a5   8 months ago     13.3kB

# Notes-->
# ubuntu_python_pip ubuntu + python + pip installed and then committed by me
# ubuntu2204_python310 ubuntu + python installed and then committed by me
# python slim is smallest size image, but ubuntu with python installed is smaller than python:latest

# remove all running processes
docker rm `docker ps -aq`