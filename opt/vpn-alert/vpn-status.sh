#!/usr/bin/env bash

# @Purpose It sends mail alert only if VPN service goes down in Regions
# @Background   Meant to be run as a cronjob. Requires that awscli is installed.
# @Usage: vpn-status.sh
# 

#Function for mailalert in HTML Format
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
    <th>VPN Region</th>
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

#mail_alert 'VPN Status' 'success'

#Alert for N.Virginia VPN
ssh -i /opt/vpn-alert/access.pem ec2-user@34.225.36.174 sudo ipsec verify | grep FAILED
if [ $? -eq 0 ]; then
        printf "$(date +%Y-%m-%d:%H-%M) VPN Status failed for Oregon region!\n"
        mail_alert 'N.Virginia' 'Failed'| mutt  -e "set content_type=text/html"  -e "set send_charset=utf-8"  -s "N.Virginia VPN Status - $(date +%Y-%m-%d_%H-%M)" devops@orzota.com
else
        printf "$(date +%Y-%m-%d:%H-%M) VPN is working fine in N.Virginia region!\n"
fi


#Alert for Ohio VPN
ssh -i /opt/vpn-alert/access.pem ec2-user@13.59.234.26  sudo ipsec verify | grep FAILED
if [ $? -eq 0 ]; then
        printf "$(date +%Y-%m-%d:%H-%M) VPN Status failed for Oregon region!\n"
        mail_alert 'Ohio' 'Failed'| mutt  -e "set content_type=text/html"  -e "set send_charset=utf-8"  -s "Ohio VPN Status - $(date +%Y-%m-%d_%H-%M)" devops@orzota.com
else
        printf "$(date +%Y-%m-%d:%H-%M) VPN is working fine in Ohio region!\n"
fi

#Alert for Oregon VPN
ssh -i /opt/vpn-alert/access.pem ec2-user@34.212.224.32 sudo ipsec verify | grep FAILED
if [ $? -eq 0 ]; then
	printf "$(date +%Y-%m-%d:%H-%M) VPN Status failed for Oregon region!\n"
        mail_alert 'Oregon' 'Failed'| mutt  -e "set content_type=text/html"  -e "set send_charset=utf-8"  -s "Oregon VPN Status - $(date +%Y-%m-%d_%H-%M)" devops@orzota.com 
else
	printf "$(date +%Y-%m-%d:%H-%M) VPN is working fine in Oregon region!\n"
fi


