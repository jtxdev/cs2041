#!/usr/bin/perl
# Starting point for COMP2041/9041 assignment 
# http://www.cse.unsw.edu.au/~cs2041/assignments/python2perl
# written by andrewt@cse.unsw.edu.au September 2014
use warnings;
use strict;
use Text::Tabs;
use Text::Balanced 'extract_bracketed';

$tabstop = 4;

my $pythonfile = $ARGV[0];
open(F,"<$pythonfile") or die "$0: Can't open $pythonfile: $!\n";
my @pythoncodewithtabs = <F>;
chomp(@pythoncodewithtabs);
my @pythoncode = expand(@pythoncodewithtabs);
my %seenvars;
my @vars;
my @arrs;
my @hashes;
my @nums;
my @strs;
my $handled = 0;

# first loop:
	# stores potential scalar variables
	# stores potential array names
	# stores potential hash names
	# converts basic python control flow keywords to perl syntax
	# converts range() function
	# converts print formatting
	# converts sys functions
	# converts re functions
	# converts split and join



foreach my $line (@pythoncode) {

	# converts "else if" to "elif" (python to perl syntax change)

	$line =~ s/elif/elsif/;
	
	# converts "<>"to "!=" operator;

	$line =~ s/<>/!=/;

	# handles comments at the end of lines of code

	if ($line =~ /^[^#]+#/) {
		$line =~ s/#/;#/;
	}
	
	# identifies print:
		# Python's print print a new-line character by default
		# so we need to add it explicitly to the Perl print statement

	if ($line =~ /print/) {
		if ($line =~ /print\s*"(.*)"\s*$/) {
	
			# handles "" strings
		
			$line =~ s/print\s*"(.*)"\s*$/print \"$1\\n\"/;
		} elsif ($line =~ /\s*print\s*([^;]*);/) { 

			# handles print within one liners

			$line =~ s/print\s*([^;]*);/print $1, \"\\n\"; /;
		} elsif ($line =~ /\s*print\s*"(.*)"\s*%\s*(.*)\s*$/) {
			$line =~ s/print\s*"(.*)"\s*%\s*(.*)\s*$/printf \"$1\\n\", $2/;
		} elsif ($line =~ /\s*print\s*(.*)\s*$/) {
	
			# handles all other prints
			if ($1 ne "") {
				$line =~ s/print\s*(.*)\s*$/print $1, \"\\n\"/;
			} else {
				$line =~ s/print\s*(.*)\s*$/print \"\\n\"/;
			}
		} else {
			
			# Lines we can't translate are turned into comments
			# just incase @_@?
		
			$line = "#$line";
		}

			#removes "\n" if , at end of python print

		if ($line =~ /\,\,/) {
			$line =~ s/\,\, \"\\n\"//;
		}
	}

	# handles re functions

	if ($line =~ /re\./) {

		# handles re.match
		if ($line =~ /re.match/) {
			$handled = $line =~ s/re.match\(\s*r['"]((.*))['"],\s*(\w+)\s*\)/$3 =~ thisisaflag\/^($1)\//;
			if ($handled == 0) {
				$line =~ s/re.match\(\s*r['"]((.*))['"],\s*(\w+)\s*,\s*(.*)\s*\)/$3 =~ thisisaflag\/^($1)\/$4/;
				if ($4 ne "") {
					my $mods = $4;
					$line =~ s/\|*re.M/m/;
					$line =~ s/\|*re.I/i/;
					$line =~ s/\|*re.L/l/;
					$line =~ s/\|*re.U/u/;
					$line =~ s/\|*re.X/x/;
					$line =~ s/\|*re.S//;
				}
			}
		}

		# handles re.search
		if ($line =~ /re.search/) {
		$handled = $line =~ s/re.search\(\s*r['"]((.*))['"],\s*(\w+)\s*\)/$3 =~ thisisaflagm\/($1)\//;
			if ($handled == 0) {	
				$handled = $line =~ s/re.search\(\s*r['"]((.*))['"],\s*(\w+)\s*,\s*(.*)\s*\)/$3 =~ thisisaflagm\/($1)\/$4/;
				if ($4 ne "") {
					my $mods = $4;
					$line =~ s/\|*re.M/m/;
					$line =~ s/\|*re.I/i/;
					$line =~ s/\|*re.L/l/;
					$line =~ s/\|*re.U/u/;
					$line =~ s/\|*re.X/x/;
					$line =~ s/\|*re.S//;
				}
			}
		}


		# handles re.sub

		$line =~ s/re.sub\(\s*r['"]((.*))['"],\s*['"](.*)['"],\s*(\w+)\s*\)/$4 =~ thisisaflags\/$2\/$3\/g/;



		# handles scalar conversion of list context of result of =~


		my $subbed = 0;
		$subbed = $line =~ s/\b(\w+)\b\s*=\s*\b(\w+)\b\s*=~\s*thisisaflags(.*)/($1 = $2) =~ thisisaflags$3/;
		if ($subbed) {
			$line =~ /\b(\w+)\b/;
			if ($seenvars{$1}++ == 0) {
				push (@vars, $1);
			}
		}

		$subbed = $line =~ s/\b(\w+)\b\s*=\s*\b(\w+)\b\s*=~\s*thisisaflag([^s])(.*)/$2 =~ thisisaflag$3$4; $1 = \$1/;
		if ($subbed) {
			print "## $1\n";
			if ($seenvars{$1}++ == 0) {
				push (@vars, $1);
			}
		}

	}

	# handle split and join

		# split

	if ($line =~ /\.split/) {
	$line =~ s/(\$?\w+)\.split\(\'(.)\'\)/split(\/\\$2\/, $1)/;
		if ($line =~ /\b(\w+)\b\s*=\s*\bsplit\(\/\\(.)\/, (\$?\w+)\)/) {
			my $array = $1;
			$line =~ s/$array/\@$array/;
		}
	}
		# join
	if ($line =~ /['"](.)['"]\.join(.*)\s*/) {

		my $delim = $1;
		my $endofline = $2;
		my $oldjoin;
		my $oldremainder;
		my $newjoin;


		my @result = extract_bracketed( $endofline, '()' );

		$oldjoin = $result[0];
		$oldremainder = $result[1];
		print "#oldjoin $oldjoin\n";
		$oldjoin =~ /\((.*)\)/;
		$newjoin = "join(\"$delim\", $1)";
		$line =~ /(.*)['"](.)['"]\.join/;
		print "#line $line\n";
		$line = "$1$newjoin$oldremainder";

	#$line =~ s/['"](.)['"]\.join\((.*)\)/join("$1", $2)/;
	}
	# handles sys functions
	if ($line =~ /sys\./) {

		$handled = 0;

		#handles sys.argv

		$handled += $line =~ s/sys.argv/ARGV/;

		if ($handled > 0) {
			print "#SYS $line\n";
		}
		# handles sys.stout.write()

		#if ($line =~ /sys\.stdout\.write\((.*)\)\s*$/) {
			# handles sys.stout.write()
			
		$handled += $line =~ s/sys\.stdout\.write\((.*)\)\s*$/print $1/;

		#} elsif ($line =~ /sys\.stdin\.readline\(\)/) {

			# handles sys.stdin.readline()

		$handled +=	$line =~ s/sys\.stdin\.readline\(\)/<STDIN>/;
		#} elsif ($line =~ /sys\.stdin\.readlines\(\)/) {

			# handles sys.stdin.readlines()

			if ($line =~ /\b(\w+)\b\s*=\s*sys\.stdin\.readlines\(\)/) {
				my $array = $1;
				$line =~ s/$array/\@$array/;
			$handled +=	$line =~ s/sys\.stdin\.readlines\(\)/<STDIN>/;
				#print "#$line\n";
			}
		#} elsif ($line =~ /sys\.stdin/) {

			# handles sys.stdin

			$handled +=$line =~ s/sys\.stdin/<STDIN>/;
		#} else {
			
			# Lines we can't translate are turned into comments
			# just incase @_@?
		if ($handled == 0) {
			$line = "#$line";
		}
		#}
	}

	# identifies and stores variable
	# Handles scalar/array assignments

	if ($line =~ /^\s*\b(\w+)\b\s*=/) {

		if ($line =~ /^\s*\b(\w+)\b\s*=\s*(\[|open)/) {

			# handles array initialisation

			if ($line =~ /^\s*\b(\w+)\b\s*=\s*\[\]/) {
				$line = "#\@$line\n";
			} elsif ($line =~ /^\s*\b(\w+)\b\s*=\s*open/) {
			} else {
				$line =~ s/\[/\(/;
				$line =~ s/\]/\)/;
			}
			if ($seenvars{$1}++ == 0) {
				push (@arrs, $1);
			}
		} elsif ($line =~ /^\s*\b(\w+)\b\s*=\s*\{/) {

			# handles hash initialisation
			if ($line =~ /^\s*\b(\w+)\b\s*=\s*\{\}/) {
				$line = "#\%$line";
			}
			if ($seenvars{$1}++ == 0) {
				push (@hashes, $1);
			}
		} else { 

			# handles scalar initialisation

			if ($seenvars{$1}++ == 0) {
				push (@vars, $1);
			}
		}
	} elsif ($line =~ /^\s*\@(\w+)\b\s*=/) {

			# handles preconverted array

		if ($seenvars{$1}++ == 0) {
			push (@arrs, $1);
		}
	}

	if ($line =~ /for\s*(\w*)\s*in\s*(.*):/) {

		# identifies and stores x as a variable in 'for x in'

		if ($seenvars{$1}++ == 0) {
			push (@vars, $1);
		}
		$line =~ s/for\s*(\w*)\s*in\s*(.*):/for $1 ($2):/;
		$line =~ s/for/foreach/;

	}

	# handles break 
	
	#if ($line =~ /break/) {
		$line =~ s/break/last/;
		$line =~ s/continue/next/;
	#} 
}

# second loop:
	# converts variables to perl syntax

foreach my $line (@pythoncode) {
	if ($line !~ /^#/) {
		foreach my $var (@vars) {

			# converts all instances of var

			$line =~ s/\b$var\b/\$$var/g;
			#if ($line =~ /^[^"]*"[^"]*("[^"]*"[^"]*)*[^"]*\$$var\b/) {

				# if var is between "s or 's --> unscalar

				$line =~ s/(^[^"]*"[^"]*("[^"]*"[^"]*)*[^"]*)\$$var\b/$1$var/;
				$line =~ s/(^[^']*'[^']*('[^']*'[^']*)*[^']*)\$$var\b/$1$var/;
			#}
		}
		foreach my $arr (@arrs) {

			#converts all non converted instances of arr
			if ($line !~ /\@$arr/) {
				$line =~ s/\b$arr\b/\@$arr/g;
			}
			#if ($line =~ /^[^"]*"[^"]*("[^"]*"[^"]*)*[^"]*\@$arr\b/) {

				# if arr is between "s or 's --> unarray

				$line =~ s/(^[^"]*"[^"]*("[^"]*"[^"]*)*[^"]*)\@$arr\b/$1$arr/;
				$line =~ s/(^[^']*'[^']*('[^']*'[^']*)*[^']*)\@$arr\b/$1$arr/;
			#}
		}
		foreach my $hash (@hashes) {

			$line =~ s/\b$hash\b/\%$hash/g;

			#if ($line =~ /^[^"]*"[^"]*("[^"]*"[^"]*)*[^"]*\@$hash\b/) {

				# if arr is between "s or 's --> unhash

				$line =~ s/(^[^"]*"[^"]*("[^"]*"[^"]*)*[^"]*)\%$hash\b/$1$hash/;
				$line =~ s/(^[^']*'[^']*('[^']*'[^']*)*[^']*)\%$hash\b/$1$hash/;
			#}
		}
	}
}

#third loop:
	# fixes perl type specific problems eg. length -> scalar if @ or %.

foreach my $line (@pythoncode) {

	#if ($line =~ /len\(/) {

		# converts len function 

	if ($line =~ /len\(\@(\w+)\)/) {
		$line =~ s/len/scalar/;

		#$line =~ s/len\(\@(\w+)\)/\@$1/;
	} else {
		$line =~ s/\blen\b/length/;
	}
	#}

		# converts rest of argv

	if ($line =~ /range(.*)\s*/) {

		my $range = $1;
		my $oldrange;
		my $newrange;

	# converts range functions to perl syntax eg. range(1, 3) -> (1..2)


		#extract balanced bracket after range

		my @result = extract_bracketed( $range, '()' );

		# print "#1 $result[0]\n";
		# print "#2 $result[1]\n";
		# print "#3 $result[2]\n";

		$oldrange = $result[0];

		#$range =~ /\((.*)\)/;
		if ($oldrange =~ /,/) {
			#print "##$oldrange\n";
			$oldrange =~ /\((.*),\s*(.*)\)/;
			$newrange = "$1..$2 - 1";
			$line =~ /(.*)range/;
			$line = "$1$newrange\):";
		} else {
			# single argument range
			#print "##$oldrange\n";
			$oldrange =~ /\((.*)\)/;
			$newrange = "0..$1 - 1";
			$line =~ /(.*)range/;
			$line = "$1$newrange\):";
		}
	}

	# handles open

	if ($line =~ /open\("*([^")]*)"*\)/) {

		my $filename = $1;
		my $filename2 = $filename;
		$filename2 =~ s/(\w)/<$1/;
		$line =~ s/open\("*([^")]*)"*\)/open F, "$filename2" or die "\$0: can not open $filename: \$!"/;
		
		# Temporary location for transforming

		$line =~ s/foreach\s*\$(\w+)\s*\((open F,[^)]*)\)/$2;while \$$1 = <F>/;
	
	}

	#handles fileinput.input();

	$line =~ s/foreach\s*\$(\w+)\s*\(fileinput.input\(\)\)/while \$$1 = <>/;
	
	#if ($line =~ /\@(.*)\.append\((.*)\)/) {

		# converts append function 

	if ($line =~ /\@(.*)\.append(.*)\s*/) {

		my $list = $1;
		my $endofline = $2;
		my $oldappend;
		my $oldremainder;
		my $newappend;


		my @result = extract_bracketed( $endofline, '()' );

		$oldappend = $result[0];
		$oldremainder = $result[1];
		print "#oldappend $oldappend\n";
		$oldappend =~ /\((.*)\)/;
		$newappend = "push(\@$list, $1)";
		$line =~ /(.*)\@(.*)\.append(.*)\s*/;
		print "#line $line\n";
		$line = "$1$newappend$oldremainder";

	#$line =~ s/\@(.*)\.append\((.*)\)/push\(\@$1, $2\)/;
	}

		#converts pop function
	if ($line =~ /\@(.*)\.pop(.*)\s*/) {

		my $list = $1;
		my $endofline = $2;
		my $oldpop;
		my $oldremainder;
		my $newpop;
		my $offset;


		my @result = extract_bracketed( $endofline, '()' );

		$oldpop = $result[0];
		$oldremainder = $result[1];
		print "#oldpop $oldpop\n";
		$oldpop =~ /\((.*)\)/;
		$offset = $1;
		if ($offset eq "") {
			$newpop = "splice(\@$list, -1, 1)";
		} else {
			$newpop = "splice(\@$list, $offset, 1)";
		}
		$line =~ /(.*)\@(.*)\.pop(.*)\s*/;
		print "#line $line\n";
		$line = "$1$newpop$oldremainder";

	#$line =~ s/\@(.*)\.pop\((.*)\)/splice(\@$1, $2, 1)/;
	}
	#}

	#if ($line =~ /\@(.*)\[/) {

		# converts ascessing array

	$line =~ s/\@(\w+)\[/\$$1\[/;

	# converts .group[]
	if ($line =~ /group/) {
		my $groupindex;
		my @matches;
		print "#group $line\n";
		@matches = $line =~ /(\$\w+\.group\(([^)]*)\))/g;
		#print @matches;
		foreach my $match (@matches) {
			print "# $match\n";
			$match =~ /\$\w+\.group\(([^)]*)\)/;
			if ($1 ne "") {
				$groupindex = $1 + 1;
				$line =~ s/\$\w+\.group\($1\)/\$$groupindex/g;
				#$line =~ s/\w+\.group\(([^)]*)\)/\\\$$groupindex/g;
			} else {
				$line =~ s/\$(\w+)\.group\(([^)]*)\)/\$$1/g;
			}
		}
	}
	#}

	#convert if element in hash

		# convert X (not) in Y
	$line =~ s/\$(\w+)\s*in\s*\%((\w+)(\[\$\w+\])*)/defined \%$2\[\$$1\]/;
	$line =~ s/\$(\w+)\s*not\s*in\s*\%((\w+)(\[\$\w+\])*)/!defined \%$2\[\$$1\]/;

		# convert sorted();
	$line =~ s/sorted\((%.+)\.keys\(\)\)/sort keys $1/;

	#converts split

	$line =~ s/(\$?\w+)\.split\(\'(.)\'\)/split(\/\\$2\/, $1)/;

	#converts accessing hashes
	if ($line =~ /\%(\w+)(\[(\$\w+)\])+/) {
			# Changed [] to {};
		$line =~ s/(\[(\$\w+)\])/\{$2\}/g; 
		print "#HASH $line\n";
		$line =~ s/\%((\w+)(\{\$\w+\})+)/\$$1/g;
	}
		#$line =~ s/\%(\w+)(\[(\$\w+)\])+/\$$1\{$3\}/g;
	$line =~ s/(?<=keys )(\$(\w+)(\{(\$\w+)\})+)/\%\{$1\}/;

	if ($line =~ /ARGV/) {	
		$line =~ s/ARGV/\$ARGV/;
		$line =~ s/\$ARGV\[1:\]/\@ARGV/;
		$line =~ s/1\.\.length\(\$ARGV\)/0\.\.\@ARGV/;
 	}

}



# fourth loop: 
	# Expanding loops and blocks

my $blocks = 0;
my $indentsize = 4;
foreach my $line (@pythoncode) {
	chomp $line;
	my $tabs = $indentsize * $blocks;
	my $previoustab = $indentsize * ($blocks - 1);
	my $do;
	my $tab = " " x $indentsize;
	if ($previoustab < 0) {
		$previoustab = 0;
	}
	#$line =~ s/\t/$tab/;

	# Inline with current indent

	#print "#$line $tabs\n";

	if ($line =~ /^\s{$tabs}(.*)/) { 
		#print "#tabs $line\n";
		#print "#NEWINDENT $blocks";
		# identifies if for foreach while
		if ($line =~ /^\s{$tabs}[^ ]?.*\b(if|for|foreach|while)\b\s*(.*):\s*(.*)/) {

			# converts to perl syntax eg. for x < 0: ---> while ($x < 0) {
			chomp $1;
			chomp $2;
			chomp $3;
			$do = $3;
			if ($do ne "") {
				#print "ONELINER $line\n";
				$line =~ s/\b(if|while|else|elsif)\b\s*(.*):\s*(.*)/$1 ($2) {\n\t$3;\n}/;
				$line =~ s/\b(for|foreach)\b\s*(.*):\s*(.*)/$1 $2 {\n\t$3;\n}/;
			} else {
				$blocks++;
				#print "#MULTILINERtabs $line\n";
				$line =~ s/\b(if|while|else|elsif)\b\s*(.*):\s*(.*)/$1 ($2) {/;
				$line =~ s/\b(for|foreach)\b\s*(.*):\s*(.*)/$1 $2 {/;
			}
		}

		if ($line eq $pythoncode[$#pythoncode] and $blocks > 0) {

			# eof reached, close all open {'s

			chomp $line;
			my $str = ""; 
			foreach (0..$blocks - 1) {
				my $indent = $tab x --$blocks; 
				$str = "$str$indent}\n";
			}
			$line = "$line;\n$str";
		}

	#Inline with -1 indent

	} elsif ($line =~ /^\s{$previoustab}.*/) {

		#print "#pretabs $line\n";
		#print "#OLDINDENT $blocks ";

		# converts to perl syntax eg. for x < 0: ---> for (x < 0) {

		if ($line =~ /^\s{$previoustab}[^ ]?.*\b(if|for|foreach|while|else|elsif)\b\s*(.*):\s*(.*)/) {
			
			# if first line unindented is another if for else etc.

			$do = $3;
			if ($do ne "") {

			#print "ONELINER $line\n";
					# for one liners eg if x: {a; b; c;}

					$line =~ s/\b(if|while|else|elsif)\b\s*(.*):\s*(.*)/}\n$1 ($2) {\n\t$3;\n}/;
					$line =~ s/\b(for|foreach)\b\s*(.*):\s*(.*)/}\n$1 $2 {\n\t$3;\n}/;
					#$blocks--;
			} else {

			#print "#MULTILINER $line\n";
					#apply correct closing bracket and indentation according to keyword
				if ($1 eq "else") {
					$line =~ s/\b(else)\b\s*(.*):\s*(.*)/} $1 {/;
				} elsif ($1 eq "elsif") {
					$line =~ s/\b(elsif)\b\s*(.*):\s*(.*)/} $1 ($2) {/;	
				} else {
					$line =~ s/\b(if|while)\b\s*(.*):\s*(.*)/$1 ($2) {/;
					$line =~ s/\b(for|foreach)\b\s*(.*):\s*(.*)/$1 $2 {/;
					$line =~ /^(\s*)/;
					$line = "$1}\n$line";
				}
			}
		} else {
			
			# just append } and start newline with correct indentation

			$line =~ /^(\s*)/;
			$line = "$1}\n$line";
			$blocks--;
		}
	} elsif ($blocks > 0) {
		$line =~ /^(\s*)/;
		my $count = length( $1 ) / 4;
		my $count2;
		my $str = "";
		while ($count < $blocks) {
			$count2 = $count;
			while ($count2 < $blocks - 1) {
				$str = "$str$tab";
				$count2++;
			}
			$str = "$str}\n";
			$count++;
		}
		$line = "$str$line";
		$blocks -= $count;
	}
}


# String loop
foreach my $line (@pythoncode) {
	chomp $line;
	if ($line =~ /\+/) {
		if ($line =~ /(^[^"]*("[^"]*"[^"]*)*[^"]*)\s*\+\s*"(.*)"/) {
			$line =~ s/\+/\./;
		} 
	}
	if ($line =~ /\*/) {
		#if ($line =~ /(^[^"]*("[^"]*"[^"]*)*[^"]*)\s*\*\s*[0-9]*\s*/) {
			#$line =~ s/\*/x/;
		#} els
		if ($line =~ /\$(\w+)\s*\*\s*[0-9]+\s*/) {
			$line =~ s/\*/x/;
		}
	}
}

foreach my $line (@pythoncode) {
	chomp $line;
	$line =~ s/thisisaflag//;
	$line =~ s/;\s*$//g;
	if ($line =~ /^#!/) {
	
		# translate #! line 
		
		print "#!/usr/bin/perl -w\n";
		#print "\$| =1;\n"; #unbuffer output for testing
	} elsif ($line =~ /^\s*#/ || $line =~ /^\s*$/) {
	
		# Blank & comment lines can be passed unchanged
		
		print "$line\n";
	} elsif ($line =~ /^import/) {

		#imports commented out: phased for deletion

		print "#$line\n";
	} elsif ($line =~ /int\((.*)\)/) {

		#int command unneccsary

		$line =~ s/int\((.*)\)/$1;/;
		print "$line\n";
	} else {	
		# Lines we can't translate are turned into comments
		if ($line =~ /{$/) {
			print "$line\n";
		} elsif ($line =~ /^[}\s]*}$/) {
			print "$line\n";
		} elsif ($line =~ /print\s*(\@\w+)\s*/) {
			#print "#Join? $line\n";
			$line =~ s/(\@\w+)/"[", join\(\"\, \"\, $1), "]"/g;
			print "$line\n";
		} else {
			print "$line;\n";
		}
	}
}


#TODO

# comparison operators: <, <=, >, >=, <>, !=, == (string arguments)
# concatenations operators: + += (string & list arguments)
# : (arrays)
# raw strings (r'')
# re.match, re.search, re.sub
# open() including the optional second parameter (mode).
# functions


#scp python2perl.pl cs2041test.sh input enrollments  cjth726@login.cse.unsw.edu.au:/import/ravel/1/cjth726/:import/ravel/1/cjth726/cs2041/ass1
