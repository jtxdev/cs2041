#!/usr/bin/python

import sys

if len(sys.argv) != 3:
    print >>sys.stderr, "Usage: %s" % sys.argv[0]
    sys.exit(1)

for x in range(int(sys.argv[1])):
    print "%s" % sys.argv[2]

