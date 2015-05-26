#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if test $# -lt 2
then
	echo "usage $0: <subset> <input> <options> | input: input enrollments |options --show and --showall"
	exit 1
fi

for file in $DIR/examples/$1/*.py
do
	echo "Running ./python2perl.pl $file"
	./python2perl.pl $file >h.pl
	if [ $# -eq "3" ] && [ $3 == "--show" ] ; then
		cat h.pl
	fi
	echo "Testing diffences in output"
	echo "Testing pythonfile"
	python -u $file <$2 > py.output 
	echo "Testing perlfile"
	perl h.pl <$2 > pl.output 
	if diff py.output pl.output &> /dev/null ; then
		echo SUCCESS
	else 
		if [ $# -eq "3" ] && [ $3 == "--showall" ] ; then
			cat h.pl
			cat py.output
			cat pl.output
		fi
		echo FAIL
	fi
done

# scp python2perl.pl cs2041test.sh cjth726@login.cse.unsw.edu.au:/import/ravel/1/cjth726/cs2041/ass1