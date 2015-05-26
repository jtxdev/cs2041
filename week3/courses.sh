#!/bin/bash

wget -q -O- "http://www.handbook.unsw.edu.au/vbook2014/brCoursesByAtoZ.jsp?StudyLevel=Undergraduate&descr=$1" | grep "$1[0-9]*.html" | cut -f3 -d"<" | sed 's/\.html\">/ /' | sed 's/A href="http:\/\/www.handbook.unsw.edu.au\/undergraduate\/courses\/2014\///' | tr \< ' ' > file1
wget -q -O- "http://www.handbook.unsw.edu.au/vbook2014/brCoursesByAtoZ.jsp?StudyLevel=Postgraduate&descr=$1" | grep "$1[0-9]*.html" | cut -f3 -d"<" | sed 's/\.html\">/ /' | sed 's/A href="http:\/\/www.handbook.unsw.edu.au\/postgraduate\/courses\/2014\///' | tr \< ' ' > file2
cat file1 file2 | sed 's/[ \t]*$//' | sort | uniq