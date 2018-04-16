.PHONY : all clean

all : book.pdf

clean :
	latexmk -C

book.pdf :
	latexmk -pdf book.tex
