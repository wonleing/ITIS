#!/bin/bash
#This script is used for create login username and password.
((`id -u` != 0)) && echo "You need to be root!" && exit
yum install -q -y python-cherrypy python-genshi
cat initdb.sql | sqlite3 db
python index.py &
sleep 2
echo Webserver started!
