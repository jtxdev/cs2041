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
my %seentypes;
my @vars;
my @arrs;
my @hashes;
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
		if ($line =~ /print\s*"((?:[^'"\\]|\\.)*)"\s*$/) {
		
			# handles "" strings
		
			$line =~ s/print\s*"((?:[^'"\\]|\\.)*)"\s*$/print \"$1\\n\"/;
		} elsif ($line =~ /\s*print\s*(.*)"(.*)"\s*%\s*(.*)\s*$/) {
			$line =~ s/print\s*(.*)"((?:[^'"\\]|\\.)*)"\s*%\s*(.*)\s*$/printf $1\"$2\\n\", $3/;
			$line =~ s/\\n\\n/\\n/
		} elsif ($line =~ /\s*print\s*([^;]*);/) { 
			# handles print within one liners

			$line =~ s/print\s*([^;]*);/print $1, \"\\n\"; /;
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
		$oldjoin =~ /\((.*)\)/;
		$newjoin = "join(\"$delim\", $1)";
		$line =~ /(.*)['"](.)['"]\.join/;
		$line = "$1$newjoin$oldremainder";


	}
	# handles sys functions
	if ($line =~ /sys\./) {

		$handled = 0;

		#handles sys.argv

		$handled += $line =~ s/sys.argv/ARGV/;

			# handles sys.stout.write()
		$handled += $line =~ s/sys.exit\(1\)/exit 1/;
			
		$handled += $line =~ s/sys\.stdout\.write\((.*)\)\s*$/print $1/;


			# handles sys.stdin.readline()

		$handled +=	$line =~ s/sys\.stdin\.readline\(\)/<STDIN>/;


			# handles sys.stdin.readlines()

			if ($line =~ /\b(\w+)\b\s*=\s*sys\.stdin\.readlines\(\)/) {
				my $array = $1;
				$line =~ s/$array/\@$array/;
				$handled +=	$line =~ s/sys\.stdin\.readlines\(\)/<STDIN>/;
			}

			# handles sys.stdin

			$handled +=$line =~ s/sys\.stdin/<STDIN>/;
			$handled +=$line =~ s/\bsys\.stderr\b/STDERR/;
			$handled +=$line =~ s/>>STDERR/STDERR/;

			
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

		if ($line =~ /^\s*\b(\w+)\b\s*=\s*["'](.*)["']/) {
			$seentypes{$1} = 1;
		} elsif ($line =~ /^\s*\b(\w+)\b\s*=\s*[0-9]+\s*[^x]*/) {
			$seentypes{$1} = 2;
		}


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
		$line =~ s/\bfor\b/foreach/;

	}

	# handles break 
	
		$line =~ s/\bbreak\b/last/;
		$line =~ s/\bcontinue\b/next/;
}

# second loop:
	# converts variables to perl syntax

foreach my $line (@pythoncode) {
	if ($line !~ /^#/) {
		foreach my $var (@vars) {

			# converts all instances of var

			$line =~ s/\b$var\b/\$$var/g;

			# if var is between "s or 's --> unscalar

			$line =~ s/(^[^"]*"(?:[^"\\]|\\.)*("(?:[^"\\]|\\.)*"[^"]*)*[^"]*)\$$var\b/$1$var/;
			$line =~ s/(^[^']*'(?:[^'\\]|\\.)*('(?:[^'\\]|\\.)*'[^']*)*[^']*)\$$var\b/$1$var/;
		}
		foreach my $arr (@arrs) {

			#converts all non converted instances of arr
			if ($line !~ /\@$arr/) {
				$line =~ s/\b$arr\b/\@$arr/g;
			}

			# if arr is between "s or 's --> unarray

			$line =~ s/(^[^"]*"(?:[^"\\]|\\.)*("(?:[^"\\]|\\.)*"[^"]*)*[^"]*)\@$arr\b/$1$arr/;
			$line =~ s/(^[^']*'(?:[^'\\]|\\.)*('(?:[^'\\]|\\.)*'[^']*)*[^']*)\@$arr\b/$1$arr/;
			
		}
		foreach my $hash (@hashes) {

			$line =~ s/\b$hash\b/\%$hash/g;

			# if arr is between "s or 's --> unhash

			$line =~ s/(^[^"]*"(?:[^"\\]|\\.)*("(?:[^"\\]|\\.)*"[^"]*)*[^"]*)\%$hash\b/$1$hash/;
			$line =~ s/(^[^']*'(?:[^'\\]|\\.)*('(?:[^'\\]|\\.)*'[^']*)*[^']*)\%$hash\b/$1$hash/;
		}
	}
}

#third loop:
	# fixes perl type specific problems eg. length -> scalar if @ or %.

foreach my $line (@pythoncode) {

		# converts len function 

	if ($line =~ /\blen\(\@(\w+)\)/) {
		$line =~ s/len/scalar/;
	} else {
		$line =~ s/\blen\b/length/;
	}

		# converts rest of argv

	if ($line =~ /range(.*)\s*/) {

		my $range = $1;
		my $oldrange;
		my $newrange;

	# converts range functions to perl syntax eg. range(1, 3) -> (1..2)


		#extract balanced bracket after range

		my @result = extract_bracketed( $range, '()' );

		$oldrange = $result[0];

		if ($oldrange =~ /,/) {
			$oldrange =~ /\((.*),\s*(.*)\)/;
			$newrange = "$1..$2 - 1";
			$line =~ /(.*)range/;
			$line = "$1$newrange\):";
		} else {
			# single argument range
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
		$oldappend =~ /\((.*)\)/;
		$newappend = "push(\@$list, $1)";
		$line =~ /(.*)\@(.*)\.append(.*)\s*/;
		$line = "$1$newappend$oldremainder";

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
		$oldpop =~ /\((.*)\)/;
		$offset = $1;
		if ($offset eq "") {
			$newpop = "splice(\@$list, -1, 1)";
		} else {
			$newpop = "splice(\@$list, $offset, 1)";
		}
		$line =~ /(.*)\@(.*)\.pop(.*)\s*/;
		$line = "$1$newpop$oldremainder";
	}

		# converts ascessing array

	$line =~ s/\@(\w+)\[/\$$1\[/;

	# converts .group[]
	if ($line =~ /group/) {
		my $groupindex;
		my @matches;
		@matches = $line =~ /(\$\w+\.group\(([^)]*)\))/g;
		foreach my $match (@matches) {
			$match =~ /\$\w+\.group\(([^)]*)\)/;
			if ($1 ne "") {
				$groupindex = $1 + 1;
				$line =~ s/\$\w+\.group\($1\)/\$$groupindex/g;
			} else {
				$line =~ s/\$(\w+)\.group\(([^)]*)\)/\$$1/g;
			}
		}
	}

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
		$line =~ s/\%((\w+)(\{\$\w+\})+)/\$$1/g;
	}
	$line =~ s/(?<=keys )(\$(\w+)(\{(\$\w+)\})+)/\%\{$1\}/;

	if ($line =~ /\bARGV\b/) {
		$line =~ s/\bARGV/\$ARGV/;	
		print "#1line $line\n";
		$line =~ s/\bARGV\[([0-9]*)\]/\$ARGV[$1-1]/;
		print "#2line $line\n";
		$line =~ s/\$ARGV\[1:\]/\@ARGV/;
		print "#3line $line\n";
		$line =~ s/1\.\.length\(\@ARGV\)/0\.\.\@ARGV/;
		print "#4line $line\n";
		$line =~ s/\$ARGV\[0-1\]/\$0/;
		print "#5line $line\n";
		$line =~ s/length\(\@ARGV\)\s*(<|<=|>|>=|<>|!=|==)\s*([0-9]*)/scalar\(\@ARGV\) $1 $2 - 1/;
 	}

}



# fourth loop: 
	# Expanding loops and blocks

my $blocks = 0;
my $closeblocks = 0;
my $previndent = 0;
my $currindent = 0;
my @blockstack;
my $do;
my $linecount = 0;
foreach my $line (@pythoncode) {
	$linecount++;
	my $dedent = 0;
	chomp $line;
	$line =~ /^(\s*)/;
	my $indent = $1;
	my $currindent = length($indent);
	#check if indent <>;
	#print "#1 BLOCKS = $blocks | $line\n";
	if (length($indent) > $previndent) {

		# push previous indent on stack, increment blockcount

		push (@blockstack, $previndent);
		$previndent = length($indent);
		$blocks++;

	} elsif (length($indent) < $previndent) {

		# pop stack until indents match, decrement blockcount and count pops

		$closeblocks = 0;
		$dedent = 1;
		my $top = pop @blockstack;

		$blocks--;
		$closeblocks++;
 
		while ($top != length($indent) and $top != 0) {
			if (scalar(@blockstack) > 0) {

				$top = pop @blockstack;
				$blocks--;
				$closeblocks++;
			}
		}
		$previndent = $top;
	}
	my $newindent = "    " x $blocks;
	my $closingindent = "    " x $closeblocks;
	if ($dedent == 0) {

		# If not dedenting
		if ($line =~ /^\s{$previndent}[^ ]?.*\b(if|for|foreach|while)\b\s*(.*):\s*(.*)/) {
   			# converts to perl syntax eg. for x < 0: ---> while ($x < 0) {
			chomp $1;
			chomp $2;
			chomp $3;
			$do = $3;
			if ($do ne "") {
				$line =~ s/\b(if|while|else|elsif)\b\s*(.*):\s*(.*)/$1 ($2) {\n\t$3;\n}/;
				$line =~ s/\b(for|foreach)\b\s*(.*):\s*(.*)/$1 $2 {\n\t$3;\n}/;
			} else {
				$line =~ s/\b(if|while|else|elsif)\b\s*(.*):\s*(.*)/$1 ($2) {/;
				$line =~ s/\b(for|foreach)\b\s*(.*):\s*(.*)/$1 $2 {/;
			}
		}
		if ($linecount == ($#pythoncode + 1) and $blocks > 0) {

			# eof reached, close all open {'s

			chomp $line;
			my $str = ""; 
			foreach (0..$blocks - 1) {
				my $eofindent = "    " x --$blocks; 
				$str = "$str$eofindent}\n";
			}
			$line = "$line;\n$str";
		}
		$line =~ s/^\s{$previndent}(?!=\s)/$newindent/;
	} elsif ($dedent == 1) {

		# If dedenting
		if ($line =~ /^\s{$previndent}[^ ]?.*\b(if|for|foreach|while|else|elsif)\b\s*(.*):\s*(.*)/) {
		# if first line unindented is another if for else etc.

			$do = $3;
			if ($do ne "") {
				# for one liners eg if x: {a; b; c;}

				$line =~ s/\b(if|while|else|elsif)\b\s*(.*):\s*(.*)/}\n$1 ($2) {\n\t$3;\n}/;
				$line =~ s/\b(for|foreach)\b\s*(.*):\s*(.*)/}\n$1 $2 {\n\t$3;\n}/;
			} else {
					#apply correct closing bracket and indentation according to keyword
				if ($closeblocks > 0) {

					# closing popped dedents

					my $count = 0;
					my $count2;
					my $str = "$newindent";
					my $tab = "    ";
					while ($count < $closeblocks) {
						$count2 = $count;
						while ($count2 < $closeblocks - 1) {
							$str = "$str$tab";
							$count2++;
						}
						$str = "$str}\n$newindent";
						$count++;
					}
					chomp $str;
					$line = "$str$line";
				}

				if ($1 eq "else") {
					$line =~ s/\s*\b(else)\b\s*(.*):\s*(.*)/ $1 {/;
				} elsif ($1 eq "elsif") {
					$line =~ s/\s*\b(elsif)\b\s*(.*):\s*(.*)/ $1 ($2) {/;	
				} else {
					$line =~ s/\b(if|while)\b\s*(.*):\s*(.*)/\n$newindent$1 ($2) {/;
					$line =~ s/\b(for|foreach)\b\s*(.*):\s*(.*)/\n$newindent$1 $2 {/;
				}
			}
		} elsif ($closeblocks > 0) {

			# closing popped dedents

			my $count = 0;
			my $count2;
			my $str = "$newindent";
			my $tab = "    ";
			while ($count < $closeblocks) {
				$count2 = $count;
				while ($count2 < $closeblocks - 1) {
					$str = "$str$tab";
					$count2++;
				}
				$str = "$str}\n";
				$count++;
			}
			$line = "$str$line";
		}
	$line =~ s/^\s{$previndent}(?!=\s)/$newindent/;
	}
}

# String loop
foreach my $line (@pythoncode) {
	chomp $line;
	if ($line =~ /\+/) {

		#converts if arguments are strings

		if ($line =~ /['"](?:[^'"\\]|\\.)*['"]\s*\+\s*['"](?:[^"\\]|\\.)*['"]/) {
			$line =~ s/(['"](?:[^'"\\]|\\.)*['"]\s*)\+(\s*['"](?:[^"\\]|\\.)*['"])/$1\.$2/;
		} 
		#(^[^"]*("[^"]*"[^"]*)*)
		if ($line =~ /['"](?:[^'"\\]|\\.)*['"]\s*\+\s*\$(\w+)\s*/) {
			if ($seentypes{$1} == 1) {
				$line =~ s/(['"](?:[^'"\\]|\\.)*['"]\s*)\+(\s*\$(\w+)\s*)/$1\.$2/;
			}
		}
		if ($line =~ /\$(\w+)\s*\+\s*['"](?:[^"\\]|\\.)*['"]\s*/) {
			if ($seentypes{$1} == 1) {
				$line =~ s/(\$(\w+)\s*)\+(\s*['"](?:[^"\\]|\\.)*['"]\s*)/$1\.$3/;
			}
		}
		if ($line =~ /\$(\w+)\s*\+\s*\$(\w+)\s*/) {
			if ($seentypes{$1} == 1 and $seentypes{$2} == 1) {
				$line =~ s/(\$(\w+)\s*)\+(\s*\$(\w+)\s*)/$1\.$3/;
			}
		}
	}
	if ($line =~ /\*/) {

		#converts if one argument is a string and one argument is a number

		if ($line =~ /\$(\w+)\s*\*\s*[0-9]+\s*/) {
			if ($seentypes{$1} == 1) {
				$line =~ s/(\$(\w+)\s*)\*(\s*[0-9]+\s*)/$1x$3/;
			}
		}
		if ($line =~ /['"](?:[^'"\\]|\\.)*['"]\s*\*\s*[0-9]+\s*/) {
			$line =~ s/(['"](?:[^'"\\]|\\.)*['"]\s*)\*(\s*[0-9]+\s*)/$1x$2/;
		}
		if ($line =~ /['"](?:[^'"\\]|\\.)*['"]\s*\*\s*\$(\w+)\s*/) {
			if ($seentypes{$1} == 2) {
				$line =~ s/(['"](?:[^'"\\]|\\.)*['"]\s*)\*(\s*\$(\w+)\s*)/$1x$2/;
			}
		}
		if ($line =~ /\$(\w+)\s*\+\s*['"](?:[^"\\]|\\.)*['"]\s*/) {
			if ($seentypes{$1} == 1) {
				$line =~ s/(\$(\w+)\s*)\*(\s*['"](?:[^"\\]|\\.)*['"]\s*)/$1x$3/;
			}
		}
		if ($line =~ /\$(\w+)\s*\*\s*\$(\w+)\s*/) {
			if ($seentypes{$1} != $seentypes{$2}) {
				$line =~ s/(\$(\w+)\s*)\*(\s*\$(\w+)\s*)/$1x$3/;
			}
		}
	}
	if ($line =~ /\$\w+\s*(?:<|<=|>|>=|<>|!=|==)\s*\$\w+\s*/) {

		#converts if arguments are of form: string scalar op string scalar

		my @matches;
		@matches = $line =~ /(\$\w+\s*(?:<|<=|>|>=|<>|!=|==)\s*\$\w+\s*)/g;
		foreach my $match (@matches) {
			$match =~ /\$(\w+)\s*(?:<|<=|>|>=|<>|!=|==)\s*\$(\w+)\s*/;
			if ($seentypes{$1} == 1 and $seentypes{$2} == 1) {

				$line =~ s/(\$\w+\s*)\<(\s*\$\w+\s*)/$1lt$2/;
				$line =~ s/(\$\w+\s*)\<\=(\s*\$\w+\s*)/$1le$2/;
				$line =~ s/(\$\w+\s*)\>(\s*\$\w+\s*)/$1gt$2/;
				$line =~ s/(\$\w+\s*)\>\=(\s*\$\w+\s*)/$1ge$2/;
				$line =~ s/(\$\w+\s*)(?:<>|!=)(\s*\$\w+\s*)/$1ne$2/;
				$line =~ s/(\$\w+\s*)\=\=(\s*\$\w+\s*)/$1eq$2/;
			}
		}
	}

	if ($line =~ /['"](?:[^'"\\]|\\.)*['"]\s*(?:<|<=|>|>=|<>|!=|==)\s*['"](?:[^'"\\]|\\.)*['"]\s*/) {

		#converts if arguments are of form: stringliteral op stringliteral

		my @matches;
		@matches = $line =~ /(['"](?:[^'"\\]|\\.)*['"]\s*(?:<|<=|>|>=|<>|!=|==)\s*['"](?:[^'"\\]|\\.)*['"]\s*)/g;
		foreach my $match (@matches) {

				$line =~ s/(['"](?:[^'"\\]|\\.)*['"]\s*)\<(\s*['"](?:[^'"\\]|\\.)*['"]\s*)/$1lt$2/;
				$line =~ s/(['"](?:[^'"\\]|\\.)*['"]\s*)\<\=(\s*['"](?:[^'"\\]|\\.)*['"]\s*)/$1le$2/;
				$line =~ s/(['"](?:[^'"\\]|\\.)*['"]\s*)\>(\s*['"](?:[^'"\\]|\\.)*['"]\s*)/$1gt$2/;
				$line =~ s/(['"](?:[^'"\\]|\\.)*['"]\s*)\>\=(\s*['"](?:[^'"\\]|\\.)*['"]\s*)/$1ge$2/;
				$line =~ s/(['"](?:[^'"\\]|\\.)*['"]\s*)(?:<>|!=)(\s*['"](?:[^'"\\]|\\.)*['"]\s*)/$1ne$2/;
				$line =~ s/(['"](?:[^'"\\]|\\.)*['"]\s*)\=\=(\s*['"](?:[^'"\\]|\\.)*['"]\s*)/$1eq$2/;
		}
	}

	if ($line =~ /\$\w+\s*(?:<|<=|>|>=|<>|!=|==)\s*['"](?:[^'"\\]|\\.)*['"]\s*/) {
		
		#converts if arguments are of form: string scalar op stringliteral

		my @matches;
		@matches = $line =~ /(\$\w+\s*(?:<|<=|>|>=|<>|!=|==)\s*['"](?:[^'"\\]|\\.)*['"]\s*)/g;
		foreach my $match (@matches) {
			$match =~ /\$(\w+)\s*(?:<|<=|>|>=|<>|!=|==)\s*['"](?:[^'"\\]|\\.)*['"]\s*/;
			if ($seentypes{$1} == 1) {


				$line =~ s/(\$\w+\s*)\<(\s*['"](?:[^'"\\]|\\.)*['"]\s*)/$1lt$2/;
				$line =~ s/(\$\w+\s*)\<\=(\s*['"](?:[^'"\\]|\\.)*['"]\s*)/$1le$2/;
				$line =~ s/(\$\w+\s*)\>(\s*['"](?:[^'"\\]|\\.)*['"]\s*)/$1gt$2/;
				$line =~ s/(\$\w+\s*)\>\=(\s*['"](?:[^'"\\]|\\.)*['"]\s*)/$1ge$2/;
				$line =~ s/(\$\w+\s*)(?:<>|!=)(\s*['"](?:[^'"\\]|\\.)*['"]\s*)/$1ne$2/;
				$line =~ s/(\$\w+\s*)\=\=(\s*['"](?:[^'"\\]|\\.)*['"]\s*)/$1eq$2/;
			}
		}
	}

	if ($line =~ /['"](?:[^'"\\]|\\.)*['"]\s*(?:<|<=|>|>=|<>|!=|==)\s*\$\w+\s*/) {

		#converts if arguments are of form: string scalar op string scalar

		my @matches;
		@matches = $line =~ /(['"](?:[^'"\\]|\\.)*['"]\s*(?:<|<=|>|>=|<>|!=|==)\s*\$\w+\s*)/g;
		foreach my $match (@matches) {
			$match =~ /['"](?:[^'"\\]|\\.)*['"]\s*(?:<|<=|>|>=|<>|!=|==)\s*\$(\w+)\s*/;
			if ($seentypes{$1} == 1) {

				$line =~ s/(['"](?:[^'"\\]|\\.)*['"]\s*)\<(\s*\$\w+\s*)/$1lt$2/;
				$line =~ s/(['"](?:[^'"\\]|\\.)*['"]\s*)\<\=(\s*\$\w+\s*)/$1le$2/;
				$line =~ s/(['"](?:[^'"\\]|\\.)*['"]\s*)\>(\s*\$\w+\s*)/$1gt$2/;
				$line =~ s/(['"](?:[^'"\\]|\\.)*['"]\s*)\>\=(\s*\$\w+\s*)/$1ge$2/;
				$line =~ s/(['"](?:[^'"\\]|\\.)*['"]\s*)(?:<>|!=)(\s*\$\w+\s*)/$1ne$2/;
				$line =~ s/(['"](?:[^'"\\]|\\.)*['"]\s*)\=\=(\s*\$\w+\s*)/$1eq$2/;
			}
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
	} elsif ($line =~ /^\s*#/ || $line =~ /^\s*$/) {
	
		# Blank & comment lines can be passed unchanged
		
		print "$line\n";
	} elsif ($line =~ /^import/) {

		#imports commented out: phased for deletion

		print "#$line\n";
	#} elsif ($line =~ /int\((.*)\)/) {

		#int command unneccsary

		#$line =~ s/int\((.*)\)/$1/;
		#print "$line;\n";
	} elsif ($line =~ /STDERR/) {
		$line =~ s/STDERR,/STDERR/;
		print "$line;\n";
	} else {	
		# Lines we can't translate are turned into comments
		if ($line =~ /{$/) {
			print "$line\n";
		} elsif ($line =~ /^[}\s]*}$/) {
			print "$line\n";
		} elsif ($line =~ /print\s*(\@\w+)\s*/) {
			$line =~ s/(\@\w+)/"[", join\(\"\, \"\, $1), "]"/g;
			print "$line\n";
		} else {
			print "$line;\n";
		}
	}
}



#TODO

# : (arrays)
# raw strings (r'')
# open() optional second parameter (mode).
# functions


#scp python2perl.pl cs2041test.sh input enrollments  cjth726@login.cse.unsw.edu.au:/import/ravel/1/cjth726/:import/ravel/1/cjth726/cs2041/ass1
