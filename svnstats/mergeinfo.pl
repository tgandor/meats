#!/usr/bin/env perl

use strict;
use warnings;

my @revs = ();
my %paths = ();

open(INFO, 'svn pg svn:mergeinfo . |');
while(<INFO>)
{
  chomp;
  my ($path, $merged) = split(':');
  my @morerevs = split(',', $merged);
  for (@morerevs) { $paths{$_} = $path; }
  # print "$path $merged $morerevs[0]\n";
  push (@revs, @morerevs);
}
close(INFO);

# print "Results:\n";
# for(@revs) { print "$_\n"; }

for my $rev (@ARGV) {
  for (@revs) {
    if (/-/) {
      my ($min, $max) = split('-');
      if ($rev >= $min && $rev <= $max) { print "$rev: $paths{$_}\n"; }
    } else {
      if ($rev == $_) { print "$rev: $paths{$_}\n"; }
    } 
  }
}

