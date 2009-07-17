#!/bin/bash
#This script is used to make application.conf take effect. You need to be root to run this!
source application.conf
source server.conf

((`id -u` !=0 )) && echo "You need to be root to run application configure script!" && exit

#MediaWiki settings
rpm -q mediawiki
if (($?==1));then
  yum -q -y install mediawiki
  wikidir=$apache_path/wiki
  [ -z $mw_urlbase ] || (mkdir -p $apache_path/$mw_urlbase; wikidir=$apache_path/$mw_urlbase/wiki)
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
  firefox http://localhost:$apache_port/$mw_urlbase/wiki/config/index.php
  mv $wikidir/config/LocalSettings.php $wikidir/
  sed -i "s/<\/html>/\n<li><a href="$mw_urlbase/wiki">MediaWiki page<\/a><\/li><\/html>/" $apache_path/index.html
fi

#Wordpress settings
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
  sed -i "s/<\/html>/\n<li><a href="$wp_urlbase/wordpress">Wordpress page<\/a><\/li><\/html>/" $apache_path/index.html
fi

#Bugzilla settings
rpm -q bugzilla
if (($?==1));then
  yum -q -y install bugzilla
  bzdir=$apache_path/bugzilla
  [ -z $bz_urlbase ] || (mkdir -p $apache_path/$bz_urlbase; bzdir=$apache_path/$bz_urlbase/bugzilla)
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
  cd $bzdir
  ./checksetup.pl /tmp/bz_temp
  cd -
  rm -rf /tmp/bz_temp
  sed -i "s/<\/html>/\n<li><a href="$wp_urlbase/bugzilla">Bugzilla page<\/a><\/li><\/html>/" $apache_path/index.html
fi

#Drupal settings
rpm -q drupal
if (($?==1));then
  yum -q -y install drupal
  drdir=$apache_path/drupal
  [ -z $dr_urlbase ] || (mkdir -p $apache_path/$dr_urlbase; drdir=$apache_path/$dr_urlbase/drupal)
  ln -s /usr/share/drupal $drdir
  echo "create database $dr_dbname;
create user $dr_dbuser@localhost;
update mysql.user set Password=password(\"$dr_dbpwd\") where User=\"$dr_dbuser\";
grant all privileges on $dr_dbname.* to $dr_dbuser@localhost;
flush privileges;" | mysql -u $database_uname -p$database_passwd
cp /etc/drupal/default/default.settings.php /etc/drupal/default/settings.php
sed -i -e "/^\$db_url/c\\\$db_url= 'mysql:\/\/$dr_dbuser:$dr_dbpwd@localhost\/$dr_dbname';" /etc/drupal/default/default.settings.php
fi
