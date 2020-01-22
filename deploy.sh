#!/bin/bash

eval "$(ssh-agent -s)" &&
ssh-add -k ~/.ssh/id_rsa &&
cd /var/www/backend    #direktori pada server (ec2 aws)
git pull

source ~/.profile
echo "$DOCKERHUB_PASS" | docker login --username $DOCKERHUB_USER --password-stdin
docker stop gudangworkout2
docker rm gudangworkout2
docker rmi bimonalta/gudang_workout:be2
docker run -d --name gudangworkout2 -p 5000:5000 bimonalta/gudang_workout:be2
