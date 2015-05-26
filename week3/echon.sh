#!/bin/bash
USAGE="Usage: ./echon.sh <number of lines> <string>"
ERROR1="./echon.sh: argument 1 must be a non-negative integer"
if [ "$#" -ne 2 ]; then
	echo "$USAGE"
else 
	test $1 -lt 0 2>/dev/null
		if [ $? = 1 ]; then
			for ((i = 1; i <= $1; i++)); 
			do
	   			echo $2
			done
		else
			echo $ERROR1
		fi
fi
