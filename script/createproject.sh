#!/bin/bash
#This script is used to make server.conf take effect. You need to be root to run this!
source /etc/itis/server.conf
source /etc/itis/application.conf
source /etc/itis/config

((`id -u` !=0 )) && echo "You need to be root to run create project script!" && exit
(($# != 2)) && echo "Usage: ./$0 project_name application_name!" && exit
[ -f $apache_path/$1.html ] || echo "<p>Project: $1</p><br/>" > $apache_path/$1.html
case "$2" in
  ldap)
    $MAIN_DIR/script/ldapadduser.sh
    echo "LDAP user added!" >> $apache_path/$1.html;;
  samba)
    mkdir -p $share_path/$1
    echo "share directory added" >> $apache_path/$1.html;;
  MediaWiki)
    echo "<li><a href=wiki>Mediawiki</a></li>" >> $apache_path/$1.html;;
  Wordpress)
    echo "<li><a href=wordpress>Wordpress</a></li>" >> $apache_path/$1.html;;
  Bugzilla)
    echo "<li><a href=bugzilla>Bugzilla</a></li>" >> $apache_path/$1.html;;
  Sugarcrm)
    echo "<li><a href=sugarcrm>Sugarcrm</a></li>" >> $apache_path/$1.html;;
  Dotproject)
    echo "<li><a href=dotproject>Dotproject</a></li>" >> $apache_path/$1.html;;
  Orangehrm)
    echo "<li><a href=orangehrm>Orangehrm</a></li>" >> $apache_path/$1.html;;
  Drupal)
    echo "<li><a href=drupal>Drupal</a></li>" >> $apache_path/$1.html;;
  *)
    echo application $2 is not defined
    exit 1;;
esac
chown apache:apach $apache_path/$1.html
