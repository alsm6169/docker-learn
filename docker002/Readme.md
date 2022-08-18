# What we learned in previous chapter
- basic docker commands e.g. to run a container, to launch in containers bash shell, remove image etc.
- we created a custom container from ubuntu, installed python and executed python code that is stored locally

# Current Chapter Scope
- create custom container using docker file with python code within the container i.e. will be shipped with the container
- save output of code run from container on to a local folder

### Docker command to build the image
Refer to previous chapter for basic docker commands, addtional commands

1. build docker image from Dockerfile
`$ docker build -t docker002 .`
2. build docker image from Dockerfile with a specific tag
`$ docker build -t docker002:v2 .`

### check the built docker image
```
$ docker images
REPOSITORY           TAG       IMAGE ID       CREATED         SIZE
docker002            latest    a8a3a4509b82   9 seconds ago   144MB
```
### check the content of the docker image
```
$ docker run -it --rm docker002 bash
root@affe618fc28a:/usr/src/myapp# pwd
/usr/src/myapp
root@affe618fc28a:/usr/src/myapp# ls -l
total 8
-rw-r--r-- 1 root root 2028 Aug 18 06:02 Readme.md
-rw-r--r-- 1 root root 1047 Aug 17 15:11 echo_docker.py
root@affe618fc28a:/usr/src/myapp# exit
exit
$ 
```
### run docker without any parameter
```
$ docker run -it --rm docker002
passed from dockerfile
$ 
```
### run docker with parameter
```
$ docker run -it --rm docker002 python echo_docker.py 'new command line param'
new command line param
```
### run docker with parameter and save output to file
**Note: file generated is ephemeral and gets destroyed with the container exit**
```
$ docker run -it --rm docker002 python echo_docker.py 'new command line param' -f out.txt
new command line param
$ ls
Dockerfile	Readme.md	echo.py
```
### run docker with parameter and save output to file in a persistent way i.e. visible after container exits
**Note:
local 'current' directory is mounted on docker as '/mounted_vol'
we specify the output of program to /mounted_vol/out.txt with a -f flag**
```
$ docker run -it --rm -v "$PWD":/mounted_vol -w /usr/src/myapp docker002 python echo_docker.py -f /mounted_vol/out.txt "from the command line into file"
from the command line into file
$ ls -l
total 32
-rw-r--r--  1 anirudh  staff   947 18 Aug 08:06 Dockerfile
-rw-r--r--  1 anirudh  staff  2516 18 Aug 08:12 Readme.md
-rw-r--r--  1 anirudh  staff  1047 17 Aug 17:11 echo.py
-rw-r--r--  1 anirudh  staff    31 18 Aug 08:15 out.txt
$ cat out.txt 
from the command line into file
```
## Summary
What happened here is:  
- we created a new docker image with python installed (we could have installed additional libaries like pandas etc.)
- now we *run this image to run our python program to save the results locally*
