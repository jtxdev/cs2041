#!/usr/bin/python

a = 10
b = 20
c = 0

if ( a and b ):
    print "Line 1 - a and b are true"
else:
    print "Line 1 - Either a is not true or b is not true"

if ( a or b ):
    print "Line 2 - Either a is true or b is true or both are true"
else:
    print "Line 2 - Neither a is true nor b is true"


a = 0
if ( a and b ):
    print "Line 3 - a and b are true"
else:
    print "Line 3 - Either a is not true or b is not true"

if ( a or b ):
    print "Line 4 - Either a is true or b is true or both are true"
else:
    print "Line 4 - Neither a is true nor b is true"

if not( a and b ):
    print "Line 5 - Either a is not true or b is not true"
else:
    print "Line 5 - a and b are true"
