#!/usr/bin/perl -w
# Simple CGI script written by andrewt@cse.unsw.edu.au
# Outputs a form which will rerun the script
# An input field of type hidden is used to pass an integer
# to successive invocations
# Two submit buttons are used to produce different actions

use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);

print header, start_html('A Guessing Game Player');
warningsToBrowser(1);

$max_target = 100;
$min_target = 0;

if (defined param("Correct?")) {
    print h1("I win!"),
          end_html;
} elsif (defined param("x")) {
    if (defined param("Higher?")) {
        $min_target = param("x");
        $max_target = param("max");
        $hidden_variable = findmiddle($max_target, $min_target);
    } else {
        $max_target = param("x");
        $min_target = param("min");
        $hidden_variable = findmiddle($max_target, $min_target);
    }
} else {
    $hidden_variable = findmiddle($max_target, $min_target);
}

if (!defined param("Correct?")) {
    param('x', $hidden_variable);
    param('max', $max_target);
    param('min', $min_target);
    print h2("My guess is $hidden_variable"),
          start_form,
          hidden('x'),
          hidden('max'),
          hidden('min'),
          submit('Higher?'),
          submit('Correct?'),
          submit('Lower'),
          end_form,
          end_html;
}
sub findmiddle
{
    if ((($_[0] + $_[1]) / 2) > 50) {
        int(($_[0] + $_[1] + 1) / 2);
    } else {
        int(($_[0] + $_[1]) / 2);
    }
}
#scp guess.cgi cjth726@login.cse.unsw.edu.au:/import/ravel/1/cjth726/public_html