#!/usr/bin/perl

package MyParser;
    use base qw(HTML::Parser);

    # we use these three variables to count something
    our ($text_elements, $start_tags, $end_tags);

    # here HTML::text/start/end are overridden 
    sub text	{ $text_elements++  }
    sub start	{ $start_tags++	    }
    sub end	{ $end_tags++	    }

    package main;

    # Test the parser

    my $html = "
    <html>
	<head>
	    <title>Bla</title>
	</head>
	<body>
	Hers the body.
	</body>
    </html> "

    my $parser = MyParser->new;
    $parser->parse( $html );	# parse() is also inherited from HTML::Parser

    print "
    text elements:  $MyParser::text_elements
    start tags   :  $MyParser::start_tags
    end tags     :  $MyParser::end_tags
    "
