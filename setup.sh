#!/bin/bash
#This script is used for create login username and password.
((`id -u` != 0)) && echo "You need to be root!" && exit
(($# != 2)) && echo "Usage: $0 username password" && exit
yum install -q -y python-cherrypy python-genshi
sed -e "s/username/$1/g" -e "s/password/$2/g" initdb | sqlite3 db1
python index.py &
sleep 2
echo Webserver started!
