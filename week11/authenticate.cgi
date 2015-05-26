#!/usr/bin/perl
# Simple CGI script written by andrewt@cse.unsw.edu.au
# Sum two numbers and outputs a form which will rerun the script

use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);

print header, start_html('Sum Two Numbers');
warningsToBrowser(1);

if(!param("Username") && !param("Password")) {
print start_form;
print 'Username: ', textfield('Username');
print p;
print end_form;
}

if (param("Username") && !param("Password")) {
$hidden_username = param("Username");
print start_form;
print hidden('Username');
print 'Password: ', textfield('Password');
print p;
print end_form;
}

if (param("Username") && param("Password")) {
	$username = param("Username");
	$username =~ s/\W//g;
	chomp $username;
	$password = param("Password");
	chomp $password;
	$password_file = "users/$username.password";
	if (!open F, "<$password_file") {
	    print "Unknown username!\n";
	} else {
		$correct_password = <F>;
	    chomp $correct_password;
	    if ($password eq $correct_password) {
	        print "You are authenticated.\n";
	    } else {
	        print "Incorrect password!\n";
	    }
	}
}

print end_html;

#scp authenticate.cgi cjth726@login.cse.unsw.edu.au:/import/ravel/1/cjth726/public_html