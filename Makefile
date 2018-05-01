.PHONY : all clean

all : book.pdf

clean :
	latexmk -C

book.pdf : book.tex body.tex
	latexmk -pdf book.tex
