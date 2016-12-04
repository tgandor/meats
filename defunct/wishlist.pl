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

mc kdf aptitude apt-rdepends kdesdk-scripts fdupes kdirstat
p7zip-full p7zip-rar unrar rar
openvpn openssh-server
numlockx cpufrequtils

subversion mercurial git-core cvsnt

idle python-numpy python-scipy python-matplotlib python-mpi
python-matplotlib-doc python-doc python-docutils
python-argparse python-argparse-doc
python-profiler pylint graphviz
python-codespeak-lib
python-pyrex pyrex-mode
python-dialog
swig swig-doc cableswig python-dev
doxygen doxygen-doc doxygen-gui
indent

jython jython-doc
clisp clisp-doc
perl-doc

mpich2 mpich2-doc mpichpython

qt4-dev-tools qt4-designer qt4-doc-html
pyqt4-dev-tools

octave3.2 gnuplot qtoctave ipython
gnuplot-doc

mplayer mencoder vlc
dvdrip dvdrip-doc

chromium-browser 
gimp inkscape simple-scan xsane
audacity
kteatime

wine

gnubik childsplay chromium-bsu tuxmath tuxpaint tuxtype
lletters kdegames

