#!/usr/bin/perl

for my $f (@ARGV)  {
  open(LIST, "unzip -l $f |");
  
  my $state = 0;
  while(<LIST>) {
    ++$state and next if /^----/;
    next if $state != 1;
    #$_ = substr($_, 30, -1);

    my @F = split;
    splice(@F, 0, 3);
    $_ = join(' ', @F);

    my $oryg = $_;
    s/\?/_/g;
    print "$oryg > $_\n";
    if(/\/$/) {
      system "mkdir -p \"$_\"";
    } else {
      system "unzip -p $f \"$oryg\" > \"$_\"";
    }
  }
}
