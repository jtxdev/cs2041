#!/bin/bash

for i;
do
	#echo $i
	display "$i"
	echo "Address to e-mail this image to?"
	read EMAIL
	echo "Message to accompany image?"
	read MSG
	echo '$MSG'|mutt -s 'Something' -a $i -- $EMAIL
	echo "$i sent to $EMAIL"
done