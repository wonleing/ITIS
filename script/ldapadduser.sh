#!/bin/bash
source /etc/itis/server.conf
((`id -u` !=0 )) && echo "You need to be root to run add ldap user script!" && exit
(($# < 2)) && echo "Usage: ./$0 project_name user_list" && exit
pjname=$1
shift
userlist=$@
dcstring="dc=`echo $ldap_com | sed 's/\./,dc=/g'`"

echo -e "dn: ou=$pjname,$dcstring
ou: $pjname
objectClass: top
objectClass: organizationalUnit\n" > /tmp/ldapcache

for i in $userlist;do
  grep ^$i: /etc/passwd
  (($?)) && (useradd $i -d /home/$i;echo -e "$i\n$i" | passwd $i)
  echo -e "dn: uid=$i,ou=$pjname,$dcstring
uid: $i
objectClass: account
objectClass: top\n" >> /tmp/ldapcache
done

pkill slapd
touch $ldap_path/DB_CONFIG
slapadd -l /tmp/ldapcache
slapd

