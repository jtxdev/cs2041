#!/usr/bin/perl -w

$count = 0;
foreach $i (2..99) {
    $k = $i/2;
    $j = 2;
    foreach $j (2..$k) {
        $k = $i % $j;
        if ($k == 0) {
            $count = $count - 1;
            last;
        }
        $k = $i/2;
    }
    $count = $count + 1;
}
print "$count\n";
