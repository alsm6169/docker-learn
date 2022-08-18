# Current Chapter Scope
- Learn a few Docker commands
- Create a Docker image manually (using a series of commands on console)
- Use to Docker image (which has all dependencies) to run your script
- 
## Few essential docker commands
[docker commands link](https://www.edureka.co/blog/docker-commands/)
1. pull a new image from docker repository (only pull not run)
````
$ docker pull hello-world
Using default tag: latest
latest: Pulling from library/hello-world
2db29710123e: Pull complete 
Digest: sha256:7d246653d0511db2a6b2e0436cfd0e52ac8c066000264b3ce63331ac66dca625
Status: Downloaded newer image for hello-world:latest
docker.io/library/hello-world:latest
````
2. List all local images
````
$ docker images
REPOSITORY           TAG       IMAGE ID       CREATED         SIZE
hello-world          latest    feb5d9fea6a5   10 months ago   13.3kB
````
3. List the exited images
````
$ docker ps -a
CONTAINER ID   IMAGE         COMMAND    CREATED          STATUS                      PORTS     NAMES
6298feb8949d   hello-world   "/hello"   29 seconds ago   Exited (0) 27 seconds ago             competent_satoshi
````
4. List running images
```
$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```
5. Pull and run a new image
```
$ docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
2db29710123e: Pull complete 
Digest: sha256:7d246653d0511db2a6b2e0436cfd0e52ac8c066000264b3ce63331ac66dca625
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
...  
...
```
6. remove stopped / executed container (i.e. ones we can see with $ docker ps -a but cannot see in $ ps) 
```
$ docker rm 6298feb8949d
6298feb8949d

```
7. remove all processes that have exited
```
docker rm `docker ps -aq` 
```
8. remove downloaded image
```
$ docker rmi hello-world
Untagged: hello-world:latest
Untagged: hello-world@sha256:7d246653d0511db2a6b2e0436cfd0e52ac8c066000264b3ce63331ac66dca625
Deleted: sha256:feb5d9fea6a5e9606aa995e879d862b825965ba48de054caab5ef356dc6b3412
Deleted: sha256:e07ee1baac5fae6a26f30cabfe54a36d3402f96afda318fe0a96cec4ca393359
```
9. login to bash shell into an image
```
$ docker run -it ubuntu bash
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
d19f32bd9e41: Pull complete 
Digest: sha256:34fea4f31bf187bc915536831fd0afc9d214755bf700b5cdb1336c82516d154e
Status: Downloaded newer image for ubuntu:latest
root@17ec918701d6:/# ls
bin   dev  home  lib32  libx32  mnt  proc  run   srv  tmp  var
boot  etc  lib   lib64  media   opt  root  sbin  sys  usr
root@17ec918701d6:/# exit
exit
$ docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED          STATUS                       PORTS     NAMES
17ec918701d6   ubuntu    "bash"    25 seconds ago   Exited (127) 5 seconds ago             inspiring_bose
```
#login into bash shell in a specific directory
```
$ docker run -it --rm -w /usr/src/myapp python:slim bash
# check files after login into bash
root@77f91c03e472:/usr/src/myapp# ls -l
total 0
root@77f91c03e472:/usr/src/myapp# 
```
#login into bash shell in a specific directory after mounting volume
```
$ docker run -it --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:slim bash
# check files after login into bash
root@8ff888b4e06b:/usr/src/myapp# ls -l
total 12
-rw-r--r-- 1 root root 6056 Aug 17 20:00 Readme.md
-rw-r--r-- 1 root root 1047 Aug 17 15:11 echo.py
root@8ff888b4e06b:/usr/src/myapp# 
```
10. run an image and auto remove the container after exiting
```
$ docker run --rm hello-world

Hello from Docker!
...
...
$ docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

```
## Building Docker image by hand
**Objective:** To create a docker image by hand  containing python.  
***NOTE:** Almost never it is done like this. Dockerfile is a better way to do things. 
Dockerfile is described in next tutorial.*

**# manually update an image. example: install python in ubuntu and commit that image**  
`$ docker run -it  ubuntu bash`   
#now inside the bash shell of the image  
#update ubuntu  
`$ apt-get update`  
#install python  
`$ apt-get install -y python3`   
#check python version  
`$ python3 -V`  
#install the pip package  
`$ apt-get install -y python3-pip`  
#exit  
`$ exit`  
#use command docker ps -a to get the container_id  
`$ docker ps -a`  
#see the difference in the image   
#example: docker diff 63c8258db2a0  
`$ docker diff <container_id>`   
#docker commit (create new image)  
#example: docker commit 63c8258db2a0 ubuntu_python_pip  
`$ docker commit <container_id> new_image_name`  

#comparing different python images  
```
$ docker images
REPOSITORY           TAG       IMAGE ID       CREATED          SIZE
ubuntu_python_pip    latest    ec1476734a48   21 seconds ago   461MB
ubuntu               latest    df5de72bdb3b   2 weeks ago      77.8MB
```
***Notes-->  
#ubuntu_python_pip = ubuntu + python + pip installed and then committed  
#python:slim is the smallest size image, but ubuntu with python installed is smaller than python:latest, 
likely due to additional libraries***

## Running python program in the Docker image
*echo.py:*  This python scrip `echo.py` echos the command line input back on the console or file as specified by the 
input parameters.  
If no input parameters are provided then 'Hi, PyCharm' is echoed on console.
```
$ ls -l
total 24
-rw-r--r--  1 staff  staff  6064 17 Aug 17:13 Readme.md
-rw-r--r--  1 staff  staff  1047 17 Aug 17:11 echo.py
```
1. with echo results on console
```
$ docker run -it --rm --name docker001 -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu_python_pip python3  echo.py 
Hi from ArgumentParser

$ docker run -it --rm --name docker001 -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu_python_pip python3  echo.py 'how are you doing?'
how are you doing?
```
2. with echo results saved on disk (persistent)
#running with arguments # 2, since volume is mounted, we can see the output file in PWD
```
$ ls -l
total 24
-rw-r--r--  1 staff  staff  6351 17 Aug 22:40 Readme.md
-rw-r--r--  1 staff  staff  1047 17 Aug 17:11 echo.py
$ docker run -it --rm --name docker001 -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu_python_pip python3  echo.py 'how are you doing?' -f echo.txt
how are you doing?
$ ls -l
total 32
-rw-r--r--  1 staff  staff  6351 17 Aug 22:40 Readme.md
-rw-r--r--  1 staff  staff  1047 17 Aug 17:11 echo.py
-rw-r--r--  1 staff  staff    18 17 Aug 22:40 echo.txt

$ cat echo.txt 
how are you doing?
```
## Summary
What happened here is:  
- we created a new docker image with python installed (we could have installed additional libaries like pandas etc.)
- now we call this image to run our python program
In subsequent chapters we will even put our custom scripts into image to make it shippable binary


