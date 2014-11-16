# Makefile for tree, June, 1990.  Greg Lee

LEX = flex
# LEXLIB =
# or if you don't have flex, use:
# LEX = lex 
LEXLIB = -lfl

CC=gcc

# Use flag -u or -t to make .tex files:
UT = -u

# Keyword required by PS driver at the begining of TeX
# \specials to incorporate line of text directly in PS output
# (see explanation at the beginning of tex.c).  Default is
# no keyword.
DEFS = -DSKEY=\"ps:\"
#DEFS = -DSKEY=\"ps::\"
#DEFS = -DSKEY=\"ps-string \"
#DEFS = -DSKEY=\"ps-string=\"
#DEFS = -DSKEY=\"pstext=\"
#DEFS =

all:	tree tpar unpar

tree:	tree.l tex.c
	$(LEX) tree.l
	$(CC) $(DEFS) -O -s -o tree lex.yy.c $(LEXLIB)
	rm lex.yy.c

tpar: tpar.l
	$(LEX) tpar.l
	$(CC) -O -s -o tpar lex.yy.c $(LEXLIB)
	rm lex.yy.c

unpar: unpar.l
	$(LEX) unpar.l
	$(CC) -O -s -o unpar lex.yy.c $(LEXLIB)
	rm lex.yy.c

mdoc:	mdoc.l
	$(LEX) mdoc.l
	$(CC) -O -s -o mdoc lex.yy.c $(LEXLIB)
	@rm lex.yy.c

use.tre: use.raw mdoc
	rm -f use.tre
	mdoc <use.raw >use.tre

tex:	sample.tex texsample.tex tpsample.tex use.tex

sample.tex: sample tree
	rm -f sample.tex
	@echo '--- Expect a warning about an ill-formed \tree command ---'
	tree $(UT) sample >sample.tex
tpsample.tex: tpsample tree tpar
	rm -f tpsample.tex
	tpar -t tpsample |tree $(UT) >tpsample.tex
texsample.tex: texsample tree
	rm -f texsample.tex
	tree $(UT) texsample >texsample.tex
use.tex: use.tre tree
	rm -f use.tex
	@echo '--- Expect two warnings about discarded text ---'
	tree $(UT) use.tre >use.tex

shar:
	makekit -m
	mv Part01 tree.shar1
	mv Part02 tree.shar2
	mv Part03 tree.shar3

DIST = MANIFEST Makefile README mdoc.l sample tex.c \
	texsample tpar.l tpsample tree.1 tree.l unpar.l use.raw

tar:	$(DIST)
	tar cf tree.tar $(DIST)

zoo:	$(DIST)
	zoo a tree $(DIST)
