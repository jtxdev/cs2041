#!/usr/bin/python

import sys
import fileinput
import re
import glob
import string
import operator
import math
import collections

for arg in sys.argv[1:]:

	myhash = collections.defaultdict(dict)
	myhash2 = collections.defaultdict(dict)
	targets = [];
	poets = [];

	for poet in glob.glob("poets/*.txt"):
		m = re.search('(?<=poets/)\w+', poet);
		poet = m.group(0).replace("_", " ")
		myhash2[poet]['scoreisnotaword'] = 0;
		poets.append(poet);


	a = open(arg, 'r');
	inputtext = [];
	for lines in a:
		lines = lines.lower()
		inputtext += re.split(r'[^a-zA-Z]', lines);
	targets += filter(None, inputtext);

	for file in glob.glob("poets/*.txt"):
		words = [];
		input = [];
		poet = file;
		m = re.search('(?<=poets/)\w+', file);
		poet = m.group(0)
		poet = poet.replace("_", " ")
		f = open(file, 'r');
		for lines in f:
			lines = lines.lower()
			input += re.split(r'[^a-zA-Z]', lines);
		words += filter(None, input);
		for k in words:
			myhash[poet][k] = myhash[poet].setdefault(k, 0) + 1
		myhash2[poet]['totalisnotaword'] = len(words)
		#counter = words.count((sys.argv[1]).lower());
		#print "%(counter)4d/%(words)6d = %(frequency).9f %(poet)s" % {"counter": counter, "words": len(words), "frequency": float(counter)/len(words), "poet": poet}
		#print "log((%(counter)d+1)/%(words)6d) = %(frequency)8.4f %(poet)s" % {"counter": counter, "words": len(words),

	d = collections.defaultdict(int)
	for target in targets:
		#print target;
		for poet in glob.glob("poets/*.txt"):
			m = re.search('(?<=poets/)\w+', poet);
			poet = m.group(0).replace("_", " ")
			d[target] = myhash[poet].setdefault(target, 0);
			myhash2[poet]['scoreisnotaword'] += math.log(((float(d[target]) + 1)/myhash2[poet]['totalisnotaword']));

	s = collections.defaultdict(int);
	for poet in poets:	
		s[poet] = myhash2[poet]['scoreisnotaword']

	#for p in sorted(s, key=s.get, reverse=True):
	#	print p

	#for poet in poets:	
		#print myhash2[poet]['scoreisnotaword'];
	#	print "%(poem)s most resembles the work of %(poet)s (log-probability=%(lp)5.1f)\n" % {"poem": arg, "poet": poet, "lp": myhash2[poet]['scoreisnotaword']}

	poet = sorted(s, key=s.get, reverse=True)[0]
	print "%(poem)s most resembles the work of %(poet)s (log-probability=%(lp)5.1f)" % {"poem": arg, "poet": poet, "lp": myhash2[poet]['scoreisnotaword']}


