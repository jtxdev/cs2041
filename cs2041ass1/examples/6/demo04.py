#!/usr/bin/python
# written by andrewt@cse.unsw.edu.au as a COMP2041 lecture example
# Count the number of lines on standard input.

import sys
lines = []
for line in sys.stdin:
    lines.append(line)
    
i = len(lines) - 1
while i >= 0:
    print lines[i],
    i = i - 1
