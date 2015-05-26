#!/usr/bin/perl -w

@files = ();
$N=10;
$flag=0;

if ($#ARGV == -1) {
	@line = <STDIN>;
	$init = $#line - $N + 1;
    if ($init < 0) {
    	$init = 0;
    }
	for ($line_number = $init; $line_number < $#line + 1; $line_number++) {
		print $line[$line_number];
	}
} elsif ($ARGV[0] =~ /-[0-9]*$/) {
	if ($#ARGV > 1) {
		$flag=1;
	}
	$N=-1 * $ARGV[0];
	for ($i = 1; $i < $#ARGV + 1; $i++) {
		push @files, $ARGV[$i];
	}
} else {
	if ($#ARGV > 0) {
		$flag=1;
	}
	foreach $arg (@ARGV) {
	    push @files, $arg;
	}
}

foreach $f (@files) {
    open(F,"<$f") or die "$0: Can't open $f: $!\n";
    if ($flag == 1) {
    	print "==> $f <==\n";
    }
    @line = <F>;
    $init = $#line - $N + 1;
    if ($init < 0) {
    	$init = 0;
    }
	for ($line_number = $init; $line_number < $#line + 1; $line_number++) {
		print $line[$line_number];
	}
    close(F);
}