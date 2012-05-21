#!/usr/bin/env perl

use strict;
use warnings;

die("Usage:  <username>\n") if $#ARGV == -1;
my $user = $ARGV[0];
my $print = 0;

while(<STDIN>)
{
	if (/^r[1-9]/) { 
		my @data = split(/\s+/);
		$print = 1 if ($data[2] eq $user);
	}
	if ($print) 
	{
		print;
		$print = 0 if (/^---/);
	}
}
# print @ARGV;

