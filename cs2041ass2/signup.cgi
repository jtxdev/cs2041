#!/usr/bin/perl -w

use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use CGI::Session;
use Digest::MD5 qw(md5_hex);

warningsToBrowser(1);
$students_dir = "./students";
$tmp_dir = "./tmp";
$verifyurl = url()."/verify.cgi";
$verifyurl =~ s/signup.cgi\///;

$signinurl = url()."/login.cgi";
$signinurl =~ s/signup.cgi\///;
$signinlink = "<a href=\"$signinurl\">Sign in</a>";


#Bootstrap code and signin example html/css template used

if(!param("Username") || !param("Password1") || !param("Password2") || !param("EmailAddress")) {
	print page_header();
	start_html("Love2041 Signup");
	if (defined param('error') && param('error') eq '1') {
		print BSAlert("That username is not valid");
	}
	if (defined param('error') && param('error') eq '2') {
		print BSAlert("That password is not valid");
	}
	if (defined param('error') && param('error') eq '3') {
		print BSAlert("That username is not valid");
		print BSAlert("That password is not valid");
	}
	if (defined param('error') && param('error') eq '4') {
		print BSAlert("That email is not valid");
	}
	if (defined param('error') && param('error') eq '5') {
	    print BSAlert("That username is not valid");
		print BSAlert("That email is not valid");
	}
	if (defined param('error') && param('error') eq '6') {
	    print BSAlert("That password is not valid");
		print BSAlert("That email is not valid");
	}
	if (defined param('error') && param('error') eq '7') {
		print BSAlert("That username is not valid");
	    print BSAlert("That password is not valid");
		print BSAlert("That email is not valid");
	}
	if (defined param('error') && param('error') eq '8') {
		print BSAlert("The passwords don't match");
	}
	if (defined param('error') && param('error') eq '9') {
		print BSAlert("That username is not valid");
		print BSAlert("The passwords don't match");
	}
	if (defined param('error') && param('error') eq '10') {
		print BSAlert("That password is not valid");
		print BSAlert("The passwords don't match");
	}
	if (defined param('error') && param('error') eq '11') {
		print BSAlert("That username is not valid");
		print BSAlert("That password is not valid");
		print BSAlert("The passwords don't match");
	}
	if (defined param('error') && param('error') eq '12') {
		print BSAlert("That email is not valid");
		print BSAlert("The passwords don't match");
	} 
	if (defined param('error') && param('error') eq '13') {
		print BSAlert("That username is not valid");
		print BSAlert("That email is not valid");
		print BSAlert("The passwords don't match");
	} 
	if (defined param('error') && param('error') eq '14') {
	    print BSAlert("That password is not valid");
		print BSAlert("That email is not valid");
		print BSAlert("The passwords don't match");
	}
	if (defined param('error') && param('error') eq '15') {
		print BSAlert("That username is not valid");
	    print BSAlert("That password is not valid");
		print BSAlert("That email is not valid");
		print BSAlert("The passwords don't match");
	}
	if (defined param('error') && param('error') eq '16') {
		print BSAlert("That username is already taken");
	}

	print signup_form();
	print end_html(),
} elsif (param("Username") && param("Password1") && param("Password2") && param("EmailAddress")) {
	$check = 0;
	$username = param("Username");
	chomp $username;
	if ($username !~ /^[a-zA-Z0-9_]+$/ || length($username) < 6 || length($username) > 30) {
		$check += 1;
	}
	$password = param("Password1");
	chomp $password;
	if (length($password) < 6 || length($password) > 30) {
		$check += 2;
	}
	$emailaddr = param("EmailAddress");
	chomp $emailaddr;
	if ($emailaddr !~ /\@/) {
		$check += 4;
	}
	$password2 = param("Password2");
	chomp $password2;
	if ($password ne $password2) {
		$check += 8;
	}


	my @students = glob("$students_dir/*");
	$_=lc for @students;

	my $userdirectory = lc("$students_dir/$username");

	my $usertmpdir = "$tmp_dir/$username/";
	if ($check > 0) {
		print redirect("signup.cgi?error=$check");
    	exit 0;
	}
	unless ( grep( /^$userdirectory$/, @students ) ) {
		print page_header(); 
		my $digest = md5_hex(rand);
		unless(mkdir $usertmpdir) {
			print BSInfo("Please check your email!");
			exit 0;
		}

		sendverificationemail($emailaddr, $username, $password, $digest);
		maketempacct($usertmpdir, $digest, $username, $password, $emailaddr);

		# print $check;
		# print @students;
		# print $userdirectory;

		print BSInfo("A verification link has been sent to your email!");
		exit 0;
	} else {
    	print redirect('signup.cgi?error=16');
    	exit 0;
	}
}	

sub sendverificationemail {
    my $from    = 'admin@love2041.com';
    my $to      = "$_[0]";
    my $subject = 'Thank you for signing up to LOVE2041';
  	my $message = "Thanks for signing up to LOVE2041 Your perfect match awaits you <3!\n\nYour Username is: $_[1]\nYour Password is: $_[2]\n\nJust one more step until your account is ready\nPlease follow this link to verify your acct: $verifyurl?username=$_[1]&verify=$_[3]";
	
	open(MAIL, "|/usr/sbin/sendmail -t");

	# Email Header
	print MAIL "To: $to\n";
	print MAIL "From: $from\n";
	print MAIL "Subject: $subject\n\n";
	# Email Body
	print MAIL $message;

	close MAIL;
}

sub maketempacct {
	open newacct, ">$_[0]/verify.txt" or die "can not open $_[0]/verify.txt: $!";
	print newacct "$_[1]";
	close newacct;

	open newacct, ">$_[0]/profile.txt" or die "can not open $_[0]/profile.txt: $!";
	print newacct "username:\n\t$_[2]\npassword:\n\t$_[3]\nemail:\n\t$_[4]";
	close newacct;

	open newacct, ">$_[0]/preferences.txt" or die "can not open $_[0]/profile.txt: $!";
	print newacct "";
	close newacct;
}


sub signup_form {
	return
	"<!-- Adapted from bootstrap signin example template http://getbootstrap.com/examples/signin/-->
	<div class=\"container\">

      <form class=\"form-signup\" method=\"post\" role=\"form\">
        <h2 class=\"form-signup-heading\">Love2041 Registration</h2>

		<div class=\"form-group\">
		   	<label for=\"Username\" class=\"control-label\">Username</label>
       			 <input type=\"text\" name=Username id=Username class=\"form-control\" placeholder=\"Username\" required=\"\">
		</div>    
		<div class=\"form-group\">
		   	<label for=\"Password1\" class=\"control-label\">Password</label>
       			 <input type=\"password\" name=Password1 id=Password1 class=\"form-control\" placeholder=\"Password\" required=\"\">
		</div>
		<div class=\"form-group\">
		   	<label for=\"Password2\" class=\"control-label\">Confirm Password</label>
       			 <input type=\"password\" name=Password2 id=Password2 class=\"form-control\" placeholder=\"Password\" required=\"\">
		</div>
		<div class=\"form-group\">
		   	<label for=\"EmailAddress\" class=\"control-label\">Email Address</label>
       			<input type=\"email\" name=EmailAddress id=EmailAddress class=\"form-control\" placeholder=\"Email Address\" required=\"\">
		</div>
        <button class=\"btn btn-lg btn-primary btn-block\" type=\"submit\">Sign up</button>
        <br>Have an account? $signinlink
      </form>
    </div>"
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

sub page_trailer {
	my $html = "";
	$html .= join("", map("<!-- $_=".param($_)." -->\n", param())) if $debug;
	$html .= "<!-- ".self_url()." -->\n";
	$html .= "<!-- ".$url." -->\n";
	$html .= end_html;
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
