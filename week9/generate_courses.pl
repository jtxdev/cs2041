#!/usr/bin/perl
use warnings;
use strict;

my @courses; 
my @compcourses;
my $line;


open(C,"<course_codes.txt") or die "$0: Can't open course_codes.txt: $!\n";

@courses = <C>;
chomp(@courses);

foreach $line (@courses) {
	if ($line =~ /COMP/) {
		push (@compcourses, $line);
	}
}

foreach $line (@compcourses) {
	print "$line\n";
}

