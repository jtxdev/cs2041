#!/bin/sh

# Run from webserver.sh to handle a single http request
# written by andrewt@cse.unsw.edu.au as a COMP2041 example

read http_request || exit 1

status_line="HTTP/1.0 200 OK"
content_type="text/plain"
request="$(echo "$http_request" | cut -f2 -d' ')"
if [ -d ~/public_html$request ]; then
	if [ -e ~/public_html$request/index.html ]; then
		content=$(echo `cat ~/public_html$request/index.html`)
		content_length=`echo "$content"|wc -c`
		content_type="html"
	echo "HTTP/1.0 200 OK"
	echo "Content-type: $content_type"
	echo "Content-length: $content_length"
	echo	
	echo "$content"
	else
		#taken from
		INDEX=`ls -1 ~/public_html$request | sed "s/^.*/      <li\>\<a\ href=\"\\\\$request\/&\"\>&\<\\/a\>\<\\/li\>/" | sed 's/\/\//\//'`
	echo "<html>
	  <head><title>Index of ~/public_html$request</title></head>
	  <body>
	    <h2>Index of ~/public_html$request</h2>
	    <hr>
	    <ui>
	<li><a href="..">Parent Directory</a></li>
	$INDEX
	    <ui>
	  </body>
	</html>
	"
	fi
elif [ -e ~/public_html$request ]; then
		content=$(echo `cat ~/public_html$request`)
		content_length=`echo "$content"|wc -c`
		ishtml="$(echo "$request" | grep ".html$" | cut -f2 -d'.')" 
		if [ "$ishtml" = "html" ]; then
			content_type="html"
		fi
	echo "HTTP/1.0 200 OK"
	echo "Content-type: $content_type"
	echo "Content-length: $content_length"
	echo	
	echo "$content"
else
 	content="LEL YOU BROKED IT! 404 :'(s"
	content_length=`echo "$content"|wc -c`
	echo "HTTP/1.0 404 Not Found"
	echo "Content-type: $content_type"
	echo "Content-length: $content_length"
	echo	
	echo "$content"
fi
exit 0