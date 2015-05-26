#!/usr/bin/python
#taken from lecture examples

import sys
if len(sys.argv) != 2:
    print >>sys.stderr, "Usage: %s <n>" % sys.argv[0]
    sys.exit(1)
m = 0
string = '@'
while  m  < int(sys.argv[1]):
    string =  string + string
    m += 1
print "String of 2^%d = %d characters created\n" % (m, len(string));