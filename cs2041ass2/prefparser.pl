#!/usr/bin/perl

#loading profile variables

$students_dir = "./students2";

#load_allprofiles();
load_pref();

print get_preferences();

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

sub load_pref {
	my $student_to_show  = $_[0];
	my $pref_filename = "$student_to_show\preferences.txt";
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
			$profile_field_info = "$profile_field_info|$1";
			$studentprofileinfo{$_[0]}{$profile_field} = $profile_field_info;
		} 
	}
	#$profile .= "profile.txt $count\n";
	close $p;
}

sub get_pref_field {
	if (defined $studentprefinfo{$_[0]}{$_[1]}) {
		return $studentprefinfo{$_[0]}{$_[1]}
	} else {
		return "";
	}
}

sub get_preferences {
	my $pref = "";
	$pref .= "Gender: ".get_pref_field($_[0], 'gender')."\n";
	$pref .= "Age: ".get_pref_field($_[0], 'age')."\n";
	$pref .= "Hair Colour: ".get_pref_field($_[0], 'hair_colours')."\n";
	$pref .= "Height: ".get_pref_field($_[0], 'height')."\n";
	$pref .= "Weight: ".get_pref_field($_[0], 'weight')."\n";
	$pref .= "Degree: ".get_pref_field($_[0], 'degree')."\n";
	$pref .= "Courses: ".get_pref_field($_[0], 'courses')."\n";
	return $pref;
}



