#!/usr/bin/perl -w

$number = 0;
while ($number >= 0) {
    print "> ";
    $number = <STDIN>;
    if ($number >= 0) {
        if ($number % 2 == 0) {
            print  "Even\n";
        } else {
            print "Odd\n";
        }
    }
}
print "Bye\n";
