#!/usr/bin/perl -w
use strict;

foreach my $arg (@ARGV) {

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
		$poets{"$poet"} {scoreisnotaword} = 0;
	}
#print "End1\n";
#print "Start2\n";
	open(T,"<$arg") or die "$0: Can't open $arg: $!\n";
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
		my $poet = $file;
		$poet =~ s/poets\///;
		$poet =~ s/\.txt//;
		$poet =~ tr/_/ /;
		my @Fnew;
		while (<F>) {
			my @Fitems = split(/[^A-Za-z]/, $_);
			foreach my $word (@Fitems){
				$word = lc($word);
			    if( ( defined $word ) and !($word =~ /^$/ )){
			        push (@Fnew, $word);
			        $words++;
			        if ( !defined $poets{"$poet"}{"$word"} ) {
			        	$poets{"$poet"}{"$word"} = 1;
			    	} else {
			    		$poets{"$poet"}{"$word"}++;
			    	}
			    }
			}
		}
		$poets{"$poet"}{totalisnotaword} = $words;
		#print "$poet $words\n";
	}
	#print "End3";
	foreach $target (@Tnew) {
		$target = lc($target);
		foreach my $poet (glob "poets/*.txt") {
			$poet =~ s/poets\///;
			$poet =~ s/\.txt//;
			$poet =~ tr/_/ /;
			if ( !defined $poets{"$poet"}{"$target"} ) {
				$poets{"$poet"}{scoreisnotaword} = $poets{"$poet"}{scoreisnotaword} + log( 1 / $poets{"$poet"}{totalisnotaword} );
				#$poets{"$poet"}{"$target"} = $count;
			} else {
				$poets{"$poet"}{scoreisnotaword} = $poets{"$poet"}{scoreisnotaword} + log( ($poets{"$poet"}{"$target"} + 1) / $poets{"$poet"}{totalisnotaword} );
			}
		#print "\n";
		}
	}	
	#foreach my $poet ( sort { $poets{$b}{scoreisnotaword} <=> $poets{$a}{scoreisnotaword} } keys %poets ) {
	#	printf "%s: log_probability of %5.1f for %s\n", $ARGV[0], $poets{"$poet"} {scoreisnotaword}, $poet;
	#}
	my ($poet) = sort { $poets{$b}{scoreisnotaword} <=> $poets{$a}{scoreisnotaword} } keys %poets;

	printf "%s most resembles the work of %s (log-probability=%5.1f)\n", $arg, $poet, $poets{"$poet"}{scoreisnotaword};
}	



