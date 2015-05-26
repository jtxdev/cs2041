#!/usr/bin/perl -w
use strict;

my $count = 0;
my $target = $ARGV[0];
while (<STDIN>) {
	#$words += scalar(split(/[a-zA-Z]/, $_));
	my @items = split(/[^A-Za-z]/, $_);
	my @new;
	foreach(@items){
	    if( ( defined $_) and ($_ =~ /^$target$/i)){
	        $count++;
	    }
	}
}
my $word = lc($target);
print "$word occurred $count times";