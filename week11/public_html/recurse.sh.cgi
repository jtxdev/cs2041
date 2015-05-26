#!/bin/sh
# Output some simple HTML

count="$(echo `env` | grep -oE "REDIRECT_QUERY_STRING=[0-9]*" | sed 's/REDIRECT_QUERY_STRING=//')"
count2=$(($count + 1))

echo "Content-type: text/html

<!DOCTYPE html>
<html lang="en">
<head>
<title>Recurse</title>
</head
<body>
<b>Level $count2</b>: <a href="http://cgi.cse.unsw.edu.au/~cjth726/recurse.sh.cgi?$count2">Run me again<a/>
</body>
</html>"

