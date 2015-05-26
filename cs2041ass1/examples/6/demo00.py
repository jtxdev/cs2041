#!/usr/bin/python
#countlines taken from examples
import sys

line_count = 0
for line in sys.stdin:
    line_count += 1
print "%d lines" % line_count