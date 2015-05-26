#!/usr/bin/perl -w

my $oldrange = "(2, 100)"
my $newrange = "(2..100 - 1)"

$line = $oldrange;

$line =~ s/$oldrange/$newrange/;
print "$line\n";