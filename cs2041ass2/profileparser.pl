#!/usr/bin/perl

#loading profile variables

%studentprofileinfo;
$students_dir = "./students";

#load_allprofiles();
load_profile();
print get_profile(samplestudent);


sub load_allprofiles {
	my @students = glob("$students_dir/*");
	foreach $student (@students) {
		#$profile .= "$student\n";
		$count = 0;
		my $student_to_show  = $student;
		my $profile_filename = "$student_to_show/profile.txt";
		#$profile .= "$profile_filename\n";
		open my $p, "$profile_filename" or die "can not open $profile_filename: $!";
		while (<$p>) {
			if (/^(\w*):/) {
			 	$count++;
			}
			#$profile .= "$1\n" if (/^(\w*):/);
		}
		if ($count >= 16) {
			$profile .= "$profile_filename $count\n";
		}
		close $p;
	}
}

sub load_profile {
	$count = 0;
	$profile_field = "";
	$profile_field_info = "";
	open my $p, "profile.txt" or die "can not open profile.txt: $!";
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
			$profile_field_info = "$profile_field_info|$1";
			$studentprofileinfo{samplestudent}{$profile_field} = $profile_field_info;
		} 
	}
	#$profile .= "profile.txt $count\n";
	close $p;
}

sub load_pref {
	$count = 0;
	$profile_field = "";
	$profile_field_info = "";
	open my $p, "preference.txt" or die "can not open preference.txt: $!";
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
			$profile_field_info = "$profile_field_info|$1";
			$studentprofileinfo{samplestudent}{$profile_field} = $profile_field_info;
		} 
	}
	#$profile .= "profile.txt $count\n";
	close $p;
}

sub get_profile {
	local $profile = "";
	$profile .= "Username: ".get_username($_[0])."\n";
	$profile .= "Name: ".get_name($_[0])."\n";
	$profile .= "Password: ".get_password($_[0])."\n";
	$profile .= "Email: ".get_email($_[0])."\n";
	$profile .= "Gender: ".get_gender($_[0])."\n";
	$profile .= "Birthdate: ".get_birthdate($_[0])."\n";
	$profile .= "Hair Colour: ".get_hair_colour($_[0])."\n";
	$profile .= "Height: ".get_height($_[0])."\n";
	$profile .= "Weight: ".get_weight($_[0])."\n";
	$profile .= "Degree: ".get_degree($_[0])."\n";
	$profile .= "Courses: ".get_courses($_[0])."\n";
	$profile .= "Favourite Books: ".get_favourite_books($_[0])."\n";
	$profile .= "Favourite Hobbies: ".get_favourite_hobbies($_[0])."\n";
	$profile .= "Favourite Movies: ".get_favourite_movies($_[0])."\n";
	$profile .= "Favourite Bands: ".get_favourite_bands($_[0])."\n";
	$profile .= "Favourite TV Shows: ".get_favourite_TV_Shows($_[0])."\n";
	return $profile;
}

sub get_name {
	return $studentprofileinfo{$_[0]}{name};
}

sub get_username {
	return $studentprofileinfo{$_[0]}{username};
}

sub get_password {
	return $studentprofileinfo{$_[0]}{password};
}

sub get_gender {
	return $studentprofileinfo{$_[0]}{gender};
}

sub get_birthdate {
	return $studentprofileinfo{$_[0]}{birthdate};
}

sub get_height {
	return $studentprofileinfo{$_[0]}{height};
}

sub get_degree {
	return $studentprofileinfo{$_[0]}{degree};
}

sub get_email {
	return $studentprofileinfo{$_[0]}{email};
}

sub get_favourite_books {
	return $studentprofileinfo{$_[0]}{favourite_books};
}

sub get_favourite_hobbies {
	return $studentprofileinfo{$_[0]}{favourite_hobbies};
}

sub get_favourite_movies {
	return $studentprofileinfo{$_[0]}{favourite_movies};
}

sub get_favourite_TV_Shows {
	return $studentprofileinfo{$_[0]}{favourite_TV_Shows};
}

sub get_favourite_bands {
	return $studentprofileinfo{$_[0]}{favourite_bands};
}

sub get_courses {
	return $studentprofileinfo{$_[0]}{courses};
}

sub get_weight {
	return $studentprofileinfo{$_[0]}{weight};
}

sub get_hair_colour {
	return $studentprofileinfo{$_[0]}{hair_colour};
}



