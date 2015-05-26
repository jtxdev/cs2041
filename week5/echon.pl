#!/usr/bin/perl -w

if (@ARGV == 2) {
	for ($i = 0; $i < $ARGV[0]; $i++) {
		print "$ARGV[1]\n";
	}
} else {
	print "Usage: ./echon.pl <number of lines> <string>\n";
}