#!/bin/sh
# Output some simple HTML

IPADDR="$(echo `env` | sed 's/.*REMOTE_ADDR=\(.*\)\s.*/\1/' | cut -f1 -d' ' )"

#echo "$IPADDR"

HOSTNAME="$(echo `host $IPADDR` | cut -f2 -d':' | sed 's/Address//')"

#echo "$HOSTNAME"

BROWSER="$(echo `env` | sed 's/.*HTTP_USER_AGENT=\(.*\) SERVER_PORT=80.*/\1/')"



echo "Content-type: text/html

<!DOCTYPE html>
<html lang=\"en\"><head>
<title>IP, Host and Browser IP</title>
<style type=\"text/css\">
table{border-collapse:collapse;margin:0 auto;line-height:20px;width:728px;table-layout:fixed;}
tr{height:30px;}
td{border: solid 1px;padding: 0px 10px;}
</style>
</head>
<body>
<table id=\"info_table\">
<tbody><tr><td>Browser IP Address</td><td>$IPADDR
</td></tr><tr><td>Browser Hostname</td><td>$HOSTNAME
</td></tr><tr><td>Browser</td><td>$BROWSER
</td></tr></tbody></table>"


