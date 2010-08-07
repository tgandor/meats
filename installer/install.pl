use strict;
use Config;
use File::Copy;
use File::Basename;
use File::Find;

$\ = "\n";


sub get_bin {
  print "Scanning executable paths...";
  for(split $Config::Config{path_sep}, $ENV{PATH} ) {
      return $_ if -w $_;
      print "Read Only: $_" if ! -w $_;
  }
}

my $bindir = &get_bin;
print "Taret directory is: $bindir";

my @installs = qw(
../otofotki/otofotki.sh
../unwinzip/unwinzip.pl
);

map { print; copy($_, $bindir); chmod 0755, "$bindir/$_"; } @installs;

__END__

print __FILE__;
print dirname(__FILE__);

sub wyp {
  print if /.c/;
}

find(\&wyp, "..");

