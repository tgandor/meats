#!/usr/bin/perl

$comm = "sudo apt-get install --install-recommends";

while(<DATA>) {
    chomp;
    $comm .= " $_";
}

print "$comm\n";
system($comm);

__DATA__

vim emacs 
eclipse 
kile texlive-lang-polish texlive-doc-pl
texlive-fonts-extra
ttf-mscorefonts-installer

mc kdf aptitude kdesdk-scripts
p7zip-full p7zip-rar unrar rar
openvpn openssh-server
numlockx

subversion mercurial git-core

idle python-numpy python-scipy python-matplotlib python-mpi
python-matplotlib-doc python-doc python-docutils
python-argparse python-argparse-doc

jython jython-doc
clisp clisp-doc
perl-doc

mpich2 mpich2-doc mpichpython

octave3.2 gnuplot qtoctave
gnuplot-doc

mplayer mencoder
dvdrip dvdrip-doc

chromium-browser 
gimp inkscape
audacity
kteatime

wine

gnubik childsplay chromium-bsu tuxmath tuxpaint tuxtype
lletters 


