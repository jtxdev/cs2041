#!/usr/bin/perl -w
# written by andrewt@cse.unsw.edu.au as a COMP2041 lecture example
# Count the number of lines on standard input.

foreach $line (<STDIN>) {
    push @lines, $line
}
   
$i = @lines - 1;
while ($i >= 0) {
    print $lines[$i];
    $i = $i - 1;
}