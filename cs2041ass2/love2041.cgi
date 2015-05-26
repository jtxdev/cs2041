#!/usr/bin/perl -w

# written by andrewt@cse.unsw.edu.au September 2013
# as a starting point for COMP2041/9041 assignment 2
# http://cgi.cse.unsw.edu.au/~cs2041/assignments/LOVE2041/

use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use Data::Dumper;  
use List::Util qw/min max/;
use CGI::Cookie;
use CGI::Session;
use File::Copy;

#use strict;

CGI::Session->name("LOVE2041COOKIE");
#$CGI::POST_MAX = 1024 * 5000;

warningsToBrowser(1);

# some globals used through the script
$debug = 1;
$students_dir = "./students";
$studentsperpage = 10;
$url = url(-relative=>1);
$checkurl = url(-relative=>1,-path_info=>1,-query=>1);

$s = CGI::Session->load() or die CGI::Session->errstr();
    
if ( $s->is_expired ) {
    print header(),
        start_html(),
        p("Your session timed out! Please refresh the page."),
        end_html();
    exit 0;
}

$name = $s->param('username');
$loggedin = $s->param('_isLoggedIn');

if ((!$name || !defined($loggedin) || (defined(param('keywords')) && param('keywords') eq "logout"))) {
	print redirect('login.cgi');
} elsif (param('keywords') eq "signup") {
	print redirect('signup.cgi');
} elsif (defined(param('view')) && param('view') eq 'myprofile' 
	&& defined(param("action")) && (param("action") eq "savechanges" 
	||		   param("action") eq "saveprefs"
	||		   param("action") eq "deleteprofilepic"
	||		   param("action") eq "saveprofilepic")) {
		#print page_header();
		#To add:
		#print redirect('love2041.cgi?view=myprofile');

		#page directly handles header
} elsif (defined(param('view')) && param('view') eq 'myacct' 
	&& defined(param("action")) && (param("action") eq "savepass" 
	||		   param("action") eq "saveuser" 
	||         param("action") eq "saveemail" 
	||	 	   param("action") eq "savevisibility")) {
		#print page_header();
		#To add:
		#print redirect('love2041.cgi?view=myacct');

		#page directly handled header
} 
else {
# print start of HTML ASAP to assist debugging if there is an error in the script
# force HTML5
	# my $header = "";
	# my $dtd = '<!DOCTYPE html>';
	# $header .= page_header();
	# $header =~ s/<!DOCTYPE.*?>/$dtd/s;
	# $header =~ s/<html.*?>/<html>/s;
	# print $header;
	print page_header();
}

if (defined param('keywords')) {
	
	if (param('keywords') eq "signup") {
		print page_trailer();
		exit 0;
	} elsif (param('keywords') eq "logout") {
		$s->delete();
		$s->flush(); 
		print page_trailer();
		exit 0;
	} 
} else {

	if (defined(param('view')) && param('view') eq 'search') {
		if (defined(param('search'))) {
			$type = param('type');
			print search_screen($type, param('search'));
		}	
	} elsif (defined(param('view')) && param('view') eq 'browse') {
		print browse_screen();
	} elsif (defined(param('view')) && param('view') eq 'profile') {
		print profile_screen();
	} elsif (defined(param('view')) && param('view') eq 'myprofile') {
		print myprofile_screen();
	} elsif (defined(param('view')) && param('view') eq 'myacct') {
		print myacct_screen();
	} elsif (defined(param('view')) && param('view') eq 'message') {
		print message_screen();
	} else {
		print myprofile_screen();
	}
}

print page_trailer();
exit 0;	



#screens



#generates search screen
sub search_screen {
	my $profilesonthispage = "";
	my $p = param('page') || 1;
	my $searchitem = lc(param('search'));
	#print $searchitem;
	$search_screen = "";
	#$search_screen .= h2('WTF');
	load_allprofiles();
	load_allpref();
	my $gendercheck = 0;
	if ($_[0] eq 'gender') {
		$gendercheck = 1;
	}


	my @students;
	foreach $student (sort(keys %studentprofileinfo)) {
		#print pre("$studentprofileinfo{$student}{$_[0]}\n");
		if (lc($studentprofileinfo{$student}{$_[0]}) =~ /$searchitem/) {
			if ($gendercheck == 1) {
				if (lc($studentprofileinfo{$student}{$_[0]}) =~ /^\|$searchitem$/) {
					push (@students, $student);
				}
			} else {
				push (@students, $student);
			}
		}
		#print $student;
	}


	$n = min(max(($p - 1) * $studentsperpage, 0), $#students);
	$limit = 0;
	#print "$#students";
	if ($#students >= 0) {
		for (0..9) {
			my $student_to_show  = $students[$n];
			my $profile_pic = load_profile_picture($student_to_show);
			
			
			#print "$student_to_show\n";
			if (defined $studentprofileinfo{$student_to_show}{suspended} && $studentprofileinfo{$student_to_show}{suspended} eq "|yes") {
				$profilesonthispage .= show_suspended_profile($student_to_show);
			} else {

				if (defined $studentprofileinfo{$student_to_show}{gender}) {
					if ($studentprofileinfo{$student_to_show}{gender} eq "|male") {
						$profilesonthispage .= show_browse_profile($student_to_show, $profile_pic, $n, 'panel panel-info');
					} elsif ($studentprofileinfo{$student_to_show}{gender} eq "|female") {
						$profilesonthispage .= show_browse_profile($student_to_show, $profile_pic, $n, 'panel panel-danger');
					} else {
						$profilesonthispage .= show_browse_profile($student_to_show, $profile_pic, $n, 'panel panel-primary');
					}
				} else {
					$profilesonthispage .= show_browse_profile($student_to_show, $profile_pic, $n, 'panel panel-primary');
				}
				if ($n < $#students) {
					$n++;
				} else {
					$limit = 1;
					last;
				}
			}
		}
	}

	$search_screen .= divopen('container');
    	$search_screen .= $profilesonthispage;
    $search_screen .= divclose();

    $search_screen .= divopen('text-center');
		$search_screen .= search_paginate($p, max($#students / $studentsperpage, 0));
	$search_screen .= divclose();

	return $search_screen;

}

#generates browse screen
sub browse_screen {
	my $browsehtml = "";
	my $profilesonthispage = "";
	my $p = param('page') || 1;
	my $me = "$students_dir/$name";
	my @studentstmp = glob("$students_dir/*");
	$n = min(max(($p - 1) * $studentsperpage, 0), $#studentstmp);
	$limit = 0;
	my @students;

	load_allprofiles();
	load_allpref();
	load_pref_extra($me);
	foreach $student (@studentstmp) {
		calculatematchmaking($student);
	}

	foreach my $student (sort { $studentscore{$b} <=> $studentscore{$a} } keys %studentscore) {
    	push(@students, $student);
	}
	

	for (0..9) {
		my $student_to_show  = $students[$n];
		# load_profile($student_to_show);
		# load_pref($student_to_show);
		my $profile_pic = load_profile_picture($student_to_show);
		

		if (defined $studentprofileinfo{$student_to_show}{suspended} && $studentprofileinfo{$student_to_show}{suspended} eq "|yes") {
			$profilesonthispage .= show_suspended_profile($student_to_show);
		} else {
			if (defined $studentprofileinfo{$student_to_show}{gender}) {
				if ($studentprofileinfo{$student_to_show}{gender} eq "|male") {
					$profilesonthispage .= show_browse_profile($student_to_show, $profile_pic, $n, 'panel panel-info');
				} elsif ($studentprofileinfo{$student_to_show}{gender} eq "|female") {
					$profilesonthispage .= show_browse_profile($student_to_show, $profile_pic, $n, 'panel panel-danger');
				} else {
					$profilesonthispage .= show_browse_profile($student_to_show, $profile_pic, $n, 'panel panel-primary');
				}
			} else {
				$profilesonthispage .= show_browse_profile($student_to_show, $profile_pic, $n, 'panel panel-primary');
			}
		}
		if ($n < $#students) {
			$n++;
		} else {
			$limit = 1;
			last;
		}
	}

    $browsehtml .= divopen('container');

    $browsehtml .= $profilesonthispage;
    $browsehtml .= divclose();

	$browsehtml .= p;

	$browsehtml .= divopen('text-center');
		$browsehtml .= browse_paginate($p, $#students / 10);
	$browsehtml .= divclose();

	return $browsehtml;
}

#generates profile screen
sub profile_screen {
	my $studentname = param('profile');
	my $profilehtml = "";
	my $student_to_show  = "$students_dir/$studentname";
	load_profile($student_to_show);
	load_pref($student_to_show);
	my $profile = get_profile($student_to_show); 
	my $pref = get_preferences($student_to_show);
	my $username = get_field($student_to_show, 'username');
	my $profile_pic = load_profile_picture($student_to_show);

	$profilehtml .= h2("$studentname\'s Profile");
	$profilehtml .= p;
	$profilehtml .= divopen("profile-container");
    	$profilehtml .= show_profile($profile, $pref, $profile_pic, $student_to_show);
    $pofilehtml .= divclose();
	$profilehtml .= p;

	return $profilehtml;
}

#generates myacct screen
sub myacct_screen {
	my $studentname = $name;
	my $profilehtml = "";
	my $student_to_show  = "$students_dir/$studentname";
	load_profile($student_to_show);
	my $profile = get_myacct($student_to_show); 



	if (defined param("action") && param("action") eq "editpass") {
		$profilehtml .= h2("My Account > Change Password");
		$profilehtml .= p;
		$profilehtml .= show_editmypassword($student_to_show);
	} elsif (defined param("action") && param("action") eq "edituser") {
		$profilehtml .= h2("My Account > Change Username");
		$profilehtml .= p;
		$profilehtml .= show_editmyuser($student_to_show);
	} elsif (defined param("action") && param("action") eq "editemail") {
		$profilehtml .= h2("My Account > Change Email");
		$profilehtml .= p;
		$profilehtml .= show_editmyemail($student_to_show);
	} elsif (defined param("action") && param("action") eq "editvisibility") {
		$profilehtml .= h2("My Account > Change Visiblity");
		$profilehtml .= p;
		$profilehtml .= show_editmysuspension($student_to_show);
	} elsif (defined param("action") && param("action") eq "saveuser") {
		$profilehtml .= show_savemyuser($student_to_show); 
	} elsif (defined param("action") && param("action") eq "savepass") {
		$profilehtml .= show_savemypass($student_to_show); 
	} elsif (defined param("action") && param("action") eq "saveemail") {
		$profilehtml .= show_savemyemail($student_to_show); 
	} elsif (defined param("action") && param("action") eq "savevisibility") {
		$profilehtml .= show_savemysuspension($student_to_show); 
	} else {
		$profilehtml .= h2("My Account");
	    $profilehtml .= $profile;
		$profilehtml .= p;
	}

	return $profilehtml;
}

#generates myprofile screen
sub myprofile_screen {
	my $studentname = $name;
	my $profilehtml = "";
	my $student_to_show  = "$students_dir/$studentname";
	load_profile($student_to_show);
	load_pref($student_to_show);
	my $profile = get_myprofile($student_to_show); 
	my $pref = get_preferences($student_to_show);
	my $profile_pic = load_profile_picture($student_to_show);

	if (defined param("action") && param("action") eq "editprofile") {
		$profilehtml .= h2("My Profile > Change Details");
		$profilehtml .= p;
		$profilehtml .= show_editmyprofile($student_to_show);
	} elsif (defined param("action") && param("action") eq "savechanges") {
		$profilehtml .= show_savemyprofile($student_to_show); 
	} elsif (defined param("action") && param("action") eq "editprefs") {
		$profilehtml .= h2("My Profile > Change Preferences");
		$profilehtml .= p;
		$profilehtml .= show_editmypreferences($student_to_show); 
	} elsif (defined param("action") && param("action") eq "saveprefs") {
		$profilehtml .= show_savemypreferences($student_to_show); 
	} elsif (defined param("action") && param("action") eq "editprofilepic") {
		$profilehtml .= h2("My Profile > Change Display Picture");
		$profilehtml .= p;
		$profilehtml .= show_editmyprofilepic($student_to_show); 
	} elsif (defined param("action") && param("action") eq "saveprofilepic") {
		$profilehtml .= show_savemyproflepic($student_to_show); 
	} elsif (defined param("action") && param("action") eq "deleteprofilepic") {
		$profilehtml .= show_deletemyproflepic($student_to_show); 
	} else {

	$profilehtml .= h2("My Profile");
	$profilehtml .= p;
    $profilehtml .= show_myprofile($profile, $pref, $profile_pic);
	$profilehtml .= p;
	}

	return $profilehtml;
}

sub message_screen {
	my $studentname = param('profile');
	my $messagehtml = "";
	my $student_to_show  = "$students_dir/$studentname";
	load_profile($student_to_show);

	if (defined param("action") && param("action") eq "sendmessage") {
		$messagehtml .= show_sentmessage($student_to_show); 
	} else {
		$messagehtml .= h2("Message $studentname");
		$messagehtml .= p;
		$messagehtml .= p;
		$messagehtml .= p;
		$messagehtml .= p;
		$messagehtml .= p;
		$messagehtml .= show_messagepage($student_to_show);
	}
	return $messagehtml;

}



#paginators



sub browse_paginate {
	$pagelist = "";
	$pagelist .= "<ul class=\"pagination\">";
	$count = 1;
	$next = $_[0] + 1;
	$prev = $_[0] - 1;
	if (int($_[0]) == 1) {
		$pagelist .= "<li class =\"disabled\"><a href=\"$url?view=browse&page=$prev\">&laquo;</a></li>";
	} else {
		$pagelist .= "<li><a href=\"$url?view=browse&page=$prev\">&laquo;</a></li>";
	}
	while ($count <= $_[1] + 1) {
		if ($count == $_[0]) {
			$pagelist .= "<li class=\"active\"><a href=\"$url?view=browse&page=$count\">$count</a></li>";
		} else {
			$pagelist .= "<li><a href=\"$url?view=browse&page=$count\">$count</a></li>";
		}
		$count++;
	}
	if (int($_[0]) == int($_[1] + 1)) {
		$pagelist .= "<li class =\"disabled\"><a href=\"$url?view=browse&page=$next\">&raquo;</a></li>";
	} else {
		$pagelist .= "<li><a href=\"$url?view=browse&page=$next\">&raquo;</a></li>";
	}
	$pagelist .= "</ul>";
	return $pagelist;
}

sub search_paginate {
	$pagelist = "";
	$pagelist .= "<ul class=\"pagination\">";
	$count = 1;
	$searchitem = param('search');
	$type = param('type');
	$next = $_[0] + 1;
	$prev = $_[0] - 1;
	if (int($_[0]) == 1) {
		$pagelist .= "<li class =\"disabled\"><a href=\"$url?view=search&type=$type&search=$searchitem&page=$prev\">&laquo;</a></li>";
	} else {
		$pagelist .= "<li><a href=\"$url?view=search&type=$type&search=$searchitem&page=$prev\">&laquo;</a></li>";
	}
	while ($count <= $_[1] + 1) {
		if ($count == $_[0]) {
			$pagelist .= "<li class=\"active\"><a href=\"$url?view=search&type=$type&search=$searchitem&page=$count\">$count</a></li>";
		} else {
			$pagelist .= "<li><a href=\"$url?view=search&type=$type&search=$searchitem&page=$count\">$count</a></li>";
		}
		$count++;
	}
	if (int($_[0]) == int($_[1] + 1)) {
		$pagelist .= "<li class =\"disabled\"><a href=\"$url?view=search&type=$type&search=$searchitem&page=$next\">&raquo;</a></li>";
	} else {
		#print "$_[0]".$_[1] + 1;
		$pagelist .= "<li><a href=\"$url?view=search&type=$type&search=$searchitem&page=$next\">&raquo;</a></li>";
	}
	$pagelist .= "</ul>";
	return $pagelist;
}

#!Functions for profiles



# Function to load all profiles
sub load_allprofiles {
	my @students = glob("$students_dir/*");
	foreach $student (@students) {
		my $student_to_show  = $student;
		my $profile_filename = "$student_to_show/profile.txt";
		open my $p, "$profile_filename" or die "can not open $profile_filename: $!";
		while (<$p>) {
			chomp($_);
			if (/^(\w*):/) {
				$profile_field = lc($1);
				$profile_field_info = "";
				#$profile .= "$profile_field\n";
			} elsif (/^\t(.*)/) {
				if ($profile_field eq 'birthdate') {
					$profile_field_info = $1;
					if ($profile_field_info =~ /([0-9]{4})\/([0-9]{2})\/([0-9]{2})/) {
						$profile_field_info = "$3/$2/$1";
						#print "$profile_field_info";
					}
					$studentprofileinfo{$student_to_show}{$profile_field} = $profile_field_info;
				} else {
					$profile_field_info = "$profile_field_info|$1";
					$studentprofileinfo{$student_to_show}{$profile_field} = $profile_field_info;
				}
			} 
		}
		close $p;
	}
}

# Function to load a profile
sub load_profile {
	$profile_field = "";
	$profile_field_info = "";
	my $profile_filename = "$_[0]/profile.txt";
	open my $p, "<$profile_filename" or die "can not open $profile_filename: $!";
	while (<$p>) {
		chomp($_);
		if (/^ /) {
			$count++;
		}
		if (/^(\w*):/) {
			$profile_field = lc($1);
			$profile_field_info = "";
			#$profile .= "$profile_field\n";
		} elsif (/^\t(.*)/) {
			if ($profile_field eq 'birthdate') {
				$profile_field_info = $1;
				if ($profile_field_info =~ /([0-9]{4})\/([0-9]{2})\/([0-9]{2})/) {
					$profile_field_info = "$3/$2/$1";
					#print "$profile_field_info";
				}
				$studentprofileinfo{$_[0]}{$profile_field} = $profile_field_info;
			} else {
				$profile_field_info = "$profile_field_info|$1";
				$studentprofileinfo{$_[0]}{$profile_field} = $profile_field_info;
			}
		} 
	}
	#$profile .= "profile.txt $count\n";
	close $p;
}

# Function to get profile pic path
sub load_profile_picture {
	my $profileimage_filename = "";
	if (-e "$_[0]/photo00.jpg") {
		$profileimage_filename = "$_[0]/photo00.jpg";
	} else {
		$profileimage_filename = "https://crowdscribed-prod.s3.amazonaws.com/assets/avatar/large/profile-pic-placeholder-0b43676ab39af4651fca971eaff73edb.jpg";
	}
	return $profileimage_filename;
}

# Function to generate profile 
sub get_profile {

	load_profile($_[0]);
	my $profile = "";
	my $username = get_field($_[0], 'username');
	$username =~ s/^\|//;
	my $gender: = get_field($_[0], 'gender');
	$gender =~ s/^\|//;
	my $birthdate: = get_field($_[0], 'birthdate');
	$birthdate =~ s/^\|//;
	my $hair_colour: = get_field($_[0], 'hair_colour');
	$hair_colour =~ s/^\|//;
	my $height = get_field($_[0], 'height');
	$height =~ s/^\|//;
	my $weight = get_field($_[0], 'weight');
	$weight =~ s/^\|//;
	my $degree = get_field($_[0], 'degree');
	$degree =~ s/^\|//;
	my $courses = get_field($_[0], 'courses');
	$courses =~ s/^\|//;
	$courses =~ s/\|/\n\t /g;
	my $favourite_books = get_field($_[0], 'favourite_books');
	$favourite_books =~ s/^\|//;
	$favourite_books =~ s/\|/\n\t /g;
	my $favourite_hobbies = get_field($_[0], 'favourite_hobbies');
	$favourite_hobbies =~ s/^\|//;
	$favourite_hobbies =~ s/\|/\n\t /g;
	my $favourite_movies = get_field($_[0], 'favourite_movies');
	$favourite_movies =~ s/^\|//;
	$favourite_movies =~ s/\|/\n\t /g;
	my $favourite_bands = get_field($_[0], 'favourite_bands');
	$favourite_bands =~ s/^\|//;
	$favourite_bands =~ s/\|/\n\t /g;
	my $favourite_TV_shows: = get_field($_[0], 'favourite_tv_shows');
	$favourite_TV_shows =~ s/^\|//;
	$favourite_TV_shows =~ s/\|/\n\t /g;
	my $description = get_field($_[0], 'description');
	$description =~ s/^\|//;
	$description =~ s/\|/\n\t /g;


	my $profile = "";
	$profile .= "Username: $username<br>";
	$profile .= "Gender: $gender<br>";
	$profile .= "Birthdate: $birthdate<br>";
	$profile .= "Hair Colour: $hair_colour<br>";
	$profile .= "Height: $height<br>";
	$profile .= "Weight: $weight<br>";
	$profile .= "Degree: $degree<br>";
	$profile .= "Courses: $courses<br>";
	$profile .= "Favourite Books: $favourite_books<br>";
	$profile .= "Favourite Hobbies: $favourite_hobbies<br>";
	$profile .= "Favourite Movies: $favourite_movies<br>";
	$profile .= "Favourite Bands: $favourite_bands<br>";
	$profile .= "Favourite TV shows: $favourite_TV_shows<br>";
	$profile .= "About me: $description<br>";
	return $profile;
}

# Function to generate MYprofile 
sub get_myprofile {

	load_profile($_[0]);
	my $profile = "";
	my $username = get_field($_[0], 'username');
	$username =~ s/^\|//;
	my $realname = get_field($_[0], 'name');
	$realname =~ s/^\|//;
	my $password = get_field($_[0], 'password');
	$password =~ s/^\|//;
	my $email = get_field($_[0], 'email');
	$email =~ s/^\|//;
	my $gender = get_field($_[0], 'gender');
	$gender =~ s/^\|//;
	my $birthdate = get_field($_[0], 'birthdate');
	$birthdate =~ s/^\|//;
	my $hair_colour: = get_field($_[0], 'hair_colour');
	$hair_colour =~ s/^\|//;
	my $height = get_field($_[0], 'height');
	$height =~ s/^\|//;
	my $weight = get_field($_[0], 'weight');
	$weight =~ s/^\|//;
	my $degree = get_field($_[0], 'degree');
	$degree =~ s/^\|//;
	my $courses = get_field($_[0], 'courses');
	$courses =~ s/^\|//;
	$courses =~ s/\|/\n\t /g;
	my $favourite_books = get_field($_[0], 'favourite_books');
	$favourite_books =~ s/^\|//;
	$favourite_books =~ s/\|/\n\t /g;
	my $favourite_hobbies = get_field($_[0], 'favourite_hobbies');
	$favourite_hobbies =~ s/^\|//;
	$favourite_hobbies =~ s/\|/\n\t /g;
	my $favourite_movies = get_field($_[0], 'favourite_movies');
	$favourite_movies =~ s/^\|//;
	$favourite_movies =~ s/\|/\n\t /g;
	my $favourite_bands = get_field($_[0], 'favourite_bands');
	$favourite_bands =~ s/^\|//;
	$favourite_bands =~ s/\|/\n\t /g;
	my $favourite_TV_shows: = get_field($_[0], 'favourite_tv_shows');
	$favourite_TV_shows =~ s/^\|//;
	$favourite_TV_shows =~ s/\|/\n\t /g;
	my $description = get_field($_[0], 'description');
	$description =~ s/^\|//;
	$description =~ s/\|/\n\t /g;


	my $profile = "";
	$profile .= "Username: $username<br>";
	$profile .= "Name: $realname<br>";
	#$profile .= "Password: $password<br>";
	$profile .= "Email: $email<br>";
	$profile .= "Gender: $gender<br>";
	$profile .= "Birthdate: $birthdate<br>";
	$profile .= "Hair Colour: $hair_colour<br>";
	$profile .= "Height: $height<br>";
	$profile .= "Weight: $weight<br>";
	$profile .= "Degree: $degree<br>";
	$profile .= "Courses: $courses<br>";
	$profile .= "Favourite Books: $favourite_books<br>";
	$profile .= "Favourite Hobbies: $favourite_hobbies<br>";
	$profile .= "Favourite Movies: $favourite_movies<br>";
	$profile .= "Favourite Bands: $favourite_bands<br>";
	$profile .= "Favourite TV shows: $favourite_TV_shows<br>";
	$profile .= "About me: $description<br>";
	return $profile;
}

# Function to generate browse profile
sub get_browseprofile {

	load_profile($_[0]);
	my $profile = "";
	my $username = get_field($_[0], 'username');
	$username =~ s/^\|//;
	my $gender = get_field($_[0], 'gender');
	$gender =~ s/^\|//;
	my $birthdate: = get_field($_[0], 'birthdate');
	$birthdate =~ s/^\|//;
	my $hair_colour: = get_field($_[0], 'hair_colour');
	$hair_colour =~ s/^\|//;
	my $height = get_field($_[0], 'height');
	$height =~ s/^\|//;
	my $weight = get_field($_[0], 'weight');
	$weight =~ s/^\|//;
	my $degree = get_field($_[0], 'degree');
	$degree =~ s/^\|//;
	my $description = get_field($_[0], 'description');
	$description =~ s/^\|//;
	$description =~ s/\|/\n\t /g;


	my $profile = "";
	$profile .= "Username: $username<br>";
	$profile .= "Gender: $gender<br>";
	$profile .= "Birthdate: $birthdate<br>";
	$profile .= "Hair Colour: $hair_colour<br>";
	$profile .= "Height: $height<br>";
	$profile .= "Weight: $weight<br>";
	$profile .= "Degree: $degree<br>";
	$profile .= "About me: $description<br>";
	return $profile;
}

sub get_myacct{
	load_profile($_[0]);
	my $profile = "";
	my $username = get_field($_[0], 'username');
	$username =~ s/^\|//;
	my $password = get_field($_[0], 'password');
	$password =~ s/^\|//;
	my $email = get_field($_[0], 'email');
	$email =~ s/^\|//;
	my $suspended = get_field($_[0], 'suspended');
	$suspended =~ s/^\|//;
	if ($suspended eq "") {
		$suspended = "Public";
	} else {
		$suspended = "Hidden";
	}

	return $profile .= BSmyacct($username, $password, $email, $suspended);
}

# Functions to get profile data
sub get_field {
	if (defined $studentprofileinfo{$_[0]}{$_[1]}) {
		return $studentprofileinfo{$_[0]}{$_[1]}
	} else {
		return "";
	}
}


#!functions for preferences



# Functions to load all preferences
sub load_allpref {

	my @students = glob("$students_dir/*");
	foreach $student (@students) {

		my $student_to_show  = $student;
		my $pref_filename = "$student_to_show/preferences.txt";
		my $pref_field = "";
		my $pref_field_info = "";
		open my $p, "$pref_filename" or die "can not open $pref_filename: $!";
		while (<$p>) {
			chomp($_);
			if (/^(\w*):/) {
				$pref_field = lc($1);
				$pref_field_info = "";
				#$profile .= "$profile_field\n";
			} elsif (/^\t([^\t]+)/) {
				$pref_field_info = "$pref_field_info|$1";
				$studentprefinfo{$student_to_show}{$pref_field} = $pref_field_info;

			} elsif (/^\t\t(.*)/) {
				$pref_field_info = "$pref_field_info$1";
				$studentprefinfo{$student_to_show}{$pref_field} = $pref_field_info;
			}
		}
		close $p;
	}
}

# Function to load preferences
sub load_pref {
	my $student_to_show  = $_[0];
	my $pref_filename = "$student_to_show/preferences.txt";
	my $pref_field = "";
	my $pref_field_info = "";
	open my $p, "$pref_filename" or die "can not open $pref_filename: $!";
	while (<$p>) {
		chomp($_);
		if (/^(\w*):/) {
			$pref_field = lc($1);
			$pref_field_info = "";
			#$profile .= "$profile_field\n";
		} elsif (/^\t([^\t]+)/) {
			$pref_field_info = "$pref_field_info|$1";
			$studentprefinfo{$student_to_show}{$pref_field} = $pref_field_info;

		} elsif (/^\t\t(.*)/) {
			$pref_field_info = "$pref_field_info$1";
			$studentprefinfo{$student_to_show}{$pref_field} = $pref_field_info;
		}
	}
	close $p;
}

# Function to generate preferences
sub get_preferences {

	my $gender = get_pref_field($_[0], 'gender');
	$gender =~ s/^\|//;
	my $age = get_pref_field($_[0], 'age');
	$age =~ s/^\|//;
	my $hair_colours = get_pref_field($_[0], 'hair_colours');
	$hair_colours =~ s/^\|//;
	my $height = get_pref_field($_[0], 'height');
	$height =~ s/^\|//;
	my $weight = get_pref_field($_[0], 'weight');
	$weight =~ s/^\|//;
	my $degree = get_pref_field($_[0], 'degree');
	$degree =~ s/^\|//;
	my $courses = get_pref_field($_[0], 'courses');
	$courses =~ s/^\|//;

	my $profile = "";
	$profile .= "Gender: $gender<br>";
	$profile .= "Age: $age<br>";
	$profile .= "Hair Colours: $hair_colours<br>";
	$profile .= "Height: $height<br>";
	$profile .= "Weight: $weight<br>";
	$profile .= "Degree: $degree<br>";
	$profile .= "Courses: $courses<br>";
	return $profile;
}

# Functions to get preference data
sub get_pref_field {
	if (defined $studentprefinfo{$_[0]}{$_[1]}) {
		return $studentprefinfo{$_[0]}{$_[1]}
	} else {
		return "";
	}
}

sub load_pref_minage {
	my $age = get_pref_field($_[0], 'age');
	my $minage = "";
	
	if ($age =~ /min:([0-9]+)/) {
		$minage = $1;
	}
	$studentprefinfo{$_[0]}{'minage'} = $minage;
}

sub load_pref_maxage{
	my $age = get_pref_field($_[0], 'age');
	my $maxage = "";
	
	if ($age =~ /max:([0-9]+)/) {
		$maxage = $1;
	}
	$studentprefinfo{$_[0]}{'maxage'} = $maxage;
}


sub load_pref_minweight {
	my $weight = get_pref_field($_[0], 'weight');
	my $minweight = "";
	
	if ($weight =~ /min:([0-9]+)/) {
		$minweight = $1;
	}
	$studentprefinfo{$_[0]}{'minweight'} = $minweight;
}

sub load_pref_maxweight{
	my $weight = get_pref_field($_[0], 'weight');
	my $maxweight = "";
	
	if ($weight =~ /max:([0-9]+)/) {
		$maxweight = $1;
	}
	$studentprefinfo{$_[0]}{'maxweight'} = $maxweight;
}

sub load_pref_minheight {
	my $height = get_pref_field($_[0], 'height');
	my $minheight = "";
	
	if ($height =~ /min:([0-9\.]+)/) {
		$minheight = $1;
	}
	$studentprefinfo{$_[0]}{'minheight'} = $minheight;
}

sub load_pref_maxheight{
	my $height = get_pref_field($_[0], 'height');
	my $maxheight = "";
	
	if ($height =~ /max:([0-9\.]+)/) {
		$maxheight = $1;
	}
	$studentprefinfo{$_[0]}{'maxheight'} = $maxheight;
}

sub load_pref_extra {
	load_pref_minheight($_[0]);
	load_pref_minweight($_[0]);
	load_pref_minage($_[0]);
	load_pref_maxheight($_[0]);
	load_pref_maxweight($_[0]);
	load_pref_maxage($_[0]);
}

sub get_age {
	my $birthdate = get_field($_[0], 'birthdate');
	$birthdate =~ s/^\|//;
	my $age = "";
	if ($birthdate =~ /[0-9]{2}\/[0-9]{2}\/([0-9]{4})/) {
		$yearofbirth = $1;
		$age = 2014 - $yearofbirth;		
	} else {
		$age = "";
	}
	return $age;
}

sub get_weight {
	my $weight = get_field($_[0], 'weight');
	$weight =~ s/^\|//;
	$weight =~ s/[^0-9.]*//g;
	return $weight;
}

sub get_height {
	my $height = get_field($_[0], 'height');
	$height =~ s/^\|//;
	$height =~ s/[^0-9.]*//g;
	return $height;
}

#Matching Algorithm

sub calculatematchmaking {

load_pref_extra($_[0]);
my $me = "$students_dir/$name";
my $score = 0;

	print "<!-- Gender is the most important +10000 if match -->" if $debug;

	if (get_pref_field($me, 'gender') ne "") {
		if (get_pref_field($me, 'gender') eq get_field($_[0], 'gender')) {
			$score += 10000;
			print "<!-- $_[0] match gender \+ 10000 \| score is $score -->" if $debug;
		}
	}
	if (get_pref_field($_[0], 'gender') ne "") {
		if (get_pref_field($_[0], 'gender') eq get_field($me, 'gender')) {
			$score += 10000;
			print "<!-- $_[0] reciprocate match gender \+ 10000 \| score is $score -->" if $debug;
		}
	}

	#next calculate age score

	print "<!-- Age is next \| Max score 1000  \| agescore = 1000 - mismatch -->" if $debug;

	my $myage = get_age($me);
	my $urage = get_age($_[0]);

	my $mymaxage = $studentprefinfo{$me}{'maxage'};
	my $myminage = $studentprefinfo{$me}{'minage'};
	my $urmaxage = $studentprefinfo{$_[0]}{'maxage'};
	my $urminage = $studentprefinfo{$_[0]}{'minage'};

	my $agescore = 0;
			#me first

	my $mytargetage = 0;
	my $urtargetweight = 0;

	if ($mymaxage ne "" && $myminage ne "") {
		$mytargetage = ($myminage + $mymaxage) / 2;
		print "<!-- age preference set target age $mytargetage -->" if $debug;
	} else {
		$mytargetage = $myage;
		print "<!-- age preference not set target age is your age -->" if $debug;
	}

	if ($myage ne "" && $urage ne "") {
		$agescore = 1000 - abs($urage - $mytargetage); 
		$score += $agescore;
		print "<!-- age score + $agescore \| score is $score -->" if $debug;
	}

	#then you

	if ($urmaxage ne "" && $urminage ne "") {
		$urtargetage = ($urminage + $urmaxage) / 2;
		print "<!-- age preference set target age $urtargetage -->" if $debug;
	} else {
		$urtargetage = $urage;
		print "<!-- age preference not set target age is their age -->" if $debug;
	}

	if ($myage ne "" && $urage ne "") {
		$agescore = 1000 - abs($myage - $urtargetage); 
		$score += $agescore;
		print "<!-- age reciprocate score + $agescore \| score is $score -->" if $debug;
	}

	print "<!-- Weight is next \| Max score 1000  \| weightscore = 1000 - mismatch * 10-->" if $debug;


    my $myweight = get_weight($me, 'weight');
	my $urweight = get_weight($_[0], 'weight');


	my $mymaxweight = $studentprefinfo{$me}{'maxweight'};
    my $myminweight = $studentprefinfo{$me}{'minweight'};
    my $urmaxweight = $studentprefinfo{$_[0]}{'maxweight'};
    my $urminweight = $studentprefinfo{$_[0]}{'minweight'};

    my $weightscore = 0;

    my $mytargetage = 0;
	my $urtargetweight = 0;

	if ($mymaxweight ne "" && $myminweight ne "") {
		$mytargetweight = ($myminweight + $mymaxweight) / 2;
		print "<!-- weight preference set target weight $mytargetweight -->" if $debug;
	} else {
		$mytargetweight = $myweight;
		print "<!-- weight preference not set target weight is your weight -->" if $debug;
	}

	if ($myweight ne "" && $urweight ne "") {
		$weightscore = 1000 - (abs($urweight - $mytargetweight) * 10); 
		$score += $weightscore;
		print "<!-- weight score + $weightscore \| score is $score -->" if $debug;
	}

	if ($urmaxweight ne "" && $urminweight ne "") {
		$urtargetweight = ($urminweight + $urmaxweight) / 2;
		print "<!-- weight preference set target weight $urtargetweight -->" if $debug;
	} else {
		$urtargetweight = $urweight;
		print "<!-- weight preference not set target weight is their weight -->" if $debug;
	}


	if ($myweight ne "" && $urweight ne "") {
		$weightscore = 1000 - (abs($myweight - $urtargetweight) * 10); 
		$score += $weightscore;
		print "<!-- weight score + $weightscore \| score is $score -->" if $debug;
	}

	print "<!-- Height is next \| Max score 500  \| heightscore = 500 - mismatch * 100 -->" if $debug;


    my $myheight = get_height($me, 'height');
	my $urheight = get_height($_[0], 'height');


	my $mymaxheight = $studentprefinfo{$me}{'maxheight'};
    my $myminheight = $studentprefinfo{$me}{'minheight'};
    my $urmaxheight = $studentprefinfo{$_[0]}{'maxheight'};
    my $urminheight = $studentprefinfo{$_[0]}{'minheight'};

    my $heightscore = 0;

    my $mytargetage = 0;
	my $urtargetheight = 0;

	if ($mymaxheight ne "" && $myminheight ne "") {
		$mytargetheight = ($myminheight + $mymaxheight) / 2;
		print "<!-- height preference set target height $mytargetheight -->" if $debug;
	} else {
		$mytargetheight = $myheight;
		print "<!-- height preference not set target height is your height -->" if $debug;
	}

	if ($myheight ne "" && $urheight ne "") {
		$heightscore = 500 - (abs($urheight - $mytargetheight) * 100); 
		$score += $heightscore;
		print "<!-- height score + $heightscore \| score is $score -->" if $debug;
	}

	if ($urmaxheight ne "" && $urminheight ne "") {
		$urtargetheight = ($urminheight + $urmaxheight) / 2;
		print "<!-- height preference set target height $urtargetheight -->" if $debug;
	} else {
		$urtargetheight = $urheight;
		print "<!-- height preference not set target height is their height -->" if $debug;
	}


	if ($myheight ne "" && $urheight ne "") {
		$heightscore = 500 - (abs($myheight - $urtargetheight) * 100); 
		$score += $heightscore;
		print "<!-- height score + $heightscore \| score is $score -->" if $debug;
	}
	
print "<!-- Bonus 100 if hair colour exact match (otherwise 0 cause you don't care enough) \| Max score 100  \| hairscore = +100 * ?haircolour -->" if $debug;

	if (get_pref_field($me, 'hair_colours') ne "") {
		if (get_pref_field($me, 'hair_colours') eq get_field($_[0], 'hair_colour')) {
			$score += 100;
			print "<!-- $_[0] match hair exact \+ 100 \| score is $score -->" if $debug;
		}
	}
	if (get_pref_field($_[0], 'hair_colours') ne "") {
		if (get_pref_field($_[0], 'hair_colours') eq get_field($me, 'hair_colour')) {
			$score += 100;
			print "<!-- $_[0] reciprocate match hair exact \+ 100 \| score is $score -->" if $debug;
		}
	}

		# print "$me";
	print "<!-- final score for $_[0] is $score -->" if $debug;
	$studentscore{"$_[0]"} = $score;

}


#!Showing Profiles


# Function to generate the profile text html
sub show_profile {
	my $profile = "";
	my $username = get_field($_[3], 'username');
	$username =~ s/^\|//;
	my $suspended = get_field($_[3], 'suspended');
	$suspended =~ s/^\|//;
	$profile .= divopen('col-md-3');

	if ($suspended eq "yes") {
		$profileimage_filename = "https://crowdscribed-prod.s3.amazonaws.com/assets/avatar/large/profile-pic-placeholder-0b43676ab39af4651fca971eaff73edb.jpg";
		$profile .= BSImage($profileimage_filename, 'img-responsive center-block profilepic', 'auto', 'auto');
	} else {
		$profile .= BSImage($_[2], 'img-responsive center-block profilepic', 'auto', 'auto');
	}

	$profile .= start_form(-method=>'get');

	param('view', 'message');
	$profile .= hidden('view', 'message');
	$profile .= hidden('profile', "$username");	
	$profile .= BSbutton('submit', 'btn', 'Message Me');
	$profile .= end_form;


	$profile .= divclose();
	$profile .= divopen('col-md-6');
	$profile .= h3('My Info');
	if ($suspended eq "yes") {
		$profile .= pre('This Account has been suspended');
	} else {
		$profile .= pre($_[0]);
	}
	$profile .= h3("I'm looking for");
	if ($suspended eq "yes") {
		$profile .= pre('This Account has been suspended');
	} else {
		$profile .= pre($_[1]);
	}
	$profile .= divclose();
	return $profile;
}

# Function to generate the myprofile text html
sub show_myprofile {
	my $profile = "";
	my $username = get_field($_[0], 'username');
	$username =~ s/\|//;
	$profile .= divopen('col-md-3');

	$profile .= BSImage($_[2], 'img-responsive center-block profilepic', 'auto', 'auto');
	
	$profile .= start_form(-method=>'get');

	param('view', 'myprofile');
	$profile .= hidden('view', 'myprofile');
	param('action', "editprofilepic");
	$profile .= hidden('action', "editprofilepic");
	$profile .= BSbutton('submit', 'btn', 'Change DP');
	$profile .= end_form;


	$profile .= divclose();
	$profile .= divopen('col-md-6');
	$profile .= h3('My Info');

	$profile .= start_form(-method=>'get');
		
	param('view', 'myprofile');
	$profile .= hidden('view', 'myprofile');
	param('action', "editprofile");
	$profile .= hidden('action', "editprofile");
	$profile .= BSbutton('submit', 'btn', 'Edit Profile');
	$profile .= end_form;
	$profile .= pre($_[0]);

	$profile .= h3("My Preferences");
	$profile .= start_form(-method=>'get');
		
	param('view', 'myprofile');
	$profile .= hidden('view', 'myprofile');
	param('action', "editprefs");
	$profile .= hidden('action', "editprefs");
	$profile .= BSbutton('submit', 'btn', 'Edit Preferences');
	$profile .= end_form;
	$profile .= pre($_[1]);
	$profile .= divclose();

	$profile .= "<br>";
	$profile .= "<br>";
	$profile .= "<br>";

	return $profile;
}

#To add: check birthdate
sub show_savemypreferences {
	my $prefs = makepreferences();

	my $check = 0;
	my $feedback = "";

	if ($check > 0) {
		#$feedback .= page_header();
		#$feedback .= h2("PADDING");
		#$feedback .= pre($prefs);
		$feedback .= redirect("love2041.cgi?view=myprofile&action=editprefs&error=$check");
	} else {

		open pref, ">$_[0]/preferences.txt" or die "can not open $_[0]/preferences.txt: $!";
		print pref $prefs;
		close pref;

		$feedback .= page_header();
		$feedback .= h2("Your preferences has been successfully updated");
		$feedback .= BSSuccess("Your preferences has been successfully updated");
	}
	return $feedback;

}

sub show_editmypreferences {
	load_pref($_[0]);

	my $pref = "";
	my $gender = get_pref_field($_[0], 'gender');
	my $age = get_pref_field($_[0], 'age');
	my $height = get_pref_field($_[0], 'height');
	my $weight = get_pref_field($_[0], 'weight');
	my $hair_colours = get_pref_field($_[0], 'hair_colours');
	my $degree = get_pref_field($_[0], 'degree');
	my $courses = get_pref_field($_[0], 'courses');


	my $minage = "";
	my $maxage = "";
	if ($age =~ /min:([0-9]+)/) {
		$minage = $1;
	}
	if ($age =~ /max:([0-9]+)/) {
		$maxage = $1;
	}

	my $minheight = "";
	my $maxheight = "";
	if ($height =~ /min:([0-9.]+)/) {
		$minheight = $1;
	}
	if ($height =~ /max:([0-9.]+)/) {
		$maxheight = $1;
	}

	my $minweight = "";
	my $maxweight = "";
	if ($weight =~ /min:([0-9]+)/) {
		$minweight = $1;
	}
	if ($weight =~ /max:([0-9]+)/) {
		$maxweight = $1;
	}

	$gender =~ s/^\|//;
	$age =~ s/^\|//;
	$hair_colours =~ s/^\|//;
	$height =~ s/^\|//;
	$weight =~ s/^\|//;
	$degree =~ s/^\|//;
	$courses =~ s/^\|//;

	param('gender', $gender);
	param('minage', $minage);
	param('maxage', $maxage);
	param('hair_colours', $hair_colours);
	param('minheight', $minheight);
	param('maxheight', $maxheight);
	param('minweight', $minweight);
	param('maxweight', $maxweight);
	param('degree', $degree);
	param('courses', $courses);

	param('action', 'saveprefs');


	
	$profile .= "<div class=\"container\">";
	$profile .= "<div class=\"col-md-9\" role=\"main\">";
	$profile .= "<form role=\"form\" id=\"preferenceForm\" method=\"post\" class=\"form-horizontal\">".
	 "<div class=\"form-group\">
	   <label for=\"'gender'\" class=\"col-sm-2 control-label\">Gender</label>
	    <div class=\"col-sm-5\">".
	    BSradiofield('gender', 'male', 'Male').
		BSradiofield('gender', 'female', 'Female').
		BSradiofield('gender', 'other', 'Other').
		BSradiofieldchecked('gender', '', 'Hide').
	  "</div>
	</div>".
	BSformtextfield('hair_colours', $hair_colours, 'Hair colour').
	BSformtextfield('minage', $minage, 'Minimum Age').
	BSformtextfield('maxage', $maxage, 'Maximum Age').
  "<div class=\"form-group\">
   <label for=\"minweight\" class=\"col-sm-2 control-label\">Minimum weight</label>
    <div class=\"col-sm-5\">
     <div class=\"input-group\">
   	 <input type=\"text\" class=\"form-control\" name=\"minweight\" id=\"minweight\" value=\"$minweight\">
      <div class=\"input-group-addon\">kg</div>
     </div>
   	</div>
  </div>".
  "<div class=\"form-group\">
   <label for=\"maxweight\" class=\"col-sm-2 control-label\">Maximum weight</label>
    <div class=\"col-sm-5\">
     <div class=\"input-group\">
   	 <input type=\"text\" class=\"form-control\" name=\"maxweight\" id=\"maxweight\" value=\"$maxweight\">
      <div class=\"input-group-addon\">kg</div>
     </div>
   	</div>
  </div>".
  "<div class=\"form-group\">
   <label for=\"minheight\" class=\"col-sm-2 control-label\">Minimum Height</label>
    <div class=\"col-sm-5\">
     <div class=\"input-group\">
   	 <input type=\"text\" class=\"form-control\" name=\"minheight\" id=\"minheight\" value=\"$minheight\">
      <div class=\"input-group-addon\">m</div>
     </div>
   	</div>
  </div>".
  "<div class=\"form-group\">
   <label for=\"maxheight\" class=\"col-sm-2 control-label\">Maximum Height</label>
    <div class=\"col-sm-5\">
     <div class=\"input-group\">
   	 <input type=\"text\" class=\"form-control\" name=\"maxheight\" id=\"maxheight\" value=\"$maxheight\">
      <div class=\"input-group-addon\">m</div>
     </div>
   	</div>
  </div>".
	BSformtextfield('degree', $degree, 'Degree').
	BSformtextfield('courses', $courses, 'Courses').
	"<div class=\"col-sm-10 col-sm-offset-2\">".
	hidden('view', 'myprofile').
	hidden('action', 'saveprefs').
	BSbutton('submit', 'btn btn-default', 'Submit').
	"</div>".
	"</form>".
	"</div>".
	"</div>";

	return $profile;
}

# Function to save changes to myprofile

sub show_savemyprofile {
	my $profile = makeprofile();

	my $check = 0;
	my $feedback = "";

	my $birthdate = param('birthdate') || "";
	if ($birthdate !~ /^([0-9]{2})\/([0-9]{2})\/([0-9]{4})$/) {
		$check = 1;
	} else {
		$birthdate =~ /^([0-9]{2})\/([0-9]{2})\/([0-9]{4})$/;
		if ($1 < 1 || $1 > 31) {
			$check = 1;
		} elsif ($2 < 0 || $2 > 12) {
			$check = 1;
		}
	}

	if ($check > 0) {
		#$feedback .= page_header();
		#$feedback .= pre($profile);
		$feedback .= redirect("love2041.cgi?view=myprofile&action=editprofile&error=$check");
	} else {

		open profile, ">$_[0]/profile.txt" or die "can not open $_[0]/profile.txt: $!";
		print profile $profile;
		close profile;

		$feedback .= page_header();
		#$feedback .= h2("Your profile has been successfully updated");
		$feedback .= BSSuccess("Your profile has been successfully updated");

	}
	return $feedback;
}

# Function to show the editmyprofile text html
#To add: Sanitising
sub show_editmyprofile {
		load_profile($_[0]);
		my $profile = "";
		my $username = get_field($_[0], 'username');
		$username =~ s/^\|//;
		my $realname: = get_field($_[0], 'name');
		$realname =~ s/^\|//;
		my $password: = get_field($_[0], 'password');
		$password =~ s/^\|//;
		my $email: = get_field($_[0], 'email');
		$email =~ s/^\|//;
		my $gender: = get_field($_[0], 'gender');
		$gender =~ s/^\|//;
		my $birthdate: = get_field($_[0], 'birthdate');
		$birthdate =~ s/^\|//;
		my $hair_colour: = get_field($_[0], 'hair_colour');
		$hair_colour =~ s/^\|//;
		my $height = get_field($_[0], 'height');
		$height =~ s/^\|//;
		$height =~ s/[^0-9\.]//g;
		my $weight = get_field($_[0], 'weight');
		$weight =~ s/^\|//;
		$weight =~ s/[^0-9]//g;
		my $degree = get_field($_[0], 'degree');
		$degree =~ s/^\|//;
		my $courses = get_field($_[0], 'courses');
		$courses =~ s/^\|//;
		my $favourite_books = get_field($_[0], 'favourite_books');
		$favourite_books =~ s/^\|//;
		my $favourite_hobbies = get_field($_[0], 'favourite_hobbies');
		$favourite_hobbies =~ s/^\|//;
		my $favourite_movies = get_field($_[0], 'favourite_movies');
		$favourite_movies =~ s/^\|//;
		my $favourite_bands = get_field($_[0], 'favourite_bands');
		$favourite_bands =~ s/^\|//;
		my $favourite_TV_shows: = get_field($_[0], 'favourite_tv_shows');
		$favourite_TV_shows =~ s/^\|//;
		my $description = get_field($_[0], 'description');
		$description =~ s/^\|//;

		param('action', 'savechanges');
		param('username', $username);
		param('password', $password);
  		param('email', $email);

  		if (defined param('error') && param('error') eq '1') {
			$profile .= BSAlert('The birthdate you entered is not valid');
		}

		$profile .= "<div class=\"container\">";
		$profile .= "<div class=\"col-md-9\" role=\"main\">";
		$profile .= "<form role=\"form\" id=\"registrationForm\" method=\"post\" class=\"form-horizontal\">".
		"Please separate your inputs with a pipe (|) character if you are entering multiple responses. Eg. Hot Fuzz|Superbad|etc<br><br><br>".
		BSformtextfield('realname', $realname, 'Real name').
  		hidden('username').
  		hidden('password').
  		hidden('email').
  		"<div class=\"form-group\">
  		 <label for=\"birthdate\" class=\"col-sm-2 control-label\">Birthdate</label>
		  <div class=\"col-sm-5\">
		   	 <input type=\"text\" class=\"form-control\" name=\"birthdate\" id=\"birthdate\" value=\"$birthdate\" placeholder=\"DD/MM/YYYY\">
	      </div>
		 </div>".
  		"<div class=\"form-group\">
		 <label for=\"'gender'\" class=\"col-sm-2 control-label\">Gender</label>
		 <div class=\"col-sm-5\">".
		    BSradiofield('gender', 'male', 'Male').
			BSradiofield('gender', 'female', 'Female').
			BSradiofield('gender', 'other', 'Other').
			BSradiofieldchecked('gender', '', 'Hide').
		 "</div>
		</div>".
		BSformtextfield('hair_colour', $hair_colour, 'Hair colour').
		"<div class=\"form-group\">
		 <label for=\"height\" class=\"col-sm-2 control-label\">Height</label>
		  <div class=\"col-sm-5\">
		   <div class=\"input-group\">
			 <input type=\"text\" class=\"form-control\" name=\"height\" id=\"height\" value=\"$height\">
		   <div class=\"input-group-addon\">m</div>
		  </div>
		 </div>
		</div>".
	    "<div class=\"form-group\">
		 <label for=\"weight\" class=\"col-sm-2 control-label\">Weight</label>
	   	  <div class=\"col-sm-5\">
		   <div class=\"input-group\">
			 <input type=\"text\" class=\"form-control\" name=\"weight\" id=\"weight\" value=\"$weight\">
		   <div class=\"input-group-addon\">kg</div>
		  </div>
		 </div>
		</div>".
		BSformtextfield('degree', $degree, 'Degree').
		BSformtextfield('courses', $courses, 'Courses').
		BSformtextfield('favourite_books', $favourite_books, 'Favourite Books').
		BSformtextfield('favourite_hobbies', $favourite_hobbies, 'Favourite Hobbies').
		BSformtextfield('favourite_movies', $favourite_movies, 'Favourite Movies').
		BSformtextfield('favourite_bands', $favourite_bands, 'Favourite Bands').
		BSformtextfield('favourite_tv_shows', $favourite_TV_shows, 'Favourite TV shows').
		BSformtextfield('description', $description, 'Description').
		"<div class=\"col-sm-10 col-sm-offset-2\">".
		hidden('view', 'myprofile').
		hidden('action', 'savechanges').
		BSbutton('submit', 'btn btn-default', 'Submit').
		"</div>".
		"</form>".
		"</div>".
		"</div>";

		return $profile;
}

# Function to show the editmyprofile text html
#To add: Sanitising

sub show_savemypass {
	my $check = 0;
	my $feedback = "";
	my $profile = makeprofile();

	my $correctpassword: = get_field($_[0], 'password');
		$correctpassword =~ s/^\|//;

	my $oldpassword = param('oldpassword') || "";
	my $password = param('password') || "";
	my $password2 = param('password2') || "";


	if ($oldpassword ne $correctpassword) {
		$check += 1;
	}
	if (length($password) < 6 || length($password) > 30) {
		$check += 2;
	}
	if ($password ne $password2) {
		$check += 4;
	}

	if ($check > 0) {
		$feedback .= redirect("love2041.cgi?view=myacct&action=editpass&error=$check");
	} else {

		open profile, ">$_[0]/profile.txt" or die "can not open $_[0]/profile.txt: $!";
		print profile $profile;
		close profile;

		$feedback .= page_header();
		#$feedback .= h2("Your password has successfully been changed");
		$feedback .= BSSuccess("Your password has successfully been changed");

	}
	return $feedback;
}

sub show_editmypassword{

	load_profile($_[0]);
		my $changepass = "";
		my $username = get_field($_[0], 'username');
		$username =~ s/^\|//;
		my $realname: = get_field($_[0], 'name');
		$realname =~ s/^\|//;
		my $password: = get_field($_[0], 'password');
		$password =~ s/^\|//;
		my $email: = get_field($_[0], 'email');
		$email =~ s/^\|//;
		my $gender: = get_field($_[0], 'gender');
		$gender =~ s/^\|//;
		my $birthdate: = get_field($_[0], 'birthdate');
		$birthdate =~ s/^\|//;
		my $hair_colour: = get_field($_[0], 'hair_colour');
		$hair_colour =~ s/^\|//;
		my $height = get_field($_[0], 'height');
		$height =~ s/^\|//;
		my $weight = get_field($_[0], 'weight');
		$weight =~ s/^\|//;
		my $degree = get_field($_[0], 'degree');
		$degree =~ s/^\|//;
		my $courses = get_field($_[0], 'courses');
		$courses =~ s/^\|//;
		my $favourite_books = get_field($_[0], 'favourite_books');
		$favourite_books =~ s/^\|//;
		my $favourite_hobbies = get_field($_[0], 'favourite_hobbies');
		$favourite_hobbies =~ s/^\|//;
		my $favourite_movies = get_field($_[0], 'favourite_movies');
		$favourite_movies =~ s/^\|//;
		my $favourite_bands = get_field($_[0], 'favourite_bands');
		$favourite_bands =~ s/^\|//;
		my $favourite_TV_shows: = get_field($_[0], 'favourite_tv_shows');
		$favourite_TV_shows =~ s/^\|//;
		my $description = get_field($_[0], 'description');
		$description =~ s/^\|//;

		#load params
		param('realname', $realname);
		param('username', $username);
		#param('password', $password);
		param('email', $email);
		param('gender', $gender);
		param('birthdate', $birthdate);
		param('hair_colour', $hair_colour);
		param('height', $height);
		param('weight', $weight);
		param('degree', $degree);
		param('courses', $courses);
		param('favourite_books', $favourite_books);
		param('favourite_hobbies', $favourite_hobbies);
		param('favourite_movies', $favourite_movies);
		param('favourite_bands', $favourite_bands);
		param('favourite_tv_shows', $favourite_TV_shows);
		param('description', $description);

		param('action', 'savepass');
		if (defined param('error') && param('error') eq '1') {
			$changepass .= BSAlert('The old password you entered is not correct');
		}
		if (defined param('error') && param('error') eq '2') {
			$changepass .= BSAlert('That password is not between 6-30 characters long');
		}
		if (defined param('error') && param('error') eq '3') {
			$changepass .= BSAlert('The password you entered is not correct');
			$changepass .= BSAlert('That password is not between 6-30 characters long');
		}
		if (defined param('error') && param('error') eq '4') {
			$changepass .= BSAlert('The new passwords don\'t match');
		}
		if (defined param('error') && param('error') eq '5') {
			$changepass .= BSAlert('The old password you entered is not correct');
			$changepass .= BSAlert('The new passwords don\'t match');
		}
		if (defined param('error') && param('error') eq '6') {
			$changepass .= BSAlert('That password is not between 6-30 characters long');
			$changepass .= BSAlert('The new passwords don\'t match');
		}
		if (defined param('error') && param('error') eq '7') {
			$changepass .= BSAlert('The old password you entered is not correct');
			$changepass .= BSAlert('That password is not between 6-30 characters long');
			$changepass .= BSAlert('The new passwords don\'t match');
		}
	    $changepass .= "<div class=\"container\">";
		$changepass .= "<div class=\"col-md-9\" role=\"main\">";
		$changepass .= "<form role=\"form\" id=\"passwordchangeForm\" method=\"post\" class=\"form-horizontal\">".
				#hideparams
		hidden('realname', $realname).
		hidden('username', $username).
		#hidden('password', $password).
		hidden('email', $email).
		hidden('gender', $gender).
		hidden('birthdate', $birthdate).
		hidden('hair_colour', $hair_colour).
		hidden('height', $height).
		hidden('weight', $weight).
		hidden('degree', $degree).
		hidden('courses', $courses).
		hidden('favourite_books', $favourite_books).
		hidden('favourite_hobbies', $favourite_hobbies).
		hidden('favourite_movies', $favourite_movies).
		hidden('favourite_bands', $favourite_bands).
		hidden('favourite_tv_shows', $favourite_TV_shows).
		hidden('description', $description).
		BSformpasswordfield('oldpassword', "", 'Enter Old Password').
		BSformpasswordfield('password', "", 'Enter New Password').
		BSformpasswordfield('password2', "", 'Confirm New Password').
		"<div class=\"col-sm-10 col-sm-offset-2\">".
		hidden('view', 'myacct').
		hidden('action', 'savepass').
		BSbutton('submit', 'btn btn-default', 'Submit').
		"</div>".
		"</form>".
		"</div>".
		"</div>";
	return $changepass;
}

sub show_savemyuser {
	my $check = 0;
	my $feedback = "";
	my $profile = makeprofile();
	my $username = param('username') || "";	
	my $oldusername = get_field($_[0], 'username');
		$oldusername =~ s/^\|//;
	my @students = glob("$students_dir/*");
	$_=lc for @students;
	my $olddirectory  = "$students_dir/$oldusername";
	my $newdirectory = "$students_dir/$username";
	my $userdirectory = lc("$students_dir/$username");

	my $correctpassword: = get_field($_[0], 'password');
		$correctpassword =~ s/^\|//;

	my $password = param('password') || "";

	if ($password ne $correctpassword) {
		$check += 1;
	}
	if (length($username) < 6 || length($username) > 30) {
		$check += 2;
	}
	if ( grep( /^$userdirectory$/, @students ) ) {
		$check += 4;
	} 

	if ($check > 0) {
		$feedback .= redirect("love2041.cgi?view=myacct&action=edituser&error=$check");
	} else {

		open profile, ">$_[0]/profile.txt" or die "can not open $_[0]/profile.txt: $!";
		print profile $profile;
		close profile;

		move("$olddirectory", "$newdirectory");

		$feedback .= page_header();
		#$feedback .= "$olddirectory | $newdirectory<br>";
		$feedback .= h2("Your username has been successfully changed");
		$feedback .= BSSuccess("You are required to log in again");
		$s->delete();
		$s->flush(); 
	}
	return $feedback;
}

sub show_editmyuser{

		load_profile($_[0]);
		my $changeuser = "";
		my $username = get_field($_[0], 'username');
		$username =~ s/^\|//;
		my $realname: = get_field($_[0], 'name');
		$realname =~ s/^\|//;
		my $password: = get_field($_[0], 'password');
		$password =~ s/^\|//;
		my $email: = get_field($_[0], 'email');
		$email =~ s/^\|//;
		my $gender: = get_field($_[0], 'gender');
		$gender =~ s/^\|//;
		my $birthdate: = get_field($_[0], 'birthdate');
		$birthdate =~ s/^\|//;
		my $hair_colour: = get_field($_[0], 'hair_colour');
		$hair_colour =~ s/^\|//;
		my $height = get_field($_[0], 'height');
		$height =~ s/^\|//;
		my $weight = get_field($_[0], 'weight');
		$weight =~ s/^\|//;
		my $degree = get_field($_[0], 'degree');
		$degree =~ s/^\|//;
		my $courses = get_field($_[0], 'courses');
		$courses =~ s/^\|//;
		my $favourite_books = get_field($_[0], 'favourite_books');
		$favourite_books =~ s/^\|//;
		my $favourite_hobbies = get_field($_[0], 'favourite_hobbies');
		$favourite_hobbies =~ s/^\|//;
		my $favourite_movies = get_field($_[0], 'favourite_movies');
		$favourite_movies =~ s/^\|//;
		my $favourite_bands = get_field($_[0], 'favourite_bands');
		$favourite_bands =~ s/^\|//;
		my $favourite_TV_shows: = get_field($_[0], 'favourite_tv_shows');
		$favourite_TV_shows =~ s/^\|//;
		my $description = get_field($_[0], 'description');
		$description =~ s/^\|//;

		param('realname', $realname);
		#param('username', $username);
		#param('password', $password);
		param('email', $email);
		param('gender', $gender);
		param('birthdate', $birthdate);
		param('hair_colour', $hair_colour);
		param('height', $height);
		param('weight', $weight);
		param('degree', $degree);
		param('courses', $courses);
		param('favourite_books', $favourite_books);
		param('favourite_hobbies', $favourite_hobbies);
		param('favourite_movies', $favourite_movies);
		param('favourite_bands', $favourite_bands);
		param('favourite_tv_shows', $favourite_TV_shows);
		param('description', $description);

		param('action', 'saveuser');

		if (defined param('error') && param('error') eq '1') {
			$changeuser .= BSAlert('The password you entered is not correct');
		}
		if (defined param('error') && param('error') eq '2') {
			$changeuser .= BSAlert('That username is not between 6-30 characters long');
		}
		if (defined param('error') && param('error') eq '3') {
			$changeuser .= BSAlert('The password you entered is not correct');
			$changeuser .= BSAlert('That username is not between 6-30 characters long');
		}
		if (defined param('error') && param('error') eq '4') {
			$changeuser .= BSAlert('That username is already taken');
		}
		if (defined param('error') && param('error') eq '5') {
			$changeuser .= BSAlert('The password you entered is not correct');
			$changeuser .= BSAlert('That username is already taken');
		}
		if (defined param('error') && param('error') eq '6') {
			$changeuser .= BSAlert('That username is not between 6-30 characters long');
			$changeuser .= BSAlert('That username is already taken');
		}
		if (defined param('error') && param('error') eq '7') {
			$changeuser .= BSAlert('The password you entered is not correct');
			$changeuser .= BSAlert('That username is not between 6-30 characters long');
			$changeuser .= BSAlert('That username is already taken');
		}
	    $changeuser .= "<div class=\"container\">";
		$changeuser .= "<div class=\"col-md-9\" role=\"main\">";
		$changeuser .= "<form role=\"form\" id=\"usernamechangeForm\" method=\"post\" class=\"form-horizontal\">".
		hidden('realname', $realname).
		#hidden('username', $username).
		#hidden('password', $password).
		hidden('email', $email).
		hidden('gender', $gender).
		hidden('birthdate', $birthdate).
		hidden('hair_colour', $hair_colour).
		hidden('height', $height).
		hidden('weight', $weight).
		hidden('degree', $degree).
		hidden('courses', $courses).
		hidden('favourite_books', $favourite_books).
		hidden('favourite_hobbies', $favourite_hobbies).
		hidden('favourite_movies', $favourite_movies).
		hidden('favourite_bands', $favourite_bands).
		hidden('favourite_tv_shows', $favourite_TV_shows).
		hidden('description', $description).
		BSformpasswordfield('password', "", 'Enter Password').
		BSformtextfield('username', $username, 'Enter New Username').
		"<div class=\"col-sm-10 col-sm-offset-2\">".
		hidden('view', 'myacct').
		hidden('action', 'saveuser').
		BSbutton('submit', 'btn btn-default', 'Submit').
		"</div>".
		"</form>".
		"</div>".
		"</div>";
	return $changeuser;
}

sub show_savemyemail {
	my $check = 0;
	my $feedback = "";
	my $profile = makeprofile();
	my $emailaddr = param("email") || "";

	my $correctpassword: = get_field($_[0], 'password');
		$correctpassword =~ s/^\|//;

	my $password = param('password') || "";

	if ($password ne $correctpassword) {
		$check += 1;
	}
	if ($emailaddr !~ /[^@]*\@[^@]*/) {
		$check += 2;
	}


	if ($check > 0) {
		$feedback .= redirect("love2041.cgi?view=myacct&action=editemail&error=$check");
	} else {

		open profile, ">$_[0]/profile.txt" or die "can not open $_[0]/profile.txt: $!";
		print profile $profile;
		close profile;

		$feedback .= page_header();
		$feedback .= h2("You have successfuly changed your email");
	}
	return $feedback;
}

sub show_editmyemail{

		load_profile($_[0]);
		my $changeuser = "";
		my $username = get_field($_[0], 'username');
		$username =~ s/^\|//;
		my $realname: = get_field($_[0], 'name');
		$realname =~ s/^\|//;
		my $password: = get_field($_[0], 'password');
		$password =~ s/^\|//;
		my $email: = get_field($_[0], 'email');
		$email =~ s/^\|//;
		my $gender: = get_field($_[0], 'gender');
		$gender =~ s/^\|//;
		my $birthdate: = get_field($_[0], 'birthdate');
		$birthdate =~ s/^\|//;
		my $hair_colour: = get_field($_[0], 'hair_colour');
		$hair_colour =~ s/^\|//;
		my $height = get_field($_[0], 'height');
		$height =~ s/^\|//;
		my $weight = get_field($_[0], 'weight');
		$weight =~ s/^\|//;
		my $degree = get_field($_[0], 'degree');
		$degree =~ s/^\|//;
		my $courses = get_field($_[0], 'courses');
		$courses =~ s/^\|//;
		my $favourite_books = get_field($_[0], 'favourite_books');
		$favourite_books =~ s/^\|//;
		my $favourite_hobbies = get_field($_[0], 'favourite_hobbies');
		$favourite_hobbies =~ s/^\|//;
		my $favourite_movies = get_field($_[0], 'favourite_movies');
		$favourite_movies =~ s/^\|//;
		my $favourite_bands = get_field($_[0], 'favourite_bands');
		$favourite_bands =~ s/^\|//;
		my $favourite_TV_shows: = get_field($_[0], 'favourite_tv_shows');
		$favourite_TV_shows =~ s/^\|//;
		my $description = get_field($_[0], 'description');
		$description =~ s/^\|//;

		param('realname', $realname);
		param('username', $username);
		#param('password', $password);
		#param('email', $email);
		param('gender', $gender);
		param('birthdate', $birthdate);
		param('hair_colour', $hair_colour);
		param('height', $height);
		param('weight', $weight);
		param('degree', $degree);
		param('courses', $courses);
		param('favourite_books', $favourite_books);
		param('favourite_hobbies', $favourite_hobbies);
		param('favourite_movies', $favourite_movies);
		param('favourite_bands', $favourite_bands);
		param('favourite_tv_shows', $favourite_TV_shows);
		param('description', $description);

		param('action', 'saveemail');

		if (defined param('error') && param('error') eq '1') {
			$changeemail .= BSAlert('The password you entered is not correct');
		}
		if (defined param('error') && param('error') eq '2') {
			$changeemail .= BSAlert('That email is not valid');
		}
		if (defined param('error') && param('error') eq '3') {
			$changeemail .= BSAlert('The password you entered is not correct');
			$changeemail .= BSAlert('That email is not valid');
		}

	    $changeemail .= "<div class=\"container\">";
		$changeemail .= "<div class=\"col-md-9\" role=\"main\">";
		$changeemail .= "<form role=\"form\" id=\"emailchangeForm\" method=\"post\" class=\"form-horizontal\">".
				#hideparams
		hidden('realname', $realname).
		hidden('username', $username).
		hidden('password', $password).
		#hidden('email', $email).
		hidden('gender', $gender).
		hidden('birthdate', $birthdate).
		hidden('hair_colour', $hair_colour).
		hidden('height', $height).
		hidden('weight', $weight).
		hidden('degree', $degree).
		hidden('courses', $courses).
		hidden('favourite_books', $favourite_books).
		hidden('favourite_hobbies', $favourite_hobbies).
		hidden('favourite_movies', $favourite_movies).
		hidden('favourite_bands', $favourite_bands).
		hidden('favourite_tv_shows', $favourite_TV_shows).
		hidden('description', $description).
		BSformpasswordfield('password', "", 'Enter Password').
		BSformtextfield('email', $email, 'Email').
		"<div class=\"col-sm-10 col-sm-offset-2\">".
		hidden('view', 'myacct').
		hidden('action', 'saveemail').
		BSbutton('submit', 'btn btn-default', 'Submit').
		"</div>".
		"</form>".
		"</div>".
		"</div>";
	return $changeemail;
}


sub show_savemyproflepic {
	my $check = 0;
	my $feedback = "";
	my $filename = param('filename');
    my $data = join("", <$filename>);
    my $ok = 0;

    if ($filename =~ /\.jpg$/) {
    	$ok = 1;
    }

	if ( !$filename )
	{
		$feedback .= redirect("love2041.cgi?view=myprofile&action=editprofilepic&error=0");
	} elsif ($ok == 0) {
		$feedback .= redirect("love2041.cgi?view=myprofile&action=editprofilepic&error=1");
	} else {
		if (-e "$_[0]/photo00.jpg") {
			unlink("$_[0]/photo00.jpg");
		}

		open (UPLOADFILE, ">$_[0]/photo00.jpg") or die "$!";
		binmode UPLOADFILE;

		print UPLOADFILE $data;

		close UPLOADFILE;
	}
	$feedback .= page_header();
	#$feedback .= "$filename, $data";
	$feedback .= BSSuccess("Your photo has been successfully changed");
	return $feedback;
}

sub show_deletemyproflepic {
	if (-e "$_[0]/photo00.jpg") {
		unlink("$_[0]/photo00.jpg");
	}
	$feedback .= page_header();
	#$feedback .= "$filename, $data";
	$feedback .= BSSuccess("Your photo has been successfully deleted");
	return $feedback;
}

sub show_editmyprofilepic {
	my $text = "";
	param('view', 'myprofile');
	param('action', 'saveprofilepic');

  	if (defined param('error') && param('error') eq '0') {
		$text .= BSAlert('The file is too big');
	}
	if (defined param('error') && param('error') eq '1') {
		$text .= BSAlert('That file is not a jpg');
	}

	$text .= "<div class=\"container\">.
	<div class=\"col-md-9\" role=\"main\">".
	start_form.
	BSPhotoInput('filename').
	hidden('view', 'myprofile').
	hidden('action', 'saveprofilepic').
	BSbutton('submit', 'btn btn-default', 'Change Photo').
	end_form;
	param('action', 'deleteprofilepic');
	$text .= start_form.
	hidden('view', 'myprofile').
	hidden('action', 'deleteprofilepic').
	BSbutton('submit', 'btn btn-default', 'Delete Photo').
	"</div>
	</div>";
	return $text;
}

sub BSPhotoInput {
  "<div class=\"form-group\">
    <label for=\"exampleInputFile\">Upload a new display picture</label>
    <input type=\"file\" name=\"$_[0]\" id=\"exampleInputFile\">
    <p class=\"help-block\">Upload a new photo (.jpg)</p>
  </div>"
}

sub show_sentmessage {
	my $check = 0;
	my $feedback = "";
	load_profile($_[0]);
	my $username = get_field($_[0], 'username');
	$username =~ s/^\|//;
	my $message = param('message') || "";
	my $emailaddr = get_field($_[0], 'email');
	$emailaddr =~ s/^\|//;

	sendpersonalmessage($name, $emailaddr, $message);

	$feedback .= BSSuccess("Your message has been sent to $username\'s email");
	return $feedback;
}

sub show_messagepage {
	$messagehtml = ""; 
	
	$username = get_field($_0, 'username');
	param('view', 'message');
	param('action', 'sendmessage');
	$messagehtml .= 

	   "<div class=\"container\">".
		"<div class=\"col-md-9\" role=\"main\">".
		"<form role=\"form\" id=\"emailchangeForm\" method=\"post\">".
		hidden('view', 'message').
		hidden('action', 'sendmessage').
		hidden('profile', "$username").
		BStextarea('message', "", 'Message').
		"<div class=\"col-sm-10 col-sm-offset-2\">".
		BSbutton('submit', 'btn', 'Send').
		"</div>".
		"</form>".
		"</div>".
		"</div>";
	
	return $messagehtml;
}

sub show_deletemyaccount {

}

sub show_savemysuspension {
	my $check = 0;
	my $feedback = "";
	my $profile = makeprofile();

	my $correctpassword: = get_field($_[0], 'password');
		$correctpassword =~ s/^\|//;

	my $password = param('password') || "";

	if ($password ne $correctpassword) {
		$check += 1;
	}

	if ($check > 0) {
		$feedback .= redirect("love2041.cgi?view=myacct&action=editvisibility&error=$check");
	} else {

		open profile, ">$_[0]/profile.txt" or die "can not open $_[0]/profile.txt: $!";
		print profile $profile;
		close profile;

		$feedback .= page_header();
		#$feedback .= "$olddirectory | $newdirectory<br>";
		#$feedback .= h2("Your username has been successfully changed");
		$feedback .= BSSuccess("Your visibility settings have been updated");
	}
	return $feedback;
}

sub show_editmysuspension{

		load_profile($_[0]);
		my $changeuser = "";
		my $username = get_field($_[0], 'username');
		$username =~ s/^\|//;
		my $realname: = get_field($_[0], 'name');
		$realname =~ s/^\|//;
		my $password: = get_field($_[0], 'password');
		$password =~ s/^\|//;
		my $email: = get_field($_[0], 'email');
		$email =~ s/^\|//;
		my $gender: = get_field($_[0], 'gender');
		$gender =~ s/^\|//;
		my $birthdate: = get_field($_[0], 'birthdate');
		$birthdate =~ s/^\|//;
		my $hair_colour: = get_field($_[0], 'hair_colour');
		$hair_colour =~ s/^\|//;
		my $height = get_field($_[0], 'height');
		$height =~ s/^\|//;
		my $weight = get_field($_[0], 'weight');
		$weight =~ s/^\|//;
		my $degree = get_field($_[0], 'degree');
		$degree =~ s/^\|//;
		my $courses = get_field($_[0], 'courses');
		$courses =~ s/^\|//;
		my $favourite_books = get_field($_[0], 'favourite_books');
		$favourite_books =~ s/^\|//;
		my $favourite_hobbies = get_field($_[0], 'favourite_hobbies');
		$favourite_hobbies =~ s/^\|//;
		my $favourite_movies = get_field($_[0], 'favourite_movies');
		$favourite_movies =~ s/^\|//;
		my $favourite_bands = get_field($_[0], 'favourite_bands');
		$favourite_bands =~ s/^\|//;
		my $favourite_TV_shows: = get_field($_[0], 'favourite_tv_shows');
		$favourite_TV_shows =~ s/^\|//;
		my $description = get_field($_[0], 'description');
		$description =~ s/^\|//;

		param('realname', $realname);
		param('username', $username);
		#param('password', $password);
		param('email', $email);
		param('gender', $gender);
		param('birthdate', $birthdate);
		param('hair_colour', $hair_colour);
		param('height', $height);
		param('weight', $weight);
		param('degree', $degree);
		param('courses', $courses);
		param('favourite_books', $favourite_books);
		param('favourite_hobbies', $favourite_hobbies);
		param('favourite_movies', $favourite_movies);
		param('favourite_bands', $favourite_bands);
		param('favourite_tv_shows', $favourite_TV_shows);
		param('description', $description);

		param('action', 'savevisibility');

	    $changeuser .= "<div class=\"container\">";
		$changeuser .= "<div class=\"col-md-9\" role=\"main\">";
		$changeuser .= "<form role=\"form\" id=\"visibilitychangeForm\" method=\"post\" class=\"form-horizontal\">".
		hidden('realname', $realname).
		hidden('username', $username).
		#hidden('password', $password).
		hidden('email', $email).
		hidden('gender', $gender).
		hidden('birthdate', $birthdate).
		hidden('hair_colour', $hair_colour).
		hidden('height', $height).
		hidden('weight', $weight).
		hidden('degree', $degree).
		hidden('courses', $courses).
		hidden('favourite_books', $favourite_books).
		hidden('favourite_hobbies', $favourite_hobbies).
		hidden('favourite_movies', $favourite_movies).
		hidden('favourite_bands', $favourite_bands).
		hidden('favourite_tv_shows', $favourite_TV_shows).
		hidden('description', $description).
		BSformpasswordfield('password', "", 'Enter Password').
		"<form role=\"form\" id=\"preferenceForm\" method=\"post\" class=\"form-horizontal\">".
		  "<div class=\"form-group\">
	   <label for=\"'gender'\" class=\"col-sm-2 control-label\">Show Profile</label>
	    <div class=\"col-sm-5\">".
		BSradiofieldchecked('suspension', '', 'Yes').
		BSradiofield('suspension', 'yes', 'No').
	  "</div>
	</div>".
		"<div class=\"col-sm-10 col-sm-offset-2\">".
		hidden('view', 'myacct').
		hidden('action', 'savevisibility').
		BSbutton('submit', 'btn btn-default', 'Submit').
		"</div>".
		"</form>".
		"</div>".
		"</div>";
	return $changeuser;
}

sub BSmyacct { 
	my $deleteurl = url()."/deleteacct.cgi";
	$deleteurl =~ s/love2041.cgi\///;
	$deletelink = "<a href=\"$deleteurl\">Here</a>";

	return
"<form method=\"GET\" action=\"$url?\" class=\"form-horizontal\" role=\"form\">
  <div class=\"form-group\">
    <label class=\"col-sm-2 control-label\">Username</label>
    <div class=\"col-sm-3\">
     <div class=\"input-group\">
      <input type=\"hidden\" name=\"view\" value =\"myacct\">
      <input type=\"hidden\" name=\"action\" value =\"edituser\">
      <p class=\"form-control-static\">$_[0]</p>
      <span class=\"input-group-btn\">
     	<button type=\"submit\" class=\"btn btn-default\" type=\"button\">Edit</button>
      </span>
    </div>
   </div>
  </div>
 </form>
 <form method=\"GET\" action=\"$url?\" class=\"form-horizontal\" role=\"form\">
  <div class=\"form-group\"> 
    <label class=\"col-sm-2 control-label\">Password</label>
    <div class=\"col-sm-3\">
     <div class=\"input-group\">
      <input type=\"hidden\" name=\"view\" value =\"myacct\">
      <input type=\"hidden\" name=\"action\" value =\"editpass\">
      <p class=\"form-control-static\">$_[1]</p>
      <span class=\"input-group-btn\">
     	<button type=\"submit\" class=\"btn btn-default\" type=\"button\">Edit</button>
      </span>
    </div>
   </div>
  </div>
 </form>
 <form method=\"GET\" action=\"$url?\" class=\"form-horizontal\" role=\"form\">
  <div class=\"form-group\">
    <label class=\"col-sm-2 control-label\">Email</label>
    <div class=\"col-sm-3\">
    <div class=\"input-group\">
      <input type=\"hidden\" name=\"view\" value =\"myacct\">
      <input type=\"hidden\" name=\"action\" value =\"editemail\">
      <p class=\"form-control-static\">$_[2]</p>
      <span class=\"input-group-btn\">
     	<button type=\"submit\" class=\"btn btn-default\" type=\"button\">Edit</button>
      </span>
    </div>
   </div>
  </div>
 </form>
 <form method=\"GET\" action=\"$url?\" class=\"form-horizontal\" role=\"form\">
  <div class=\"form-group\">
    <label class=\"col-sm-2 control-label\">Visibility</label>
    <div class=\"col-sm-3\">
     <div class=\"input-group\">
      <p class=\"form-control-static\">$_[3]</p>
      <input type=\"hidden\" name=\"view\" value =\"myacct\">
      <input type=\"hidden\" name=\"action\" value =\"editvisibility\">
      <span class=\"input-group-btn\">
     	<button type=\"submit\" class=\"btn btn-default\" type=\"button\">Edit</button>
      </span>
    </div>
   </div>
  </div>
 </form>
 Want to delete your account? Click $deletelink";
}

# Function to generate the browse_profile text
sub show_browse_profile {
		my $profile = "";
		$profile .= divopen('col-md-12 browseprofile');
			$profile .= divopen("$_[3]");
				$profile .= divopen('panel-heading');
					my $username = get_field($_[0], username);
					$username =~ s/\|//;
					$profile .= $username;
				$profile .= divclose();
				
					$profile .= divopen('col-md-2');	

						$profile .= BSImage($_[1], 'img-responsive center-block profilepic', 'auto', 'auto');
						
						$profile .= start_form(-method=>'get');
			
						param('view', 'profile');
						$profile .= hidden('view', 'profile');
						$profile .= hidden('profile', "$username");

						
						$profile .= BSbutton('submit', 'btn', 'View Profile');
						$profile .= end_form;

					$profile .= divclose();		
					$profile .= divopen('col-md-10');
						$profile .= pre(get_browseprofile($_[0]));
						$profile .= pre(get_preferences($_[0]));
					$profile .= divclose();
			
			$profile .= divclose();
		$profile .= divclose();
		return $profile;
}

sub show_suspended_profile {
		my $profile = "";
		my $username = get_field($_[0], username);
					$username =~ s/\|//;
		$profile .= divopen('col-md-12 browseprofile');
			$profile .= divopen("panel panel-warning");
				$profile .= divopen('panel-heading');
					$profile .= "$username";
				$profile .= divclose();
				$profileimage_filename = "https://crowdscribed-prod.s3.amazonaws.com/assets/avatar/large/profile-pic-placeholder-0b43676ab39af4651fca971eaff73edb.jpg";
					$profile .= divopen('col-md-2');	
						$profile .= BSImage($profileimage_filename, 'img-responsive center-block profilepic', 'auto', 'auto');
						
						$profile .= start_form(-method=>'get');
			
						param('view', 'profile');
						$profile .= hidden('view', 'profile');
						$profile .= hidden('profile', "$username");

						
						$profile .= BSbutton('submit', 'btn', 'View Profile');
						$profile .= end_form;

					$profile .= divclose();		
					$profile .= divopen('col-md-10');
						$profile .= pre('This Profile has been suspended');
						$profile .= pre('This Profile has been suspended');
					$profile .= divclose();
			
			$profile .= divclose();
		$profile .= divclose();
		return $profile;
}

sub makeprofile {
	my $realname = param('realname') || "";
	my $username = param('username') || "";
	my $password = param('password') || "";
	my $email = param('email') || "";
	my $gender = param('gender') || "";
	my $birthdate = param('birthdate') || "";
	my $hair_colour = param('hair_colour') || "";
	my $height = param('height') || "";
	$height =~ s/[^0-9\.]//g;
	my $weight = param('weight') || "";
    $weight =~ s/[^0-9\.]//g;
	my $degree = param('degree') || "";
	my $courses = param('courses') || "";
	   	$courses =~ s/\|/\n\t/g;
	my $favourite_books = param('favourite_books') || "";
		$favourite_books =~ s/\|/\n\t/g;
	my $favourite_hobbies = param('favourite_hobbies') || "";
		$favourite_hobbies =~ s/\|/\n\t/g;
	my $favourite_movies = param('favourite_movies') || "";
		$favourite_movies =~ s/\|/\n\t/g;
	my $favourite_bands = param('favourite_bands') || "";
		$favourite_bands =~ s/\|/\n\t/g;
	my $favourite_TV_shows = param('favourite_tv_shows') || "";
		$favourite_TV_shows =~ s/\|/\n\t/g;
	my $description = param('description') || "";
	my $suspended = param('suspension') || "";

	#$birthdate =~ /[0-9]{2}\/[0-9]{2}\/[0-9]{/;

	my $profile = "";
	$profile .= "username:\n\t$username\n";
	$profile .= "name:\n\t$realname\n";
	$profile .= "password:\n\t$password\n";
	$profile .= "email:\n\t$email\n";
	$profile .= "gender:\n\t$gender\n";
	$profile .= "birthdate:\n\t$birthdate\n";
	$profile .= "hair_colour:\n\t$hair_colour\n";
	$profile .= "height:\n\t$height\m\n";
	$profile .= "weight:\n\t$weight\kg\n";
	$profile .= "degree:\n\t$degree\n";
	$profile .= "courses:\n\t$courses\n";
	$profile .= "favourite_books:\n\t$favourite_books\n";
	$profile .= "favourite_hobbies:\n\t$favourite_hobbies\n";
	$profile .= "favourite_movies:\n\t$favourite_movies\n";
	$profile .= "favourite_bands:\n\t$favourite_bands\n";
	$profile .= "favourite_TV_shows:\n\t$favourite_TV_shows\n";
	$profile .= "description:\n\t$description\n";
	$profile .= "suspended:\n\t$suspended\n";

	return $profile;
}


sub makepreferences {

	$gender = param('gender') || "";
	$minage = param('minage') || "";
	$maxage = param('maxage') || "";
	$minweight = param('minweight') || "";
	 $minweight =~ s/[^0-9\.]//g;
	$maxweight = param('maxweight') || "";
	 $maxweight =~ s/[^0-9\.]//g;
	$minheight = param('minheight') || "";
	 $minheight =~ s/[^0-9\.]//g;
	$maxheight = param('maxheight') || "";
	 $maxheight =~ s/[^0-9\.]//g;
	$hair_colours = param('hair_colours') || "";
	$hair_colours =~ s/\|/\n\t/g;
	$degree = param('degree') || "";
	$degree =~ s/\|/\n\t/g;
	$courses = param('courses') || "";
	$courses =~ s/\|/\n\t/g;

	my $pref = "";

	$pref .= "gender:\n\t$gender\n";
	$pref .= "age:\n\tmin:\n\t\t$minage\n\tmax:\n\t\t$maxage\n";
	$pref .= "weight:\n\tmin:\n\t\t$minweight\kg\n\tmax:\n\t\t$maxweight\kg\n";
	$pref .= "height:\n\tmin:\n\t\t$minheight\m\n\tmax:\n\t\t$maxheight\m\n";
	$pref .= "hair_colours:\n\t$hair_colours\n";
	$pref .= "degree:\n\t$degree\n";
	$pref .= "courses:\n\t$courses\n";

	return $pref;
}

sub sendpersonalmessage {

	my $replylink = url()."?view=message&profile=$name";

    my $from    = 'love2041messenger@love2041.com';
    my $to      = "$_[1]";
    my $subject = "$_[0] has messaged you on Love2041!";
  	my $message = "The user $_[0] has sent you a message!\n\n$_[0] says:\n\n\n$_[2]\n\n\nTo reply to this message click here: $replylink";
	
	open(MAIL, "|/usr/sbin/sendmail -t");

	# Email Header
	print MAIL "To: $to\n";
	print MAIL "From: $from\n";
	print MAIL "Subject: $subject\n\n";
	# Email Body
	print MAIL $message;

	close MAIL;
}

#!Bootstrap Code Functions

sub BSImage {
	return "<img src=\"$_[0]\" class=\"$_[1]\" width=\"$_[2]\" height=\"$_[3]\">";
}

sub BSbutton {
	return "<button type=\"$_[0]\" class=\"$_[1]\">$_[2]</button>";
}

sub BSformtextfield {
  return 
  "<div class=\"form-group\">
   <label for=\"$_[0]\" class=\"col-sm-2 control-label\">$_[2]</label>
    <div class=\"col-sm-5\">
   	 <input type=\"text\" class=\"form-control\" name=\"$_[0]\" id=\"$_[0]\" value=\"$_[1]\">
   	</div>
  </div>"
}

sub BStextarea {
	  return 
  "<div class=\"form-group\">
   <label for=\"$_[0]\" class=\"col-sm-2 control-label\">$_[2]</label>
    <div class=\"col-sm-5\">
   	 <textarea class=\"form-control\" rows=\"3\" name=\"$_[0]\" id=\"$_[0]\" value=\"$_[1]\"></textarea>
   	</div>
  </div>"
}

sub BSformpasswordfield {
	return
 "<div class=\"form-group\">
   <label for=\"$_[0]\" class=\"col-sm-2 control-label\">$_[2]</label>
    <div class=\"col-sm-5\">
   	 <input type=\"password\" class=\"form-control\" name=\"$_[0]\" id=\"$_[0]\" value=\"$_[1]\">
   	</div>
  </div>"
}

sub BSemailfield {
	return
  "<div class=\"form-group\">
   <label for=\"$_[0]\" class=\"col-sm-2 control-label\">$_[2]</label>
  	<div class=\"col-sm-5\">
      <input type=\"email\" class=\"form-control\" name=\"$_[0]\" id=\"$_[0]\" value=\"$_[1]\">
    </div>
  </div>"
}

sub BSradiofield {
	return
  "<div class=\"radio\">
   <label>
   	<input type=\"radio\" name=\"$_[0]\" id=\"$_[0]\" value=\"$_[1]\">
    $_[2]
   </label>
  </div>"
}

sub BSradiofieldchecked {
	return
  "<div class=\"radio\">
   <label>
   	<input type=\"radio\" name=\"$_[0]\" id=\"$_[0]\" value=\"$_[1]\" checked>
    $_[2]
   </label>
  </div>";
}

sub BSAlert {
return
	"<div class=\"alert alert-danger alert-dismissible\" role=\"alert\">
  <button type=\"button\" class=\"close\" data-dismiss=\"alert\"><span aria-hidden=\"true\">&times;</span><span class=\"sr-only\">Close</span></button>
  <strong>Error: </strong> $_[0]
</div>";
}

sub BSSuccess {
return
	"<div class=\"alert alert-success alert-dismissible\" role=\"alert\">
  <button type=\"button\" class=\"close\" data-dismiss=\"alert\"><span aria-hidden=\"true\">&times;</span><span class=\"sr-only\">Close</span></button>
  <strong>Note: </strong> $_[0]
</div>";
}


#Nav Bar from bootstrap
sub NavBar {
return 
"<!-- Adapted from bootstrap fixed navbar example http://getbootstrap.com/examples/navbar-fixed-top/-->
<nav class=\"navbar navbar-default navbar-fixed-top\" role=\"navigation\">
 <div class=\"container-fluid\">
   <div class=\"navbar-header\">
   	  	<button type=\"button\" class=\"navbar-toggle collapsed\" data-toggle=\"collapse\" data-target=\"#navbar\" aria-expanded=\"false\" aria-controls=\"navbar\">
            <span class=\"sr-only\">Toggle navigation</span>
            <span class=\"icon-bar\"></span>
            <span class=\"icon-bar\"></span>
            <span class=\"icon-bar\"></span>
        </button>
      <a class=\"navbar-brand\" href=\"love2041.cgi\">LOVE2041</a>
   </div>
   <div id=\"navbar\" class=\"navbar-collapse collapse\">
    <div>
      <form method=\"GET\" action=\"$url?\" class=\"navbar-form navbar-left\" role=\"search\">
            <select class=\"form-control\" name=\"type\">
			  <option>username</option>
			  <option>gender</option>
			  <option>hair_colour</option>
			  <option>degree</option>
			  <option>courses</option>
			  <option>favourite_books</option>
			  <option>favourite_hobbies</option>
			  <option>favourite_movies</option>
			  <option>favourite_bands</option>
			  <option>favourite_tv_shows</option>
			</select>

         <div class=\"form-group\">
           <div class=\"input-group\">
            <input type=\"hidden\" name=\"view\" value =\"search\">
            <input type=\"text\" name=\"search\" class=\"form-control\" placeholder=\"Search\">
            <span class=\"input-group-btn\">
     		   <button type=\"submit\" class=\"btn btn-default\" type=\"button\">Search</button>
     		 </span>
     	   </div>
         </div>
      </form>    
    </div>
   <div>
      <ul class=\"nav navbar-nav navbar-left\">
         <li><a href=\"love2041.cgi?view=browse\">Browse</a></li>
      </ul>
      <ul class=\"nav navbar-nav navbar-right\">
         <li class=\"	dropdown\">
            <a href=\"#\" class=\"dropdown-toggle\" data-toggle=\"dropdown\">
               $name <b class=\"caret\"></b>
            </a>
            <ul class=\"dropdown-menu\">
               <li><a href=\"?view=myacct\">Account Settings</a></li>
               <li><a href=\"?view=myprofile\">My Profile</a></li>
               <li class=\"divider\"></li>
               <li><a href=\"?logout\">Logout</a></li>
            </ul>
         </li>
      </ul>
   </div>
  </div>
  </div>
</nav>";
}

# Other HTML functions

sub divopen {
	if (defined $_[0]) {
		return "<div class=\"$_[0]\">";
	} else {
		return "<div>";
	}
}

sub divclose {
	return "</div>"
}

sub hyperlink {
	"<a href =\"".$url."?$_[0]"."\">$_[1]</a>";
}

#
# HTML placed at top of every screen
#
sub page_header {
	my $html = ""; 

	$html .=    header();
		# $('.dropdown-toggle').dropdown()


   	$html .= 	start_html("-title"=>"LOVE2041", 
   					-bgcolor=>"#FEDCBA",
   					-style=>{-src=>['http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css', 
   									'http://cdn.jsdelivr.net/jquery.bootstrapvalidator/0.5.2/css/bootstrapValidator.min.css',
   								    './browse.css']});
   
 	$html .= 	center(h2(i("LOVE2041")));

 	$html .=    NavBar();
 	return $html;
}

#
# HTML placed at bottom of every screen
# It includes all supplied parameter values as a HTML comment
# if global variable $debug is set
#
sub page_trailer {
	my $html = "";
	$html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
	$html .= "<!-- ".self_url()." -->\n" if $debug;
	$html .= "<!-- ".$url." -->\n" if $debug;
	$html .= "<script type=\"text/javascript\" src=\"//cdn.jsdelivr.net/jquery.bootstrapvalidator/0.5.2/js/bootstrapValidator.min.js\"></script>";

    $html .=   "<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js\"></script>";
    $html .=   "<script src=\"http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js\"></script>";
	$html .= end_html;
	return $html;
}

#give cs2041 ass2 love2041.cgi diary.txt git.tar login.cgi signup.cgi verify.cgi browse.css lostpass.cgi signin.css deleteacct.cgi

#scp login.cgi love2041.cgi signup.cgi verify.cgi browse.css lostpass.cgi signin.css deleteacct.cgi diary.txt cjth726@weill.cse.unsw.edu.au:/import/ravel/1/cjth726/public_html/ass2