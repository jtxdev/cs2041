#!/usr/bin/python

import sys
import fileinput
import re

words = [];
for lines in sys.stdin:
	words += re.split(r'[^a-zA-Z]', lines);
words = filter(None, words);
print repr(len(words)) + " words";