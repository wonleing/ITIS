#!/bin/bash
#This script is used to make application.conf take effect. You need to be root to run this!
source application.conf
source server.conf

((`id -u` !=0 )) && echo "You need to be root to run application configure script!" && exit

#MediaWiki settings
rpm -q mediawiki
if (($?==1));then
yum -q -y install mediawiki
echo "create database $mw_dbname;
insert into mysql.user(Host,User,Password) values(\"localhost\", \"$mw_dbuser\", password(\"$mw_dbpwd\"));
grant all privileges on $mw_dbname.* to $mw_dbuser@localhost;
flush privileges;" | mysql -u $database_uname -p$database_passwd
sed -i -e "s/wikidb/$mw_dbname/g" \
-e "s/wikiuser/$mw_dbuser/g" \
-e "s/DBpassword\" \)/DBpassword\", \"$mw_dbpwd\" \)/g" \
-e "s/DBpassword2\" \)/DBpassword2\", \"$mw_dbpwd\" \)/g" \
-e "s/WikiSysop/$mw_adminuser/g" \
-e "s/SysopPass\" \)/SysopPass\", \"$mw_adminpwd\" \)/g" \
-e "s/SysopPass2\" \)/SysopPass2\", \"$mw_adminpwd\" \)/g" \
$apache_path/wiki/config/index.php
firefox http://localhost:$apache_port/wiki/config/index.php
mv $apache_path/wiki/config/LocalSettings.php $apache_path/wiki/
fi
#

