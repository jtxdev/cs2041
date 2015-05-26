#!/usr/bin/perl -w
# Written by andrewt@cse.unsw.edu.au for COMP2041
# run as count_first_names.pl enrollments
# count how many people enrolled have each first name

while ($line = <>) {
    @fields = split /\|/, $line;
    $student_number = $fields[1];
    next if $already_counted{$student_number};
    $already_counted{$student_number} = 1;
    $full_name = $fields[2];
    $full_name =~ /.*,\s+(\S+)/ or next;
    $first_name = $1;
    $fn{$first_name}++;
}

foreach $first_name (sort keys %fn) {
    printf "There are %2d people with the first name $first_name\n", $fn{$first_name};
}

    
