#!/usr/bin/perl

use warnings;
use strict;

my $url1 = "http://www.handbook.unsw.edu.au/postgraduate/courses/2014/$ARGV[0]\.html";
my $url2 = "http://www.handbook.unsw.edu.au/undergraduate/courses/2014/$ARGV[0]\.html";
my @urls;
my @prereqs;
push @urls, $url1;
push @urls, $url2;

foreach my $url (@urls) {
    open F, "wget -q -O- '$url'|" or die;
    while (my $line = <F>) {
        if ($line =~ /^\s*<(script|style)/i) {
            while ($line = <F>) {
                last if $line =~ /^\s*<\/(script|style)/i;
            }
        }
        $line =~ s/&\w+;/ /g;
        $line =~ s/<[^>]*>//g;
        if ($line =~ /Prerequisites*.*\./) {
            my $pq = $&;
            while ($pq =~ /[A-Z]{4}[0-9]{4}/) {
                 push @prereqs, $&;
                 my $url3 = "http://www.handbook.unsw.edu.au/undergraduate/courses/2014/$&\.html";
                 push @urls, $url3;
                 $pq =~ s/$&//;
            }
        }
    }
}
my @alphapqs = sort @prereqs;
foreach my $arg (@alphapqs) {
    print "$arg\n";
}



