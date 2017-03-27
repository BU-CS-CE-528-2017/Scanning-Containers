#Dockerizing MongoDB: Dockerfile for building MongoDB images

# Format: FROM repository[:version]
FROM ubuntu:14.04

#Installation
#Importing MongoDB public GPG key and create a MongoDB list file
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv EA312927
RUN echo "deb http://repo.mongodb.org/apt/ubuntu $(cat /ect/lsb-release | grep DIS TRIB_CODENAME | CUT -d = -f2)/mongodb-org/3.2 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-3.2.list

#Update apt-get sources and intall MongoDB 
RUN apt-get update && apt-get install -y mongodb-org

#Create the MongoDB data directory
RUN mkdir -p /data/db

#Expose port 27017 from the container to the host
EXPOSE 27017

#Set usr/bin/mongod as the dockerized entry-point applicatioin 
ENTRYPOINT ["/usr/bin/mongod"] 
