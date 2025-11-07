# Append to the history file, don't overwrite it on shell exit
shopt -s histappend

# Keep a large in-memory history (number of commands remembered in the current shell)
HISTSIZE=100000

# Keep a large on-disk history (max lines in ~/.bash_history)
HISTFILESIZE=200000

# Before each prompt:
#  - history -a : append new commands from this session to the history file
#  - history -n : read new lines from the history file (sync across terminals)
PROMPT_COMMAND='history -a; history -n'

# History behavior:
#  - ignoredups : don't record a command if it's the same as the previous one
#  - erasedups  : when a command is re-entered, remove its older duplicates
HISTCONTROL=ignoredups:erasedups

# Show timestamps when running `history` (YYYY-MM-DD HH:MM:SS)
HISTTIMEFORMAT="%F %T "

# Don't ignore any commands (empty means no patterns are excluded)
HISTIGNORE=""
