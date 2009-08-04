#!/bin/bash
#This script is used for create login username and password.
((`id -u` != 0)) && echo "You need to be root!" && exit
yum install -q -y python-cherrypy python-genshi
rm -rf /etc/itis /usr/itis/script
cp -r lib/* /usr/lib/python2.*/site-packages
cp -r etc/itis /etc/
mkdir -p /usr/itis
cp -r script /usr/itis/
cat /etc/itis/initdb.sql | sqlite3 db
echo Package install successfully!
python index.py &
sleep 2
echo Webserver started!
