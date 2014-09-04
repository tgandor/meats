#!/usr/bin/env perl

use strict;
use warnings;

die("Usage:  <string to find>\n") if $#ARGV == -1;
my $search = $ARGV[0];
my $print = 1; # for logs starting with "--------...-------" anyway
my @data = ();
while(<STDIN>)
{
	if (/$search/) {
		$print = 1;
	}
	push (@data, $_);
	if (/^---/)
	{
		if ($print)
		{
			print @data;
		}
		@data = ();
		$print = 0;
	}
}
# print @ARGV;

