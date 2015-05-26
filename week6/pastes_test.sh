#!/bin/bash

echo "Running /usr/bin/paste -s $@"
/usr/bin/paste -s /home/cs2041/public_html/lab/perl/paste/data? >output1
echo "Running ./pastes.pl $@"
./pastes.pl /home/cs2041/public_html/lab/perl/paste/data? >output2
echo "Running diff on the output"
result=$(echo `diff output1 output2`)
blank=""
if [ $result == $blank ] 
	then
		echo "Test succeeded - output of ./pastes.pl matched /usr/bin/paste"
	else
		echo $result
fi