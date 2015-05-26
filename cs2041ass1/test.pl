#!/usr/bin/perl -w

my $oldrange = "\(jim\)";
my $newrange = "(lol)";

print "$oldrange\n";
$line = $oldrange;

$line =~ s/$oldrange/$newrange/gee;
print "$line\n";