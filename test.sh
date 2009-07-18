#!/bin/bash
#This script is used to make application.conf take effect. You need to be root to run this!
source application.conf
source server.conf

((`id -u` !=0 )) && echo "You need to be root to run application configure script!" && exit
rpmdir=../rpmbuild


sed -i -e "s/dotproject/$dp_dbname/g" -e "s/dp_user/$dp_dbuser/" -e "s/dp_pass/$dp_dbpwd/" /usr/share/dotproject/includes/config-dist.php
  [ -z $dp_urlbase ] || sed -i "s,= \$baseUrl,= http://127.0.0.1," /usr/share/dotproject/index.php
  firefox http://localhost:$apache_port/dotproject/install/index.php
