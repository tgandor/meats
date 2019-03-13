" let _curfile = expand("%:t")
" if _curfile =~ "Makefile" || _curfile =~ "makefile" || _curfile =~ ".*\.mk"
"     set noexpandtab
" else
"     set expandtab
" endif

au FileType make setl noexpandtab
au FileType python setl kp=pydoc

set autoindent
set expandtab
set laststatus=2
set list
set listchars=tab:>-,trail:.
set modeline
set ruler
set shiftwidth=4
set smartindent
set tabstop=4

syn on
