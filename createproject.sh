#!/bin/bash
#This script is used to make server.conf take effect. You need to be root to run this!
source server.conf
source application.conf

((`id -u` !=0 )) && echo "You need to be root to run create project script!" && exit
(($# != 2)) && echo "Usage: ./$0 project_name application_name!" && exit
case "$2" in
  ldap)
    echo LDAP..$2;;
  samba)
    ;;
  MediaWiki)
    ;;
  Wordpress)
    ;;
  Bugzilla)
    ;;
  Sugarcrm)
    ;;
  Dotproject)
    ;;
  Orangehrm)
    ;;
  Drupal)
    ;;
  *)
    echo application $2 is not defined
    exit 1;;
esac
