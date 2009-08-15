#!/bin/bash
source etc/itis/config

((`id -u` != 0)) && echo "You need to be root!" && exit 1
rpm -q `cat dependencelist` > /dev/null
(($? != 0)) && echo "some packages are missed. please check dependencelist." && exit 1
echo "Alias /wiki /var/www/wiki" > /etc/httpd/conf.d/wiki.conf
echo "Alias /drupal /usr/share/drupal" > /etc/httpd/conf.d/drupal.conf
mkdir -p $MAIN_DIR
cp -r etc/itis /etc/
cp -r html index.py language README script test $MAIN_DIR
cp lib/* $LIB_DIR
ln -s $MAIN_DIR/script/itis /etc/init.d/itis > /dev/null 2>&1
cat /etc/itis/initdb.sql | sqlite3 /tmp/db > /dev/null 2>&1
echo -e "Package install successfully!\nPlease use 'service itis start' to start the service\n"
