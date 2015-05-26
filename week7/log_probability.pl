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
		my @new;
		foreach(@items){
		    if( ( defined $_) and ($_ =~ /^$target$/i )){
		        $count++;
		    }
		    if( ( defined $_) and !($_ =~ /^$/ )){
		        push(@new, $_);
		    }
		}
		$words += scalar(@new);
	}
	$poet =~ s/poets\///;
	$poet =~ s/\.txt//;
	$poet =~ tr/_/ /;
	$poets{"$poet"}{"$target"} = $count;
	$poets{"$poet"}{total} = $words;
	printf "log((%d+1)/%6d) = %8.4f %s\n", $poets{"$poet"}{"$target"}, $poets{"$poet"}{total}, log(($poets{"$poet"}{"$target"}+1)/$poets{"$poet"}{total}), $poet;
}