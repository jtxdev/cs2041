#!/usr/bin/python
#devowel taken from examples
import fileinput, re
for line in fileinput.input():
	line = re.sub(r'[aeiou]', '', line)
	print line,
