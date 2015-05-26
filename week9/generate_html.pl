#!/usr/bin/perl
use warnings;
use strict;
use POSIX qw(strftime);

my @coursecodes;
my @enrollments; 

my $line;
my $course;
my $number;
my $datestring = strftime "%A %d %B %e %H:%M:%S %Z %Y", localtime;

my $courseurl = "http://cgi.cse.unsw.edu.au/~cs2041/14s2/lab/perl/students/course_codes";
my $enrollmentsurl = "http://cgi.cse.unsw.edu.au/~cs2041/14s2/lab/perl/students/enrollments";

my %coursenames;
my %studentnames;
my %studentsenrolled;

my %seencourses;
my %seennames;


#	load course_codes 


open C, "wget -q -O- '$courseurl'|" or die;
@coursecodes = <C>;
chomp(@coursecodes);
close(C);
#	check

foreach $line (@coursecodes) {
	if ($line =~ /(COMP[0-9]{4})/) {
		#print "$1\n";
		#print "$line\n";
		$coursenames{$1} = $line;
	}
}

open F, "wget -q -O- '$enrollmentsurl'|" or die;
@enrollments = <F>;
chomp(@enrollments);
close(F);

#	check and creating keys

foreach $line (@enrollments) {
	#print "# $line\n";
	$line =~ /([^\|]*)\|([^\|]*)\|([^\|]*)\|/;
	if ($seencourses{$1}++ == 0) {
		#print "$1\n";
	}
	if ($seennames{$2}++ == 0) {
		$studentnames{$2} = $3;
	}
	$studentsenrolled{$1}{$2} = $3;
	$studentsenrolled{$2}{$1} = $3;
}

# Open index.html for writing

open(INDEXPAGE ,">index.html") or die;

# Generate links to comp courses of students

my $allcourses = "";
foreach $course (sort keys %seencourses) {
	#print INDEXPAGE "$coursenames{$course}\n";
	$allcourses = "$allcourses<li><a href=\"$course.html\">$coursenames{$course}</a></li>\n";
}

# Generate links to students

my $allstudents = "";
foreach $number (sort { $studentnames{$a} cmp $studentnames{$b} } keys %studentnames) {
	#print INDEXPAGE "$coursenames{$course}\n";
	$allstudents = "$allstudents<li><a href=\"$number.html\">$number $studentnames{$number}</a></li>\n";
}

# Generate Index Page

print INDEXPAGE "<html><head><title>Index Page</title><style type=\"text/css\"></style></head>
<body>
<h2>Index Page</h2>
<h2>All Courses</h2>
<ul>
$allcourses
</ul>
<h2>All Students</h2>
<ul>
$allstudents
</ul>
<hr>
<small>Created on $datestring
 by jasont
 as a COMP2041 lab exercise


</small></body></html>";

close(INDEXPAGE);

foreach $course (sort keys %seencourses) {
	open(COURSEPAGE, ">$course.html")  or die;

	my $coursestudents = "";
	foreach $number (sort { $studentsenrolled{$course}{$a} cmp $studentsenrolled{$course}{$b} } keys $studentsenrolled{$course}) {
		#print INDEXPAGE "$coursenames{$course}\n";
	$coursestudents = "$coursestudents<li><a href=\"$number.html\">$number $studentnames{$number}</a></li>\n";
	}

	print COURSEPAGE "<html><head><title>Students Enrolled in $coursenames{$course}</title><style type=\"text/css\"></style></head>
	<body>
	<h2>Students Enrolled in $coursenames{$course}</h2>
	<ul>
	$coursestudents
	</ul>
	<a href=\"index.html\">Back to Index</a>
	<hr>
	<small>Created on $datestring
	 by jasont
	 as a COMP2041 lab exercise


	</small></body></html>";

	close (COURSEPAGE);
}

foreach $number (keys %studentnames) {
	open(STUDENTPAGE, ">$number.html")  or die;

	my $studentcourses = "";
	foreach $course (sort keys $studentsenrolled{$number}) {
		#print INDEXPAGE "$coursenames{$course}\n";
	$studentcourses = "$studentcourses<li><a href=\"$course.html\">$coursenames{$course}</a></li>\n";
	}

	print STUDENTPAGE "<html><head><title>Courses taken by $studentnames{$number}</title><style type=\"text/css\"></style></head>
	<body>
	<h2>Courses taken by $studentnames{$number}</h2>
	<ul>
	$studentcourses
	</ul>
	<a href=\"index.html\">Back to Index</a>
	<hr>
	<small>Created on $datestring
	 by jasont
	 as a COMP2041 lab exercise


	</small></body></html>";

	close (STUDENTPAGE);
}
