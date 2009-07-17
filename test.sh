#!/bin/bash
#This script is used to make application.conf take effect. You need to be root to run this!
source application.conf
source server.conf

((`id -u` !=0 )) && echo "You need to be root to run application configure script!" && exit

  drdir=$apache_path/drupal
  [ -z $dr_urlbase ] || (mkdir -p $apache_path/$dr_urlbase; drdir=$apache_path/$dr_urlbase/drupal)
  ln -s /usr/share/drupal $drdir
  echo "create database $dr_dbname;
create user $dr_dbuser@localhost;
update mysql.user set Password=password(\"$dr_dbpwd\") where User=\"$dr_dbuser\";
grant all privileges on $dr_dbname.* to $dr_dbuser@localhost;
flush privileges;" | mysql -u $database_uname -p$database_passwd

