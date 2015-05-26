#!/usr/bin/perl
use warnings;
use strict;

my @course; 
my $url = "http://www.timetable.unsw.edu.au/current/$ARGV[0]KENS\.html";
open F, "wget -q -O- '$url'|" or die;
while (my $line = <F>) {
	if ($line =~ />[A-Z]{4}[0-9]{4}/) {
		my $course = $&;
		$course =~ s/>//;
		print "$course\n";
	}
}
