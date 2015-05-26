#!/usr/bin/perl -w
use strict;

my $words = 0;
while (<STDIN>) {
	#$words += scalar(split(/[a-zA-Z]/, $_));
	my @items = split(/[^A-Za-z]/, $_);
	my @new;
	foreach(@items){
	    if( ( defined $_) and !($_ =~ /^$/ )){
	        push(@new, $_);
	    }
	}
	$words += scalar(@new);
}
print "$words words";

