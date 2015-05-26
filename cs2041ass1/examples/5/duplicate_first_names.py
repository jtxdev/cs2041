#!/usr/bin/python
# Written by andrewt@cse.unsw.edu.au for COMP2041
# run as duplicate_first_names.py enrollments
# Report cases where there are multiple people
# of the same same first name enrolled in a course

import fileinput, re

cfn = {}
for line in fileinput.input():
    fields = line.split('|')
    course = fields[0]
    full_name = fields[2]
    m = re.match(r'.*,\s+(\S+)', full_name)
    if not m:
    	continue
    first_name = m.group(1)
    if course not in cfn:
    	cfn[course] = {}
    if first_name in cfn[course]:
    	cfn[course][first_name] += 1
    else:
    	cfn[course][first_name] = 1

for course in sorted(cfn.keys()):
	for first_name in sorted(cfn[course].keys()):
		n = cfn[course][first_name]
		if n > 1:
   			print "In %s there are %d people with the first name %s"%(course, n, first_name)
