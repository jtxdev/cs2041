#!/usr/bin/python
# written by andrewt@cse.unsw.edu.au as a 2041 lecture example
# count how many people enrolled in each course
# run as count_enrollments.py enrollments
import fileinput, re

course_names = {}
for line in open("course_codes"):
    m = re.match(r'(\S+)\s+(.*\S)', line)
    if m:
        course_names[m.group(1)] = m.group(2);

count = {}
for line in fileinput.input():
    course = re.sub(r'\|.*\n', '', line)
    if course in count:
        count[course] += 1
    else:
        count[course] = 1

for course in sorted(count.keys()):
    print  "%s has %s students enrolled"%(course_names[course], count[course])
