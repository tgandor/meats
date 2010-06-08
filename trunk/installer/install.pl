use strict;
use Config;
use File::Copy;
use File::Basename;
use File::Find;

$\ = "\n";

print "Scanning executable paths...";

for(split $Config::Config{path_sep}, $ENV{PATH} ) {
    print if -w $_;
    print "Read Only: $_" if ! -w $_;
}


__END__

print __FILE__;
print dirname(__FILE__);

sub wyp {
  print if /.c/;
}

find(\&wyp, "..");

