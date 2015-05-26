#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
for subset in {0..5}
do
	if [ $subset -lt 5 ] ; then
		for file in $DIR/examples/$subset/*.py
		do
			echo "Running ./python2perl.pl $file"
			./python2perl.pl $file >h.pl
			if [ $# -eq "1" ] && [ $1 == "--show" ] ; then
				cat h.pl
			fi
			echo "Testing diffences in output"
			echo "Testing pythonfile"
			python -u $file <input > py.output 
			echo "Testing perlfile"
			perl h.pl <input > pl.output 
			if diff py.output pl.output &> /dev/null ; then
				echo SUCCESS
			else 
				if [ $# -eq "1" ] && [ $1 == "--showall" ] ; then
					cat h.pl
					cat py.output
					cat pl.output
				fi
				echo FAIL
			fi
		done
	else 
		for file in $DIR/examples/$subset/*.py
		do
			echo "Running ./python2perl.pl $file"
			./python2perl.pl $file >h.pl
			if [ $# -eq "1" ] && [ $1 == "--show" ] ; then
				cat h.pl
			fi
			echo "Testing diffences in output"
			if [[ $file != *echo* ]] ; then
				echo "Testing pythonfile"
				python -u $file <enrollments > py.output 
				echo "Testing perlfile"
				perl h.pl <enrollments > pl.output 
			else 
				if [[ $file == *echon* ]] ; then
					echo "Testing pythonfile"
					python -u $file 3 lol > py.output 
					echo "Testing perlfile"
					perl h.pl 3 lol > pl.output
				else
					echo "Testing pythonfile"
					python -u $file 1 2 3 4 5 a b c d e > py.output 
					echo "Testing perlfile"
					perl h.pl 1 2 3 4 5 a b c d e > pl.output
				fi
			fi
			if diff py.output pl.output &> /dev/null ; then
				echo SUCCESS
			else 
				if [ $# -eq "1" ] && [ $1 == "--showall" ] ; then
					cat h.pl
					cat py.output
					cat pl.output
				fi
				echo FAIL
			fi
		done
	fi
done
# scp python2perl.pl cs2041test.sh cjth726@login.cse.unsw.edu.au:/import/ravel/1/cjth726/cs2041/ass1