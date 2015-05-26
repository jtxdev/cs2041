#!/usr/bin/perl -w

foreach $arg (@ARGV) {
	push @files, $arg;
}
foreach $f (@files) {
	open(F,"<$f") or die "$0: Can't open $f: $!\n";
	@line = <F>;
	chomp(@line);
	$string="";
	$space="	";
	for ($line_number = 0; $line_number < $#line + 1; $line_number++) {
		if ($string ne "") {
			$string = $string.$space;
		}
		$string = $string.($line[$line_number]);
	}
	print "$string\n";
}