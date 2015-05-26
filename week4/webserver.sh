#!/bin/sh

# A webserver written in shell
# written by andrewt@cse.unsw.edu.au as a COMP2041 example

# You probably don't need to change this file
# It runs handle_request.sh for each http_request
# You do need to change handle_request.sh


# most webservers use  port 80 (or 443 for https)
# We use port 2041 as port 80 isn't available to normal users
# and may be in use by a web server already

port=12345

#local an appropriate netcat binary

netcat_binary=`command -v nc.traditional 2> /dev/null` ||
   netcat_binary=`command -v netcat 2> /dev/null` ||
   	  netcat_binary=`command -v nc 2> /dev/null`

if test ! -x $netcat_binary
then
	echo "$0: netcat not available" 1>&2
	exit 1
fi

# kill any instances of this script & netcat already running
# otherwise the port 2041 wouldn't be available

# pkill/pgrep could be used here
ps -ef|
egrep "(sh .*\b$0|$netcat_binary.*$port)"|
egrep -v "\b(egrep|$$)\b"|
sed 's/^[^ ]* *//;s/ .*//'|
xargs -r kill -9 2>/dev/null

echo "Access webserver via http://127.0.0.1:$port/"

while $netcat_binary -vvl localhost -p $port -c ./handle_request.sh
do
	sleep 1
done