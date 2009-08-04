#!/bin/bash
((`id -u` != 0)) && echo "You need to be root!" && exit
rpm -q python-cherrypy
(($?==1)) && (echo "Intalling python-cherrypy...";yum -q -y python-cherrypy)
rpm -q python-genshi
(($?==1)) && (echo "Intalling python-genshi...";yum -q -y python-genshi)
rm -rf /etc/itis /usr/itis/
mkdir -p /usr/itis/
cp -r html index.py language README script test /usr/itis/
cp lib/* /usr/lib/python2.*/site-packages
cp -r etc/itis /etc/
cat /etc/itis/initdb.sql | sqlite3 /usr/itis/db
ln -s /usr/itis/script/itis /etc/init.d/itis > /dev/null 2>&1
echo -e "Package install successfully!\nPlease use '/etc/init.d/itis start' to start the service\n"
