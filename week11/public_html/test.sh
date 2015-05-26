#!/bin/sh
# Simple CGI script written by andrewt@cse.unsw.edu.au
# Print some HTML plus the environment
# passed to CGI script by the web server

cat <<eof
Content-type: text/html

<!DOCTYPE html>
<html lang="en">
<head></head>
<body>
<h2>Environment Variables</h2>
<pre>
`env`
</pre>
</body>
</html>
eof





