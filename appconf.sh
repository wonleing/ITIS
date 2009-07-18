#!/bin/bash
#This script is used to make application.conf take effect. You need to be root to run this!
source application.conf
source server.conf
((`id -u` !=0 )) && echo "You need to be root to run application configure script!" && exit
rpmdir=../rpmbuild

#MediaWiki settings
rpm -q mediawiki
if (($?==1));then
  yum -q -y install mediawiki
  wikidir=$apache_path/wiki
  ln -s /var/www/wiki $wikidir
  echo "create database $mw_dbname;
create user $mw_dbuser@localhost;
update mysql.user set Password=password(\"$mw_dbpwd\") where User=\"$mw_dbuser\";
grant all privileges on $mw_dbname.* to $mw_dbuser@localhost;
flush privileges;" | mysql -u $database_uname -p$database_passwd
  sed -i -e "s/wikidb/$mw_dbname/g" \
-e "s/wikiuser/$mw_dbuser/g" \
-e "s/DBpassword\" \)/DBpassword\", \"$mw_dbpwd\" \)/g" \
-e "s/DBpassword2\" \)/DBpassword2\", \"$mw_dbpwd\" \)/g" \
-e "s/WikiSysop/$mw_adminuser/g" \
-e "s/SysopPass\" \)/SysopPass\", \"$mw_adminpwd\" \)/g" \
-e "s/SysopPass2\" \)/SysopPass2\", \"$mw_adminpwd\" \)/g" $wikidir/config/index.php
  firefox http://localhost:$apache_port/wiki/config/index.php
  [ -z $mw_urlbase ] || echo "\$wgServer = '$mw_urlbase';" >> $wikidir/config/LocalSettings.php
  mv $wikidir/config/LocalSettings.php $wikidir/
  sed -i "s/<\/html>/\n<li><a href=\"wiki\">MediaWiki page<\/a><\/li><\/html>/" $apache_path/index.html
fi

#Wordpress settings
#No urlbase option. Use it as subdir name.
rpm -q wordpress
if (($?==1));then
  yum -q -y install wordpress
  wpdir=$apache_path/wordpress
  [ -z $wp_urlbase ] || (mkdir -p $apache_path/$wp_urlbase; wpdir=$apache_path/$wp_urlbase/wordpress)
  ln -s /usr/share/wordpress $wpdir
  echo "create database $wp_dbname;
create user $wp_dbuser@localhost;
update mysql.user set Password=password(\"$wp_mdbpwd\") where User=\"$wp_dbuser\";
grant all privileges on $wp_dbname.* to $wp_dbuser@localhost;
flush privileges;" | mysql -u $database_uname -p$database_passwd
  sed -i -e "s/putyourdbnamehere/$wp_dbname/g" -e "s/usernamehere/$wp_dbuser/g" -e "s/yourpasswordhere/$wp_dbpwd/g" /etc/wordpress/wp-config.php
  firefox http://localhost:$apache_port/$wp_urlbase/wordpress/wp-admin/install.php
  sed -i "s/<\/html>/\n<li><a href=\"$wp_urlbase\/wordpress\">Wordpress page<\/a><\/li><\/html>/" $apache_path/index.html
fi

#Bugzilla settings
rpm -q bugzilla
if (($?==1));then
  yum -q -y install bugzilla
  bzdir=$apache_path/bugzilla
  ln -s /usr/share/bugzilla $bzdir
  echo "create database $bz_dbname;
create user $bz_dbuser@localhost;
update mysql.user set Password=password(\"$bz_dbpwd\") where User=\"$bz_dbuser\";
grant all privileges on $bz_dbname.* to $bz_dbuser@localhost;
flush privileges;" | mysql -u $database_uname -p$database_passwd
  sed -i -e "s/db_name = 'bugs'/db_name = \'$bz_dbname\'/" -e "s/db_user = 'bugs'/db_user = \'$bz_dbuser\'/" -e "s/db_pass = ''/db_pass = \'$bz_dbpwd\'/" /etc/bugzilla/localconfig
  echo "\$answer{'ADMIN_EMAIL'} = '$bz_adminuser';
\$answer{'ADMIN_PASSWORD'} = '$bz_adminpwd';
\$answer{'ADMIN_REALNAME'} = '$bz_adminuser';
\$answer{'SMTP_SERVER'} = 'mail.localhost.localdomain';" > /tmp/bz_temp
  [ -z $bz_urlbase ] || echo "\$answer{'urlbase'} = '$bz_urlbase';" >> /tmp/bz_temp
  cd $bzdir
  ./checksetup.pl /tmp/bz_temp
  cd -
  rm -rf /tmp/bz_temp
  sed -i "s/<\/html>/\n<li><a href=\"bugzilla\">Bugzilla page<\/a><\/li><\/html>/" $apache_path/index.html
fi

#Sugarcrm settings
#No urlbase option. Use it as subdir name.
rpm -q sugarcrm
if (($?==1));then
  rpm -ivh $rpmdir/sugarcrm-*.rpm
  scdir=$apache_path/sugarcrm
  [ -z $sc_urlbase ] || (mkdir -p $apache_path/$sc_urlbase; scdir=$apache_path/$sc_urlbase/sugarcrm)
  chown -R apache:apache /usr/share/sugarcrm
  ln -s /usr/share/sugarcrm $scdir
  echo "create database $sc_dbname;
create user $sc_dbuser@localhost;
update mysql.user set Password=password(\"$sc_dbpwd\") where User=\"$sc_dbuser\";
grant all privileges on $sc_dbname.* to $sc_dbuser@localhost;
flush privileges;" | mysql -u $database_uname -p$database_passwd
  sed -i -e "s/;mbstring\./mbstring\./g" -e "s/EUC-JP/UTF-8/" -e "s/= SJIS/= pass/" -e "s/encoding_translation = Off/encoding_translation = On/" /etc/php.ini
  /etc/init.d/httpd restart
  cp sugarcrmconf.php /usr/share/sugarcrm/config.php
  firefox http://localhost:$apache_port/$sc_urlbase/sugarcrm/install.php
  sed -i "s/<\/html>/\n<li><a href=\"$sc_urlbase\/sugarcrm\">Sugarcrm page<\/a><\/li><\/html>/" $apache_path/index.html
fi

#Dotproject settings
rpm -q dotproject
if (($?==1));then
  rpm -ivh $rpmdir/dotproject-*.rpm
  dpdir=$apache_path/dotproject
  chown -R apache:apache /usr/share/dotproject
  ln -s /usr/share/dotproject $dpdir
  echo "create database $dp_dbname;
create user $dp_dbuser@localhost;
update mysql.user set Password=password(\"$dp_dbpwd\") where User=\"$dp_dbuser\";
grant all privileges on $dp_dbname.* to $dp_dbuser@localhost;
flush privileges;" | mysql -u $database_uname -p$database_passwd
  sed -i -e "s/dotproject/$dp_dbname/g" -e "s/dp_user/$dp_dbuser/" -e "s/dp_pass/$dp_dbpwd/" /usr/share/dotproject/includes/config-dist.php
  [ -z $dp_urlbase ] || sed -i "s,= \$baseUrl,= $dp_urlbase," /usr/share/dotproject/includes/config-dist.php
  firefox http://localhost:$apache_port/dotproject/install/index.php
  sed -i "s/<\/html>/\n<li><a href=\"sugarcrm\">Dotproject page<\/a><\/li><\/html>/" $apache_path/index.html
fi

#Orangehrm settings
rpm -q orangehrm
if (($?==1));then
  rpm -ivh $rpmdir/orangehrm-*.rpm
  ohdir=$apache_path/orangehrm
  [ -z $oh_urlbase ] || (mkdir -p $apache_path/$oh_urlbase; scdir=$apache_path/$oh_urlbase/orangehrm)
  chown -R apache:apache /usr/share/orangehrm
  ln -s /usr/share/orangehrm $ohdir
  echo "create database $oh_dbname;
create user $oh_dbuser@localhost;
update mysql.user set Password=password(\"$oh_dbpwd\") where User=\"$oh_dbuser\";
grant all privileges on $oh_dbname.* to $oh_dbuser@localhost;
flush privileges;" | mysql -u $database_uname -p$database_passwd
  sed -i -e "s/'orangehrm'/\'$oh_dbpwd\'/" -e "s/hr_mysql/$oh_dbname/" -e "s/root/$oh_dbuser/" /usr/share/orangehrm/lib/confs/Conf.php-distribution
  firefox http://localhost:$apache_port/$oh_urlbase/orangehrm/install.php
  sed -i "s/<\/html>/\n<li><a href=\"$oh_urlbase\/orangehrm\">Orangehrm page<\/a><\/li><\/html>/" $apache_path/index.html
fi

#Drupal settings
rpm -q drupal
if (($?==1));then
  yum -q -y install drupal
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
  firefox http://localhost:$apache_port/drupal/install.php
  sed -i "s/<\/html>/\n<li><a href=\"drupal\">Drupal page<\/a><\/li><\/html>/" $apache_path/index.html
fi
