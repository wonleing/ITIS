#!/bin/bash
#This script is used to make server.conf take effect. You need to be root to run this!
source server.conf
((`id -u` !=0 )) && echo "You need to be root to run server configure script!" && exit

#Shut down SELinux, which block our changing to server configuration
setenforce 0

#Mysql Configuration
which mysql > /dev/null
(($?==0)) || yum -q -y install mysql mysql-server
/etc/init.d/mysqld start
mysqladmin -u $database_uname password $database_passwd
sed -i "/^datadir/c\\datadir=$database_path" /etc/my.cnf
/etc/init.d/mysqld restart

#Apache Configuration
which apachectl > /dev/null
(($?==0)) || yum -q -y install httpd
mkdir -p $apache_path > /dev/null
grep ^DocumentRoot /etc/httpd/conf/httpd.conf > /dev/null
if (($?==0));then
  sed -i "/^DocumentRoot/c\\DocumentRoot $apache_path" /etc/httpd/conf/httpd.conf
else
  echo "DocumentRoot $apache_path" >> /etc/httpd/conf/httpd.conf
fi
grep ^Listen /etc/httpd/conf/httpd.conf > /dev/null
if (($?==0));then
  sed -i "/^Listen/c\\Listen $apache_port" /etc/httpd/conf/httpd.conf
else
  echo "Listen $apache_port" >> /etc/httpd/conf/httpd.conf
fi
echo "Now apache home directory is $apache_path, using port $apache_port" > $apache_path/index.html
#apachectl will be restart later

#Samba Configuration
which samba > /dev/null
(($?==0)) || yum -q -y install samba
(grep "path = $share_path" /etc/samba/smb.conf | grep -v '#') && (grep ^[$share_name] /etc/samba/smb.conf)
if (($?==1));then
  echo "       [$share_name]
       comment = Public samba share
       path = $share_path
       public = yes
       writable = yes
       printable = no
       write list = +root" >> /etc/samba/smb.conf
  /etc/init.d/smb restart > /dev/null
fi

#Subversion Configuration
rpm -q subversion > /dev/null
(($?==1)) && yum -q -y install subversion
rpm -q mod_dav_svn > /dev/null
(($?==1)) && yum -q -y install mod_dav_svn
mkdir -p $svn_path/$svn_repo
svnadmin create $svn_path/$svn_repo/project1
chown -R apache:apache $svn_path
apachectl restart

#Daily and Monthly cronjob
[ -f $backup_daily ] && cp $backup_daily /etc/cron.daily/
[ -f $backup_monthly ] && cp $backup_monthly /etc/cron.monthly/
/etc/init.d/crond restart > /dev/null

#If you want to enable SELinux again, please uncomment next line
#setenforce 1
