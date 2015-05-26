#!/usr/bin/perl -w
use strict;

my $count = 0;
my $words = 0;
my $target = lc($ARGV[0]);
my %poets = ();
foreach my $poet (glob "poets/*.txt") {
	$count = 0;
	$words = 0;
	open(F,"<$poet") or die "$0: Can't open $poet: $!\n";
	while (<F>) {
		#$words += scalar(split(/[a-zA-Z]/, $_));
		my @items = split(/[^A-Za-z]/, $_);
		foreach(@items){
		    if( ( defined $_) and ($_ =~ /^$target$/i )){
		        $count++;
		    }
		    if( ( defined $_) and !($_ =~ /^$/ )){
		        $words++;
		    }
		}
	}
	$poet =~ s/poets\///;
	$poet =~ s/\.txt//;
	$poet =~ tr/_/ /;
	$poets{"$poet"}{"$target"} = $count;
	$poets{"$poet"}{total} = $words;
	printf "%4d/%6d = %.9f %s\n", $poets{"$poet"}{"$target"}, $poets{"$poet"}{total}, $poets{"$poet"}{"$target"}/$poets{"$poet"}{total}, $poet;
}
