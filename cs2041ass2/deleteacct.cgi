#!/usr/bin/perl -w


#HTML/CSS Provided by http://getbootstrap.com/examples/signin/fd

use CGI qw/:all/;
use CGI::Carp qw(fatalsToBrowser warningsToBrowser);
use File::Path qw( rmtree );

warningsToBrowser(1);
$students_dir = "./students";

$signupurl = url()."/signup.cgi";
$signupurl =~ s/deleteacct.cgi\///;
$signuplink = "<a href=\"$signupurl\">Signup Now!</a>";

if(!param("Username") || !param("Password") || !param("Check")) {
		print page_header();
		start_html("Love2041 Account Obliterator");

		if (defined(param('error')) && param('error') eq "1") {
			$deleteacctscreen .= BSAlert("I'm sorry we do not recognise that username!");
		} elsif (defined(param('error')) && param('error') eq "2") {
			$deleteacctscreen .= BSAlert("Incorrect Username or Password");
		}

		$deleteacctscreen .= deleteacct_form();
		
		print $deleteacctscreen;

		print end_html(),
	} elsif (param("Username") && param("Password")) {
		$username = param("Username");
		$username =~ s/\W//g;
		chomp $username;
		$password = param("Password");
		chomp $password;
		$userdirectory = "$students_dir/$username/";
		if (!open F, "<$userdirectory") {
			print redirect('deleteacct.cgi?error=1');
		} else {
			load_profile($userdirectory);
			$correct_password = $studentprofileinfo{$userdirectory}{password};
			$correct_password =~ s/^\|//;
		    if ($password eq $correct_password) {
		        print page_header();
		        rmtree($userdirectory);
		        print BSSuccess("ACCOUNT DELETED. HAVE A NICE LIFE.");
		    } else {
		    	print redirect('deleteacct.cgi?error=2');
		    }
		}
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

sub deleteacct_form {
	"<!-- Adapted from bootstrap signin example template http://getbootstrap.com/examples/signin/-->
	<div class=\"container\">

      <form class=\"form-signin\" method=\"post\" role=\"form\">
        <h2 class=\"form-signin-heading\">We hope you found love :3</h2>
        <input type=\"text\" name=\"Username\" class=\"form-control\" placeholder=\"Username\" required=\"\" autofocus=\"\">
        <input type=\"password\" name=\"Password\" class=\"form-control\" placeholder=\"Password\" required=\"\">
        <div class=\"checkbox\">
        	<label>
          		<input type=\"checkbox\" name=\"Check\" required> Really delete my account
        	</label>
     	</div>
        <button class=\"btn btn-lg btn-danger btn-block\" type=\"submit\">Delete Account</button>
        <br>Don't have an account? $signuplink
      </form>

    </div>"
}

#
sub page_header {
	my $html = ""; 

	$html .=    header();
   	$html .= 	start_html("-title"=>"LOVE2041", 
   					-bgcolor=>"#FEDCBA",
   					-style=>{-src=>['http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css', 'http://cdn.jsdelivr.net/jquery.bootstrapvalidator/0.5.2/css/bootstrapValidator.min.css', './signin.css']});


	$html .= "<script type=\"text/javascript\" src=\"//cdn.jsdelivr.net/jquery.bootstrapvalidator/0.5.2/js/bootstrapValidator.min.js\"></script>";
    $html .=   "<script src=\"https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js\"></script>";
    $html .=   "<script src=\"http://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js\"></script>";
   

 	$html .= 	center(h1(i("nomoreL&lt/3VE2041")));
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
  <strong>Error: </strong> $_[0]
</div>"
}
