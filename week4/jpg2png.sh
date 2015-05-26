#!/bin/bash

shopt -s nullglob
for file in *.jpg
do
	#echo $file
	temp=$(echo $file | cut -f1 -d'.')
	#echo $temp
	if [ -e "$temp".png ]
		then 
			echo "$temp".png already exists
		else
			convert "$temp".jpg "$temp".png
			rm "$temp".jpg
	fi
done