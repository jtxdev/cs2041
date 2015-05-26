#!/usr/bin/python

import sys
import fileinput
import re


words = [];
target = sys.argv[1];
for lines in sys.stdin:
	my_regex = re.compile(r'\b%s\b' % target, re.IGNORECASE);
	words += re.findall(my_regex, lines);
print target.lower() + " occurred " + repr(len(words)) + " times";
