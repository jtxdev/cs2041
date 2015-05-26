#1 BLOCKS = 0 | import sys
#1 BLOCKS = 0 | if length($ARGV) != 2:
#1 BLOCKS = 0 |     printf >>STDERR, "Usage: %s <$n>\n", $0
#1 BLOCKS = 1 |     exit 1
#1 BLOCKS = 1 | $n = 0
#2 BLOCKS = 0 | $n = 0
#1 BLOCKS = 0 | $string = '@'
#1 BLOCKS = 0 | while  $n  < int($ARGV[1]):
#1 BLOCKS = 0 |     $string =  $string + $string
#1 BLOCKS = 1 |     $n += 1
#1 BLOCKS = 1 | print "String of 2^%d = %d characters created\$n" % ($n, length($string)), "\n"; 
#2 BLOCKS = 0 | print "String of 2^%d = %d characters created\$n" % ($n, length($string)), "\n"; 
#import sys
if (length($ARGV) != 2) {
    printf >>STDERR, "Usage: %s <$n>\n", $0;
    exit 1;
}
$n = 0;
$string = '@';
while ($n  < int($ARGV[1])) {
    $string =  $string + $string;
    $n += 1;
}
print "String of 2^%d = %d characters created\$n" % ($n, length($string)), "\n";
