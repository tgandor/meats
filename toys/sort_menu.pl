#!/usr/bin/env perl

print sort { 
($x = $a) =~ s/.*\(([\d\.]+) z.*/$1/;
($y = $b) =~ s/.*\(([\d\.]+) z.*/$1/; 
return $x <=> $y;
} <>;

