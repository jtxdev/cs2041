#!/usr/bin/perl

use strict;
use warnings;
my $url = "http://www.handbook.unsw.edu.au/postgraduate/courses/2014/$ARGV[0]\.html";
my $url2 = "http://www.handbook.unsw.edu.au/undergraduate/courses/2014/$ARGV[0]\.html";
my @prereqs;
open (my $F, "wget -q -O- $url $url2|") or die;
while (my $line = <$F>) {
	if ($line =~ m/<p>Prerequisites*:[^<]*</) {
		#print $line;
		my $pq = $&;
		while ($pq =~ /[A-Z]{4}[0-9]{4}/) {
			 push @prereqs, $&;
			 $pq =~ s/$&//;
		}
	}
}
my @alphapqs = sort @prereqs;
foreach my $arg (@alphapqs) {
	print "$arg\n";
}

