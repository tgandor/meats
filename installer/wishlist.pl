#!/usr/bin/perl

$comm = "sudo apt-get install --install-recommends";

while(<DATA>) {
    chomp;
    $comm .= " $_";
}

print "$comm\n";
system($comm);

$others = "
php5 
php-pear  
youtube-dl
";

__DATA__

vim clisp emacs 

mc kdf 

numlockx

subversion mercurial git-core

idle python-numpy python-scipy python-matplotlib python-mpi

eclipse 

mplayer mencoder

p7zip-full p7zip-rar unrar rar

perl-doc

openvpn openssh-server

ttf-mscorefonts-installer

dvdrip dvdrip-doc

octave3.2

gimp inkscape
