#!/usr/bin/perl -w

@line = <STDIN>;
for ($line_number = 0; $line_number < $#line + 1; $line_number++) {
	$seed = rand(42);
	$test = $seed % 10;
	print "LOL $test\n";
	print $line[$line_number];
}