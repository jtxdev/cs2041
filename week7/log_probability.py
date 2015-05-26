#!/usr/bin/python

import sys
import fileinput
import re
import glob
import string
from string import maketrans
import math

for file in glob.glob("poets/*.txt"):
	words = [];
	input = [];
	f = open(file, 'r');
	for lines in f:
		lines = lines.lower()
		input += re.split(r'[^a-zA-Z]', lines);
	words += filter(None, input);
	counter = words.count((sys.argv[1]).lower());
	poet = file;
	m = re.search('(?<=poets/)\w+', file);
	poet = m.group(0)
	poet = poet.replace("_", " ")
	#print "%(counter)4d/%(words)6d = %(frequency).9f %(poet)s" % {"counter": counter, "words": len(words), "frequency": float(counter)/len(words), "poet": poet}
	print "log((%(counter)d+1)/%(words)6d) = %(frequency)8.4f %(poet)s" % {"counter": counter, "words": len(words), "frequency": math.log((float(counter + 1)/len(words))), "poet": poet}