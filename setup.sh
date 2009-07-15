#!/bin/bash
#This script is used for create login username and password.
((`id -u` != 0)) && echo "You need to be root!" && exit
(($# != 2)) && echo "Usage: $0 username password" && exit
sed -e "s/username/$1/g" -e "s/password/$2/g" initdb | sqlite db1
python setup.py install
python index.py &
echo Webserver started!
