#!/usr/bin/perl

use warnings;
use strict;
my $url1;
my $url2;

if ($ARGV[0] =~ /^-r$/) {
    $url1 = "http://www.handbook.unsw.edu.au/postgraduate/courses/2014/$ARGV[1]\.html";
    $url2 = "http://www.handbook.unsw.edu.au/undergraduate/courses/2014/$ARGV[1]\.html";
} else {
    $url1 = "http://www.handbook.unsw.edu.au/postgraduate/courses/2014/$ARGV[0]\.html";
    $url2 = "http://www.handbook.unsw.edu.au/undergraduate/courses/2014/$ARGV[0]\.html";
}
my @urls;
my @prereqs;
push @urls, $url1;
push @urls, $url2;

foreach my $url (@urls) {
    open F, "wget -q -O- '$url'|" or die;
    while (my $line = <F>) {
        if ($line =~ /Pre-*requisites*.[^<]*</i) {
            my $pq = $&;
            $pq = $& if ($pq =~ /.*Excl/);
            $pq = uc($pq);
            while ($pq =~ /[A-Z]{4}[0-9]{4}/i) {
                my $sub = $&;
                 push @prereqs, $sub;
                 if ($ARGV[0] =~ /^-r$/) {
                    my $url3 = "http://www.handbook.unsw.edu.au/undergraduate/courses/2014/$sub\.html";
                    my $url4 = "http://www.handbook.unsw.edu.au/postgraduate/courses/2014/$sub\.html";
                    push @urls, $url3;
                    push @urls, $url4;
                 }
                 $pq =~ s/$sub//;
            }
        }
    }
}
my %hash = map { $_, 1 } @prereqs;
my @unique = keys %hash;
my @alphapqs = sort @unique;
#my @alphapqs = sort @prereqs;
foreach my $arg (@alphapqs) {
    print "$arg\n";
}



