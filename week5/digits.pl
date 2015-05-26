#!/usr/bin/perl -w
use strict;

while ( $line = <STDIN> ) {
	$line =~ tr/0123456789/<<<<<5>>>>/;
    print $line;
}
