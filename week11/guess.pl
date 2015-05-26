#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);

# Simple CGI script written by andrewt@cse.unsw.edu.au
# Outputs a form which will rerun the script
# An input field of type hidden is used to pass an integer
# to successive invocations

$max_target = 99;

print header, start_html(-bgcolor=>'white','A Simple Example');
warningsToBrowser(1);

if (!defined param("target")) {
        my $target = int (rand ($max_target + 1));
        print "I've  thought of number 0..$max_target\n";
        param('target', $target);
} elsif (defined param("guess")) {
        my $target = param('target');
        my $guess = param('guess');
        if ($guess == $target) {
            print "You guessed right, it was $target.";
            print end_html;
            exit;
        } elsif ($guess < $target) {
                print "Its higher than $guess.";
        } else {
                print "Its lower than $guess.";
        }
}

print start_form;
print 'Enter your guess: ';
print textfield('guess');
print hidden('target');
print end_form;
print end_html;