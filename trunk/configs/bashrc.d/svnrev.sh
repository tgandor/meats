# source this from your .bashrc or the like

function svnrev {
  if which colordiff; then
	  (svn log -v -r $1; svn diff -r`expr $1 - 1`:$1) | colordiff | less -r
  else 
	  (svn log -v -r $1; svn diff -r`expr $1 - 1`:$1) | less
  fi
}
