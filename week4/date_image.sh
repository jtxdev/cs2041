#!/bin/bash

for i;
do
date=$(echo `ls -l "$i"` | cut -f6-8 -d' ')
convert -gravity south -pointsize 36 -annotate 0 "$date" "$i" temp.jpg
done
