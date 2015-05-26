#!/usr/bin/python

import sys
import fileinput

for filename in sys.argv[1:]:
	infile = open(filename).readlines()
	i = len(infile)
	if (i - 10 < 0): 
		for line in infile:
	   			print line,
	else:
		for x in range(i-10, i):
			print infile[x],