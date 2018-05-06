#!/bin/bash

set -e

cp -r ./book/second-edition/src/img ./
for f in ./img/*.svg
do
  if [[ $f =~ \./img/(.*)\.svg ]]; then
    SVG=`pwd`/img/${BASH_REMATCH[1]}.svg
    PDF=`pwd`/${BASH_REMATCH[1]}.pdf
    PDFTEX=`pwd`/${BASH_REMATCH[1]}.pdf_tex
    inkscape -z -D --file="$SVG" --export-pdf="$PDF" --export-latex
    PAGES=$(egrep -a '/Type /Page\b' "$PDF" | wc -l | tr -d ' ')
    python fix_pdf_tex.py "$PAGES" < "$PDFTEX" > "$PDFTEX.tmp"
    mv "$PDFTEX.tmp" "$PDFTEX"
  fi
done

if [[ ! -e target ]]; then
  mkdir target
fi

for f in ./book/second-edition/src/*.md
do
  cp $f ./target/
  echo $f

  BASE=$(basename $f .md)
  if [[ $BASE =~ appendix-(06|07)- ]]; then
    FILTERS="--filter ./fix_headers.py --filter ./filter.py"
  else
    FILTERS="--filter ./filter.py"
  fi
  FILENAME="$BASE" pandoc -o "./target/$BASE.tex" -f markdown_github+footnotes+header_attributes-hard_line_breaks \
      --pdf-engine=lualatex --top-level-division=chapter --listings $FILTERS $f
done

python body.py < ./target/SUMMARY.md > body.tex
