" For extensive Informations on integrating Python in Vim(Script) see
" http://vimdoc.sourceforge.net/htmldoc/if_pyth.html
" https://devhints.io/vimscript
"
if !has('python3')
	finish
else
	echo 'Found python3'
endif

" 'Global' imports
python3 import sys
python3 import os

python3 sys.path.append(os.getcwd())
python3 import vexpansion

python3 vexpansion.start_server()

" Functions
" Adds a HTML-Tag after the current line
function! HTMLTag(name,...)
	if len(a:000) > 0
		" Number of additional \t given
		python3 vexpansion.html_tag(vim.eval("a:name"), vim.eval("a:1"))
	else
		" No number of additional \t given, use 0
		python3 vexpansion.html_tag(vim.eval("a:name"), 0)
	endif 
endfunc

" Insert a file specified by a url into the buffer
function! Insert_File(url)
	python3 vexpansion.insert_file(vim.eval("a:url"))
endfunc

" Custom autocomplete function
function! Autocomplete_Special(findstart, base)
	" This function is later bound to a vim command. For this it has to have 
	" two argument. For the further specifications look here:
	" http://vimdoc.sourceforge.net/htmldoc/insert.html#complete-functions
	if (a:findstart == 1)
		" Determine beginning of the word to be completed
		python3 vexpansion.startOfWord()
		return result
	else
		python3 vexpansion.getSuggestion(vim.eval("a:base"))
		" let x = ["Holger", "Zweiback", "Nervmichnicht"]
	
		return x
	endif
endfunc

" Set shortcuts for vim
" nargs is the number of arguments
command! -nargs=+ Tag call HTMLTag(<args>) " This can be called by :Tag <tagname>
command! -nargs=0 HTMLDoc call Insert_File("files/html_template.html") "

set completeopt=menuone,noselect,noinsert
set completefunc=Autocomplete_Special
imap <F5> <Esc>:echo "haha"<CR>
