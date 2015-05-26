#!/usr/bin/python
import fileinput, re
for line in fileinput.input():
	line = re.sub(r'[aeiou]', '', line)
	print line,
