#!/bin/bash

set -e

if [[ -d "./book" ]]; then
  cd book
  git checkout master
  git pull origin master
  cd ..
else
  git clone https://github.com/hazama-yuinyan/book
fi

cp -r ./book/second-edition/src/img ./
for f in ./img/*.svg
do
  if [[ $f =~ \./img/(.*)\.svg ]]; then
    SVG=`pwd`/img/${BASH_REMATCH[1]}.svg
    PDF=`pwd`/${BASH_REMATCH[1]}.pdf
    PDFTEX=`pwd`/${BASH_REMATCH[1]}.pdf_tex
    inkscape -z -D --file="$SVG" --export-pdf="$PDF" --export-latex
    PAGES=$(egrep -a '/Type /Page\b' "$PDF" | wc -l | tr -d ' ')
    python3 ./python/fix_pdf_tex.py "$PAGES" < "$PDFTEX" > "$PDFTEX.tmp"
    mv "$PDFTEX.tmp" "$PDFTEX"
  fi
done

if [[ ! -d "./target" ]]; then
  mkdir target
fi

for f in ./book/second-edition/src/*.md
do
  cp $f ./target/
  echo $f

  BASE=$(basename $f .md)
  if [[ $BASE =~ appendix-(06|07)- ]]; then
    FILTERS="--filter ./python/fix_headers.py --filter ./python/filter.py"
  else
    FILTERS="--filter ./python/filter.py"
  fi
  FILENAME="$BASE" pandoc -o "./target/$BASE.tex" -f markdown_github+footnotes+header_attributes-hard_line_breaks \
      --pdf-engine=lualatex --top-level-division=chapter --listings $FILTERS $f
done

python3 ./python/body.py < ./target/SUMMARY.md > body.tex
