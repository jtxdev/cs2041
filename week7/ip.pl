#!/usr/bin/perl -w
use strict;

my $count = 0;
my $words = 0;
my $target = "";
my %poets = ();
my @Tnew;

#print "Start1\n";
foreach my $poet (glob "poets/*.txt") {
	$poet =~ s/poets\///;
	$poet =~ s/\.txt//;
	$poet =~ tr/_/ /;
	$poets{"$poet"} {score} = 0;
}
#print "End1\n";
#print "Start2\n";
open(T,"<$ARGV[0]") or die "$0: Can't open $ARGV[0]: $!\n";
while (<T>) {
	my @Titems = split(/[^A-Za-z]/, $_);
	foreach (@Titems){
	    if( ( defined $_ ) and !($_ =~ /^$/ )){
			push (@Tnew, $_);
		}
	}
}
#print "End2\n";
#print "Start3\n";
foreach my $file (glob "poets/*.txt") {
	#print "current poet is: $poet ";
	$words = 0;
	open(F,"<$file") or die "$0: Can't open $file: $!\n";
	my @Fnew;
	while (<F>) {
		my @Fitems = split(/[^A-Za-z]/, $_);
		foreach (@Fitems){
		    if( ( defined $_) and !($_ =~ /^$/ )){
		        push (@Fnew, $_);
		        $words++;
		    }
		}
	}
	my $poet = $file;
	$poet =~ s/poets\///;
	$poet =~ s/\.txt//;
	$poet =~ tr/_/ /;
	$poets{"$poet"} {total} = $words;
	foreach $target (@Tnew) {
		if ( !defined $poets{"$poet"}{"$target"} ) {
			#print "firstloop";
			$count = 0;
			foreach (@Fnew){
			    if( ( defined $_) and ($_ =~ /^$target$/i )){
			        $count++;
			    }
			}
			$poets{"$poet"}{"$target"} = log( ($count+1) / $poets{"$poet"}{total} );
			#$poets{"$poet"}{"$target"} = $count;
		}
		$poets{"$poet"}{score} = $poets{"$poet"}{score} + $poets{"$poet"}{"$target"};
		#print "\n";
	}
}
#print "End3"
#foreach my $poet ( sort { $poets{$b}{score} <=> $poets{$a}{score} } keys %poets ) {
#	printf "%s: log_probability of %5.1f for %s\n", $ARGV[0], $poets{"$poet"} {score}, $poet;
#}
my ($poet) = sort { $poets{$b}{score} <=> $poets{$a}{score} } keys %poets;
printf "%s most resembles the work of %s (log-probability=-%5.1f)\n", $ARGV[0], $poet, $poets{"$poet"} {score};	
