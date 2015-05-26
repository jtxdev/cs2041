#!/bin/bash
SMALL="Small files:"
MEDIUM="Medium-sized files:"
LARGE="Large files:"
for file in *
do
	size=`wc -l < $file`
    if [ $size -lt 10 ]; then
        SMALL="$SMALL $file"
    elif [ $size -lt 100 ]; then
    	MEDIUM="$MEDIUM $file"
    else 
    	LARGE="$LARGE $file"
    fi
done
    echo $SMALL
    echo $MEDIUM
    echo $LARGE