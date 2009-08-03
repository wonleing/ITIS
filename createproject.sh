#!/bin/bash
#This script is used to make server.conf take effect. You need to be root to run this!
source server.conf
source application.conf

((`id -u` !=0 )) && echo "You need to be root to run create project script!" && exit
(($# != 2)) && echo "Usage: ./$0 project_name application_name!" && exit
case "$2" in
  ldap)
    echo "LDAP user added!";;
  samba)
    mkdir -p $share_path/$1;;
  MediaWiki)
    firefox http://localhost:$apache_port/wiki/index.php?title=$1&action=edit&section=1;;
  Wordpress)
    firefox http://localhost:$apache_port/$wp_urlbase/wordpress/wp-login.php;;
  Bugzilla)
    firefox http://localhost:$apache_port/bugzilla/relogin.cgi;;
  Sugarcrm)
    firefox http://localhost:$apache_port/sugarcrm/index.php?module=Project&action=EditView&return_module=Project&return_action=DetailView;;
  Dotproject)
    firefox http://localhost:$apache_port/dotproject/index.php?m=companies&a=addedit;;
  Orangehrm)
    firefox http://localhost:$apache_port/orangehrm/login.php;;
  Drupal)
    firefox http://localhost:$apache_port/drupal/?q=node/add/page;;
  *)
    echo application $2 is not defined
    exit 1;;
esac
