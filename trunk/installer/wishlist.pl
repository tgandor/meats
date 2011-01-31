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

mc kdf aptitude kdesdk-scripts

numlockx

subversion mercurial git-core

idle python-numpy python-scipy python-matplotlib python-mpi
python-argparse 
python-numpy-doc python-argparse-doc python-matplotlib-doc
python-doc

eclipse 

mplayer mencoder

p7zip-full p7zip-rar unrar rar

perl-doc doxygen doxygen-doc doxygen-gui graphviz

openvpn openssh-server

ttf-mscorefonts-installer

dvdrip dvdrip-doc

octave3.2

gimp inkscape
