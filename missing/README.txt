
This tool has two versions - one written more cleanly "sorth" and a file,
which contains a one-liner (yes, Python also allows for one liners, but -
as you'll see - they are longer and more complicated then in Perl).

The one liner is sometimes a nice thing to keep in commandline history,
and does not need writing files to any executable path.

A typical use case of these tools would be to sort the output of du(1)
with human-readable sizes, ie. -h or --human-readable :

$ du -h | sorth

or

$ du -h | python -c 'import sys, re; tok = lambda x: re.search("^([0-9.,]+)([KMG]?)", x); cl = lambda x: float(x.replace(",",".")); sys.stdout.write("".join(sorted(sys.stdin.readlines(), key = lambda x: (cl(tok(x).group(1)) * {"K":2**10,"M":2**20,"G":2**30}[tok(x).group(2)] if len(tok(x).group(2)) else cl(tok(x).group(1)) ) if tok(x) else 0.0 ) ) )'


