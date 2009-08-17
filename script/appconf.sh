#!/bin/bash
#This script is used to make application.conf take effect. You need to be root to run this!
source /etc/itis/application.conf
source /etc/itis/server.conf
cache=/tmp/cache
((`id -u` !=0 )) && echo "You need to be root to run application configure script!" && exit 1
rpm -q mediawiki wordpress bugzilla sugarcrm dotproject orangehrm drupal || exit 1

#General user provision
echo "create user apache@localhost;
grant all privileges on *.* to apache@localhost;
flush pvilileges;" | mysql -u $database_uname -p$database_passwd > /dev/null 2>&1

#Application database and user provision
echo "create database $mw_dbname;
create user $mw_dbuser@localhost;
update mysql.user set Password=password(\"$mw_dbpwd\") where User=\"$mw_dbuser\";
grant all privileges on $mw_dbname.* to $mw_dbuser@localhost;
create database $wp_dbname;
create user $wp_dbuser@localhost;
update mysql.user set Password=password(\"$wp_dbpwd\") where User=\"$wp_dbuser\";
grant all privileges on $wp_dbname.* to $wp_dbuser@localhost;
create database $bz_dbname;
create user $bz_dbuser@localhost;
update mysql.user set Password=password(\"$bz_dbpwd\") where User=\"$bz_dbuser\";
grant all privileges on $bz_dbname.* to $bz_dbuser@localhost;
create database $sc_dbname;
create user $sc_dbuser@localhost;
update mysql.user set Password=password(\"$sc_dbpwd\") where User=\"$sc_dbuser\";
grant all privileges on $sc_dbname.* to $sc_dbuser@localhost;
create database $dp_dbname;
create user $dp_dbuser@localhost;
update mysql.user set Password=password(\"$dp_dbpwd\") where User=\"$dp_dbuser\";
grant all privileges on $dp_dbname.* to $dp_dbuser@localhost;
create database $oh_dbname;
create user $oh_dbuser@localhost;
update mysql.user set Password=password(\"$oh_dbpwd\") where User=\"$oh_dbuser\";
grant all privileges on $oh_dbname.* to $oh_dbuser@localhost;
create database $dr_dbname;
create user $dr_dbuser@localhost;
update mysql.user set Password=password(\"$dr_dbpwd\") where User=\"$dr_dbuser\";
grant all privileges on $dr_dbname.* to $dr_dbuser@localhost;
flush privileges;" | mysql -u $database_uname -p$database_passwd

#Prepare work
chown -R apache:apache /usr/share/drupal
chown -R apache:apache /etc/drupal
cp /etc/drupal/default/default.settings.php /etc/drupal/default/settings.php
sed -i "/^\$db_url/c\\\$db_url= 'mysql:\/\/$dr_dbuser:$dr_dbpwd@localhost\/$dr_dbname';" /etc/drupal/default/settings.php
[ -z $dr_urlbase ] || sed -i "/^# \$base_url/c\\\$base_url = '$dr_urlbase';" /etc/drupal/default/settings.php
[ -z $sc_urlbase ] || sed -i "s,http://127.0.0.1,$sc_urlbase," /usr/share/sugarcrm/config.php
[ -z $dp_urlbase ] || sed -i "s,= \$baseUrl,= $dp_urlbase," /usr/share/dotproject/includes/config-dist.php
[ -z $mw_urlbase ] || echo "\$wgServer = '$mw_urlbase';" >> /var/www/wiki/config/LocalSettings.php

cd /usr/itis/script/
#Send http request to perform web installation
for app in {'mediawiki','wordpress','sugarcrm','dotproject','orangehrm','drupal'};do
  chown -R apache:apache /usr/share/$app
  j=0
  for i in `grep -n "======" install_$app | cut -d ":" -f1`;do
    awk "NR>$j && NR<$i" install_$app > $cache
    nc localhost 80 < $cache | grep HTTP
    j=$i
  done
done

#Specific works
#mediawiki
mv /var/www/wiki/config/LocalSettings.php /var/www/wiki/
#bugzilla
sed -i -e "s/db_name = 'bugs'/db_name = \'$bz_dbname\'/" -e "s/db_user = 'bugs'/db_user = \'$bz_dbuser\'/" -e "s/db_pass = ''/db_pass = \'$bz_dbpwd\'/" /etc/bugzilla/localconfig
echo "\$answer{'ADMIN_EMAIL'} = 'admin@itis.com';
\$answer{'ADMIN_PASSWORD'} = '$bz_adminpwd';
\$answer{'ADMIN_REALNAME'} = '$bz_adminuser';
\$answer{'SMTP_SERVER'} = 'mail.localhost.localdomain';" > /tmp/bz_temp
[ -z $bz_urlbase ] || echo "\$answer{'urlbase'} = '$bz_urlbase';" >> /tmp/bz_temp
/usr/share/bugzilla/checksetup.pl /tmp/bz_temp
rm -rf /tmp/bz_temp
#sugarcrm
cp config.php /usr/share/sugarcrm/config.php
cp htaccess /usr/share/sugarcrm/.htaccess
#dotproject
sed -e "s/DBNAME/orangehrm/" -e "s/DBUSER/orangehrm/" -e "s/DBPWD/secret/" Conf.php > /usr/share/orangehrm/lib/confs/Conf.php
#orangehrm
sed -e "s/DBNAME/$oh_dbname/" -e "s/DBUSER/$oh_dbuser/" -e "s/DBPWD/$oh_dbpwd/" Conf.php > /usr/share/orangehrm/lib/confs/Conf.php

cd -
#Set application admin account in mysql
echo "update $wp_dbname.wp_users set user_login='$wp_adminuser' where user_login='admin';
update $wp_dbname.wp_users set user_pass=MD5('$wp_adminpwd');
update $bz_dbname.profiles set login_name='$bz_adminuser' where login_name='admin@itis.com';
update $sc_dbname.users set user_hash=MD5('$sc_adminpwd');
insert into $oh_dbname.hs_hr_users (id,user_name,user_password,is_admin,receive_notification,status,deleted) values ('USR001','$oh_adminuser,MD5('$oh_adminpwd),"Yes","1","Enabled","0");
update $dp_dbname.users set user_password=md5('$dp_adminpwd') where user_username='admin';
update $dp_dbname.users set user_username='$dp_adminuser' where user_username='admin';
insert into $oh_dbname.hs_hr_user_group values ('USG001', 'Admin', '1');
insert into $oh_dbname.hs_hr_users (id,user_name,user_password,is_admin,receive_notification,status,deleted,userg_id) values ('USR001','$oh_adminuser',MD5('$oh_adminpwd'),'Yes','1','Enabled','0','USG001');" | mysql -u $database_uname -p$database_passwd
