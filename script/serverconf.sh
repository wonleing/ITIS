#!/bin/bash
#This script is used to make server.conf take effect. You need to be root to run this!
source /etc/itis/server.conf

((`id -u` !=0 )) && echo "You need to be root to run server configure script!" && exit
#Shut down SELinux, which block our changing to server configuration
setenforce 0

#Ldap Configuration. Where to configure the mail dn?
mkdir -p $ldap_path
dcstring="dc=`echo $ldap_com | sed 's/\./,dc=/g'`"
ldap_p=`slappasswd -h {MD5} -s $ldap_passwd`
sed -i -e "/secret/d" -e "/^suffix/c\\suffix\t\t\"$dcstring\"" -e "/^rootdn/c\\rootdn\t\t\"cn=$ldap_uname,$dcstring\"" -e "/^directory/c\\directory\t$ldap_path" -e "/^directory/c\\directory\t$ldap_path" -e "/        by dn.exact/c\\        by dn.exact=\"cn=$ldap_uname,$dcstring\" read" -e "/rootpw/c\\rootpw\t\t$ldap_p" /etc/openldap/slapd.conf
sed -i "/^BASE/c\\BASE $dcstring" /etc/openldap/ldap.conf
sed -i "/^base/c\\base $dcstring" /etc/ldap.conf
pkill slapd
slapd

#Mysql Configuration
/etc/init.d/mysqld start
mkdir -p $database_path
mysqladmin -u $database_uname password $database_passwd
grep "^datadir=$database_path" /etc/my.cnf
if (($?==1));then
  sed -i "/^datadir/c\\datadir=$database_path" /etc/my.cnf
  /etc/init.d/mysqld restart
fi

#Apache Configuration
mkdir -p $apache_path
grep ^DocumentRoot /etc/httpd/conf/httpd.conf
if (($?==0));then
  sed -i "/^DocumentRoot/c\\DocumentRoot $apache_path" /etc/httpd/conf/httpd.conf
else
  echo "DocumentRoot $apache_path" >> /etc/httpd/conf/httpd.conf
fi
grep ^Listen /etc/httpd/conf/httpd.conf
if (($?==0));then
  sed -i "/^Listen/c\\Listen $apache_port" /etc/httpd/conf/httpd.conf
else
  echo "Listen $apache_port" >> /etc/httpd/conf/httpd.conf
fi
sed -i "s/^#AddHandler cgi-script .cgi/AddHandler cgi-script .cgi/" /etc/httpd/conf/httpd.conf
echo "<html><p>Now apache home directory is $apache_path, using port $apache_port</p>
<li><a href="$svn_repo/$svn_repo">svn repos</a></li>
<li><a href="wiki">Mediawiki</a></li>
<li><a href="wordpress">Wordpress</a></li>
<li><a href="bugzilla">Bugzilla</a></li>
<li><a href="sugarcrm">Sugarcrm</a></li>
<li><a href="dotproject">Dotproject</a></li>
<li><a href="orangehrm">Orangehrm</a></li>
<li><a href="drupal">Drupal</a></li>
</html>" > $apache_path/index.html

apachectl restart

#Samba Configuration
grep "^\[$share_name\]" /etc/samba/smb.conf
if (($?==1));then
  mkdir -p $share_path
  echo "[$share_name]
       comment = Public samba share
       path = $share_path
       public = yes
       writable = yes
       printable = no
       write list = +root" >> /etc/samba/smb.conf
  /etc/init.d/smb restart
fi

#Subversion Configuration
grep "VNParentPath $svn_path" /etc/httpd/conf.d/subversion.conf | grep -v '#'
if (($?==1));then
  mkdir -p $svn_path
  svnadmin create $svn_path/$svn_repo
  chown -R apache:apache $svn_path
  echo "<Location /$svn_repo>
   DAV svn
   SVNParentPath $svn_path
   SVNListParentPath on
   <LimitExcept GET PROPFIND OPTIONS REPORT>
      AuthType Basic
      AuthName \"Authorization Realm\"
      AuthUserFile /var/www/svn/user_access/svn_passwdfile
      Require valid-user
   </LimitExcept>
</Location>" >> /etc/httpd/conf.d/subversion.conf
/etc/init.d/httpd restart
#svn --username leon --password leing import --depth files `pwd` http://127.0.0.1:$apache_port/$svn_repo/$svn_repo -m "initially import my scripts into $svn_repo"
fi

#Daily and Weekly cronjob
[ "x$backup_daily" != "x" ] && [ -f $backup_daily ] && cp $backup_daily /etc/cron.daily/
[ "x$backup_weekly" != "x" ] && [ -f $backup_weekly ] && cp $backup_weekly /etc/cron.weekly/
/etc/init.d/crond restart

#If you want to enable SELinux again, please uncomment next line
#setenforce 1
