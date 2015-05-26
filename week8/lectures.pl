#!/usr/bin/perl
use warnings;
use strict;

my @lectures;
my %count;
my %table;
my $d = 0;
my $t = 0;
my @daysoftheweek = ("Mon", "Tue", "Wed", "Thu", "Fri");
my @hoursoftheday = ("09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20");
my @tps = ("S1", "S2", "X1");

foreach my $tp (@tps) {
	$table{$tp}{active} = 0;
	foreach my $hour (@hoursoftheday) {
		foreach my $day (@daysoftheweek) {
			$table{$tp}{$day}{$hour} = 0;	
		}
	}
}

foreach my $arg (@ARGV) {
	if ($arg eq "-d") {
        $d = 1;
    } 
    if ($arg eq "-t") {
        $t = 1;
    } else {
		my $lineskip = 7;
		my $lecturetime = "";
		my $teachingperiod = "";
		my $url = "http://www.timetable.unsw.edu.au/current/$arg\.html";
		open F, "wget -q -O- '$url'|" or die;
		while (my $line = <F>) {
			if ($line =~ /\>Lecture.*\<\/a\>\<\/td>/) {
				$lineskip = 0;
			}
			$lineskip++;
			if ($lineskip == 2) {
				$teachingperiod = $line;
				$teachingperiod =~ s/<td class="data"><[^>]*>//;
				$teachingperiod =~ s/<.*//;
				$teachingperiod =~ s/^\s+|\s+$//g;
				$teachingperiod =~ tr/TU/SX/;
				$table{$teachingperiod}{active} = 1;
			} 
			if ($lineskip == 7) {
				$lecturetime = $line;
				$lecturetime =~ s/<td class="data">//;
				$lecturetime =~ s/<.*//;
				$lecturetime =~ s/^\s+|\s+$//g;
				if ($d == 0 && $t == 0) {
					if ($lecturetime ne "") {
						my $lecture = "$arg: $teachingperiod $lecturetime";
						if ($count{$lecture}++ == 0) {
							push (@lectures, $lecture);
						}
					}
				} else {
					if ($lecturetime ne "") {
						my $done = 0;
						my $twoday;
						my $day2;
						while (!$done) {
							$done = 1;
							$twoday = "";
							$day2 = "";
							if ($lecturetime =~ /[A-Z][a-z]{2}, [A-Z][a-z]{2} [0-9]{2}\:[0-9]{2} - [0-9]{2}\:[0-9]{2}/	) {
								$twoday = $&;
								if ($twoday =~ /[A-Z][a-z]{2}/) {
									$day2 = $&;
								}
							}
							if ($lecturetime =~ /[A-Z][a-z]{2} [0-9]{2}\:[0-9]{2} - [0-9]{2}\:[0-9]{2}/	) {
								#print "$lecturetime\n";
								$done = 0;
								my $time = $&;
								my $hour1;
								my $hour2;
								my $day;
								if ($time =~ /[A-Z][a-z]{2}/) {
									$day = $&;
								}
								if ($time =~ /[0-9]{2}/) {
									$hour1 = $&;
									$time =~ s/[0-9]{2}\:[0-9]{2}//;
								}
								if ($time =~ /[0-9]{2}/) {
									$hour2 = $&;
									$time =~ s/[0-9]{2}//;
								}
								if ($time =~ /\:30/) {
									$hour2++;
									$time =~ s/\:30//;
								}
								if ($twoday ne "") {
									my $twohour1 = $hour1;
									my $twohour2 = $hour2;
									while ($twohour1 < $twohour2) {
										if ($t == 1) {
											my $lecture = "$teachingperiod $arg $day2 $twohour1";
											if ($count{$lecture}++ == 0) {
												$table{$teachingperiod}{$day2}{$twohour1}++;
											}
										} else {
											if ($twohour1 =~ /[0][1-9]/) {
												$twohour1 =~ s/0//;
											}
											my $lecture2 = "$teachingperiod $arg $day2 $twohour1";
											if ($count{$lecture2}++ == 0) {
												push (@lectures, $lecture2);
											}
										}
										$twohour1++;
									}
								}
								while ($hour1 < $hour2) {
									if ($t == 1) {
										my $lecture = "$teachingperiod $arg $day $hour1";
										if ($count{$lecture}++ == 0) {
											$table{$teachingperiod}{$day}{$hour1}++;
										}
									} else {
										if ($hour1 =~ /[0][1-9]/) {
											$hour1 =~ s/0//;
										}
										my $lecture = "$teachingperiod $arg $day $hour1";
										if ($count{$lecture}++ == 0) {
											push (@lectures, $lecture);
										}
									}
									$hour1++;
								}
							$lecturetime =~ s/[A-Z][a-z]{2} [0-9]{2}\:[0-9]{2} - [0-9]{2}\:[0-9]{2}//;
							}
						}
					}
				}
			}
		}
	}
}
if ($t == 0 ) {
	foreach my $arg (@lectures) {
		$arg =~ s/^\s+|\s+$//g;
	    print "$arg\n";
	}
} else {
	foreach my $tp (@tps) {
		if ($table{$tp}{active} == 1) {
			print "$tp       Mon   Tue   Wed   Thu   Fri\n";
			foreach my $hour (@hoursoftheday) {
				print "$hour:00     "; 

				foreach my $day (@daysoftheweek) {
					if ($table{$tp}{$day}{$hour} > 0) {
						print "$table{$tp}{$day}{$hour}     ";
					} else {
						print "      ";
					}
				}
				print "\n";
			}
		}
	}
}

