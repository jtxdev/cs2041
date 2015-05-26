#!/usr/bin/perl -w

while ($line = <>) {
	$line =~ s/[aeiou]//g;
	print $line
}