#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use CGI::Session;
use Digest::MD5 qw(md5_hex);

warningsToBrowser(1);
$students_dir = "./students";
$tmp_dir = "./tmp";
$loginurl = url()."/login.cgi";
$loginurl =~ s/lostpass.cgi\///;


$signinurl = url()."/login.cgi";
$signinurl =~ s/lostpass.cgi\///;
$signinlink = "<a href=\"$signinurl\">Sign in</a>";

$username = param("username");
if ($username =~ /\@/) {
	$type = 'email';
} else {
	$type = 'username';
}

if (!param("username")) {
	print page_header();
	if (param('error') eq "1") {
		print BSAlert("Sorry we don't recognise that username");
	}
	if (param('error') eq "2") {
		print BSAlert("Sorry we don't recognise that email");
	} 
	print lostpass_form();
	exit 0;
} elsif ($type eq 'username') {
	$userdirectory = "$students_dir/$username";
	if (-d "$userdirectory") {
		load_profile($userdirectory);
		$correctpassword = $studentprofileinfo{$userdirectory}{password};
		$correctpassword =~ s/^\|//;

		$emailaddr = $studentprofileinfo{$userdirectory}{email};
		$emailaddr =~ s/^\|//;

		sendlostpassword($emailaddr, $username, $correctpassword);
		print page_header();
		print BSSuccess("Your details have been sent to your email");
		exit 0;
	}
	print redirect('lostpass.cgi?error=1');
	exit 0;
} elsif ($type eq "email") {
	load_allprofiles();
	$sent = 0;
	$username = lc($username);

	foreach $student (keys %studentprofileinfo) {
		if (lc($studentprofileinfo{$student}{email}) =~ /$username/) {
			$student =~ s/$students_dir\///;
			$correctpassword = $studentprofileinfo{$userdirectory}{password};
			$correctpassword =~ s/^\|//;
			sendlostpassword($emailaddr, $student, $correctpassword);
			$sent = 1;
		}
	}

	if ($sent == 1) {
		print page_header();
		print BSSuccess("Your details have been sent to your email");
		exit 0;
	} else {
		print redirect('lostpass.cgi?error=2');
		exit 0;
	}
}

sub lostpass_form {
	return
	"<!-- Adapted from bootstrap signin example template http://getbootstrap.com/examples/signin/-->
	<div class=\"container\">

      <form class=\"form-signup\" role=\"form\">
        <h2 class=\"form-signup-heading\">Lost your password?</h2>

		<div class=\"form-group\">
		   	<label for=\"Username\" class=\"control-label\">Enter Username or Email</label>
       			 <input type=\"text\" name=username id=Username class=\"form-control\" placeholder=\"Username or Email\" required=\"\">
		</div>    
        <button class=\"btn btn-lg btn-primary btn-block\" type=\"submit\">Submit</button>
      </form>
    </div>"
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

sub sendlostpassword {
    my $from    = 'passwordrecovery@love2041.com';
    my $to      = "$_[0]";
    my $subject = 'Love2041 Password Recovery';
  	my $message = "Here are your login details:\n\nYour Username is: $_[1]\nYour Password is: $_[2]\n\nLogin at: $loginurl";
	
	open(MAIL, "|/usr/sbin/sendmail -t");

	# Email Header
	print MAIL "To: $to\n";
	print MAIL "From: $from\n";
	print MAIL "Subject: $subject\n\n";
	# Email Body
	print MAIL $message;

	close MAIL;
}

sub page_header {
	my $html = ""; 

	$html .=    header();
   	$html .= 	start_html("-title"=>"LOVE2041", 
   					-bgcolor=>"#FEDCBA",
   					-style=>{-src=>['http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css', 'http://cdn.jsdelivr.net/jquery.bootstrapvalidator/0.5.2/css/bootstrapValidator.min.css', './signin.css']});


	$html .= "<script type=\"text/javascript\" src=\"//cdn.jsdelivr.net/jquery.bootstrapvalidator/0.5.2/js/bootstrapValidator.min.js\"></script>";
    $html .=   "<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js\"></script>";
    $html .=   "<script src=\"http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js\"></script>";
   

 	$html .= 	center(h1(i("LOVE2041")));
 	return $html;
}

sub BSAlert {
	"<div class=\"alert alert-danger alert-dismissible\" role=\"alert\">
  <button type=\"button\" class=\"close\" data-dismiss=\"alert\"><span aria-hidden=\"true\">&times;</span><span class=\"sr-only\">Close</span></button>
  <strong>Error: </strong> $_[0]
</div>"
}

sub BSSuccess {
	"<div class=\"alert alert-success alert-dismissible\" role=\"alert\">
  <button type=\"button\" class=\"close\" data-dismiss=\"alert\"><span aria-hidden=\"true\">&times;</span><span class=\"sr-only\">Close</span></button>
  <strong>Note: </strong> $_[0]
</div>"
}

sub BSInfo {
	"<div class=\"alert alert-info alert-dismissible\" role=\"alert\">
  <button type=\"button\" class=\"close\" data-dismiss=\"alert\"><span aria-hidden=\"true\">&times;</span><span class=\"sr-only\">Close</span></button>
  <strong>Note: </strong> $_[0]
</div>"
}
