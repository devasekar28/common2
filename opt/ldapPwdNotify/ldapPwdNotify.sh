#!/bin/bash
#Usage: bash ldapPwdNotify.sh
#Example: bash ldapPwdNotify.sh

# Name	         : /opt/ldapPwdNotify/ldapPwdNotify.sh
# Pupose         : This script will send mail alert to the users whose password is going to be expired.
# DATE           : Wed Oct 11 16:31:09 IST 2017
# Author	 : Mahesh <mahesh@orzota.com>
# Version	 : 0.1
# Requirements   : postfix needs to be configured to send an email


ROOTDN="cn=Manager,dc=orzota,dc=com"
##Password in encrypted form. If you use some other encryption technology it must be decrypted and assigned##
#ROOTPW=`echo 2K@him2ia |openssl enc -base64 -d`
ROOTPW='2K@him2ia'
##Max password age in days##
MAXPWDAGE=90
RESTOU=uid
ADMINMAILID=devops@orzota.com
USRLST=/backup/unknown_users
cat /dev/null > $USRLST
DATE=$(date)
###Sending mail to user function###
smail() {
MAILID=`ldapsearch -w $ROOTPW -D $ROOTDN -b dc=orzota,dc=com mail -LLL |grep -i ^mail|awk '{print $2}'| grep $USERID`
 if [ -n "$MAILID" ]; then
 echo -e "$DATE-$USERID-$SUB"
 echo -e "Dear $USERID,\n\nPlease reset your LDAP SSH password.We're sorry for the inconvenience, but you are requested to change your password. \nHow to Change LDAP Password:\nSSH Login into Any LDAP client machine.\nFor example, SSH Login into this ldap client machine 34.193.71.124 using 3393 ssh port with LDAP Password and use passwd linux command to update LDAP password.\nExample: \nssh -p 3393 ldapuser@34.193.71.124\nPassword should met following policy. \n1. Password should have one uppercase,number and symbols. \n2. Password should contain minimum length of 8 characters.\n3. Number of password that are kept in history which can't be used continuously for 3 times.\nIf password didn’t met above dependencies, user will get password constraint error while changing password and password will not be updated.
\n\nKindly contact us on devops@orzota.com if you have any queries.\n\nBest Regards,\nOrzota DevOps Team"|mailx -s "$SUB" $MAILID
 else
 echo "$USERID" >> $USRLST
 fi
}

for i in `ldapsearch -w $ROOTPW -D $ROOTDN -b dc=orzota,dc=com -LLL "(&(userpassword=*)(pwdchangedtime=*)(!(ou:dn:=$RESTOU)))" dn|awk '{print $2}'`
do
 #echo $i
 USERID=`echo $i|awk -F, '($1~uid){print $1}'|awk -F= '{print $2}'`
 PWCGE=`ldapsearch -xw $ROOTPW -D $ROOTDN -b $i -LLL pwdchangedtime|grep -i ^pwdchangedtime|awk '{print $2}'|sed 's/Z//'`
 EXDTE=`echo $PWCGE |cut -c 1-8`
 EXTME=`echo $PWCGE |cut -c 9- |sed 's/.\{2\}/&:/g' |cut -c -8`
 EXSEC=`date -d "$EXDTE $EXTME" +%s`
 CDSEC=`date -u +%s`
 DIFF=`expr \( $CDSEC / 86400 \) - \( $EXSEC / 86400 \)`

 if [ "$DIFF" == `expr $MAXPWDAGE - 15` ]; then
 SUB="User $USERID LDAP password expire in 15 days"
 smail
 elif [ "$DIFF" == `expr $MAXPWDAGE - 10` ]; then
 SUB="User $USERID LDAP password expire in 10 days"
 smail
 elif [ "$DIFF" == `expr $MAXPWDAGE - 5` ]; then
 SUB="User $USERID LDAP password expire in 5 days"
 smail
 elif [ "$DIFF" == `expr $MAXPWDAGE - 4` ]; then
 SUB="User $USERID LDAP password expire in 4 days"
 smail
 elif [ "$DIFF" == `expr $MAXPWDAGE - 3` ]; then
 SUB="User $USERID LDAP password expire in 3 days"
 smail
 elif [ "$DIFF" == `expr $MAXPWDAGE - 2` ]; then
 SUB="User $USERID LDAP password expire in 2 days"
 smail
 elif [ "$DIFF" == `expr $MAXPWDAGE - 1` ]; then
 SUB="User $USERID LDAP password expire in 1 day"
 smail
 elif [ "$DIFF" == "$MAXPWDAGE" ]; then
 SUB="user $USERID password will expire today at $EXTME UTC"
 smail
 elif [ $DIFF -gt 90 ]; then
 SUB="user $USERID Password has been expired"
 echo $DATE-$USERID-$SUB
 fi
 unset USERID PWCGE EXDTE EXTME EXSEC CDSEC DIFF i
done

###Send mail to Admin with non mail-id users###
 if [ -s "$USRLST" ]; then
 echo -e "Listed users mail id not available in Orzota LDAP directory. Please notify them to reset password.\n\n`cat $USRLST`\n\nby\nOrzota LDAP Admin"|mailx -s "password going to expire users list" $ADMINMAILID
 fi

