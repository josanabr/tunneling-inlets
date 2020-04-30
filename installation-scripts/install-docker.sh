#!/usr/bin/env bash
#
# Script que permite la instalacion de Docker
#
# AUTHOR: John Sanabria - john.sanabria@correounivalle.edu.co
# DATE: 2020-04-29
#
apt-get update
apt-get -y --force-yes install docker.io
usermod -aG docker vagrant
docker pull josanabr/gtd-flask-app
