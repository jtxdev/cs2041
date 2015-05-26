#!/usr/bin/python

from string import maketrans
import fileinput

intab = "0123456789"
outtab = "<<<<<5>>>>"
for lines in fileinput.input():
	print lines.translate(maketrans(intab, outtab)),;
