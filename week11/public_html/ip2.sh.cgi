#!/bin/sh
# Output some simple HTML

IPADDR="$(echo `/sbin\/ifconfig` | cut -f8 -d':' | cut -f1 -d' ')"

NEWHOSTNAME="$(echo `host $IPADDR`)"

#echo "$HOSTNAME"

NEWHOSTNAME="$(echo "$HOSTNAME")"

#echo "$NEWHOSTNAME"



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
</td></tr><tr><td>Browser Hostname</td><td>$NEWHOSTNAME
</td></tr><tr><td>Browser</td><td>Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17
</td></tr></tbody></table>"


