#!/usr/bin/env bash

#
# @Purpose 		Creates an image (AMI) of the given EC2 instance
# @Background 	Meant to be run as a cronjob. Requires that awscli is installed. Assumes that the 
# instance running this command has the permission ec2:CreateImage assigned via IAM.
#
# @Usage: 		create-ec2-image <instance-id>
#

#Function for mail alert HTML Format
mail_alert () {
str1="<!DOCTYPE HTML>
<html
<head>
<style>
table, th, td {
    border: 1px solid black;
    border-collapse: collapse;
}
th, td {
    padding: 5px;
    text-align: left;
}

</style>
</head>
<body>
<table>
  <tr>
    <th>Backup Type</th>
    <th>Status</th> 
  </tr>
<tr style=\"height:30px;\">
<td><strong>"
str2="</strong></td>
<td><strong>"
str3="</strong></td>
</tr>
</table>
</body>
</html>"
#Concatenating String 
finalstr=$str1$1$str2$2$str3
echo $finalstr
}
#mail_alert 'OpenLDAP Image Backup' 'success'

DATE=$(date +%Y-%m-%d) 
AMI_NAME="OpenLDAP Weekly Backup - $DATE"
AMI_DESCRIPTION="OpenLDAP_Weekly_Backup-$DATE"
INSTANCE_ID=$1
RETENTION_DATE=$(date +%Y-%m-%d --date="28 days ago")
#echo $RETENTION_DATE
#Deleting 4 weeks older image
#if [[ $(aws ec2 describe-images --filters Name=description,Values=OpenLDAP_Weekly_Backup-$RETENTION_DATE | grep ImageId | awk '{print $2}' | tr -d '"','') ]]
if [[ $(aws ec2 describe-images --filters Name=description,Values=OpenLDAP_Weekly_Backup-$RETENTION_DATE | awk '{ print $7}' | grep ami) ]]
then
	AMIDELETE=$(aws ec2 describe-images --filters Name=description,Values=OpenLDAP_Weekly_Backup-$RETENTION_DATE | awk '{ print $7}' | grep ami) 
        echo $AMIDELETE
	aws ec2 deregister-image --image-id "$AMIDELETE"
	echo "$(date +%Y-%m-%d:%H-%M)-$AMIDELETE ami is deleted"
else
	echo "$(date +%Y-%m-%d:%H-%M)-No AMI Present on the date of retention period"
fi

#Create weekly image backup for OpenLDAP

printf "$(date +%Y-%m-%d:%H-%M)-Requesting AMI for instance $1...\n"
aws ec2 create-image --instance-id $1 --name "$AMI_NAME" --description "$AMI_DESCRIPTION" --no-reboot
if [ $? -eq 0 ]
then
	printf "$(date +%Y-%m-%d:%H-%M)- AMI request complete!\n"
	echo "$(date +%Y-%m-%d:%H-%M)- Weekly Backup-$DATE of $INSTANCE_ID has been completed Successfully"
	mail_alert 'OpenLDAP Image Backup' 'success'| mutt  -e "set content_type=text/html"  -e "set send_charset=utf-8"  -s "Weekly Backup - $DATE" devops@orzota.com	
else
	printf "$(date +%Y-%m-%d:%H-%M)- AMI does not completed!\n"
	echo "$(date +%Y-%m-%d:%H-%M)- Weekly Backup-$DATE of $INSTANCE_ID has been Failed"
	mail_alert 'OpenLDAP Image Backup' 'Failed'| mutt  -e "set content_type=text/html"  -e "set send_charset=utf-8"  -s "Weekly Backup - $DATE" devops@orzota.com
fi
