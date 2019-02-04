AUTOMAKE_OPTIONS = gnu
bin_PROGRAMS = pvicig
EXTRA_PROGRAMS = getatoms

pvicig_SOURCES = main.c preprocess.c trim_directives.c astring.c \
				 asprintf.c atomizer_c.l atomizer_pascal.l atomizer_banal.l \
				 unique_dictionary.c atom.c comparison.c program.c GST.c \
				 atom_codes.c

getatoms_SOURCES = atom_extractor.l unique_dictionary.c

noinst_HEADERS = main.h trim_directives.h atom_codes.h unique_dictionary.h \
				 preprocess.h astring.h atom.h comparison.h program.h GST.h \
				 metrics.h compat.h

EXTRA_DIST = examples locale install_locale

POTFILES = main.c program.c

AM_CFLAGS = -g

atom_codes.h        : getatoms atomizer_c.c atomizer_pascal.c atomizer_banal.c
	./getatoms -H atom_codes.h -C atom_codes.c atomizer_c.c atomizer_pascal.c atomizer_banal.c
atom_codes.o        : atom_codes.h

# A parser and lexer of BANAL programming language
# Analizatory jêzyka BANAL (mojego autorstwa)
atomizer_banal.c : atomizer_banal.l
	$(LEX) -Patban -oatomizer_banal.c atomizer_banal.l
atomizer_banal.o : atom_codes.h

# ISO C scanner & parser, and some auxiliary functions
# Analizatory jêzyka C oraz kilka narzêdzi pomocniczych
atomizer_c.c      : atomizer_c.l
	$(LEX) -Patc -oatomizer_c.c atomizer_c.l
atomizer_c.o      : atom_codes.h
preprocess.o      : preprocess.h
trim_directives.o : trim_directives.h

# Pascal scanner & parser
# Analizatory jêzyka Pascal
atomizer_pascal.c : atomizer_pascal.l
	$(LEX) -i -Patpas -oatomizer_pascal.c atomizer_pascal.l
atomizer_pascal.o      : atom_codes.h

install: install-am
	./install_locale
dist-hook:
	rm -rf `find $(distdir) -type d -name .svn`
