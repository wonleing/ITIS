#!/bin/bash
#This script is used to make application.conf take effect. You need to be root to run this!
source application.conf
source server.conf

((`id -u` !=0 )) && echo "You need to be root to run application configure script!" && exit
rpmdir=../rpmbuild


  yum -q -y install drupal

  chown -R apache:apache /usr/share/drupal
  firefox http://localhost:$apache_port/drupal/install.php
exit
  drdir=$apache_path/drupal
  ln -s /usr/share/drupal $drdir
  echo "create database $dr_dbname;
create user $dr_dbuser@localhost;
update mysql.user set Password=password(\"$dr_dbpwd\") where User=\"$dr_dbuser\";
grant all privileges on $dr_dbname.* to $dr_dbuser@localhost;
flush privileges;" | mysql -u $database_uname -p$database_passwd
  cp /etc/drupal/default/default.settings.php /etc/drupal/default/settings.php
  sed -i "/^\$db_url/c\\\$db_url= 'mysql:\/\/$dr_dbuser:$dr_dbpwd@localhost\/$dr_dbname';" /etc/drupal/default/settings.php
  [ -z $dr_urlbase ] || sed -i "/^# \$base_url/c\\\$base_url = '$dr_urlbase';" /etc/drupal/default/settings.php
  sed -i "s/^mbstring/;mbstring/g" /etc/php.ini
