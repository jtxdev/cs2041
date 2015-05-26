#!/usr/bin/perl -w
# written by andrewt@cse.unsw.edu.au as a COMP2041 lecture example
# Count the number of lines on standard input.

$line_count = 0;
while (<STDIN>) {
	$line_count++;
}
print "$line_count lines\n";
