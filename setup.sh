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

mkdir target

for f in ./book/second-edition/src/*.md
do
  if [[ $f =~ \./book/second-edition/src/(.*)\.md ]]; then
    cp $f ./target/
    echo $f  
    FILENAME="${BASH_REMATCH[1]}.md" pandoc -o "./target/${BASH_REMATCH[1]}.tex" -f markdown_github+footnotes+header_attributes-hard_line_breaks-intraword_underscores --pdf-engine=lualatex --top-level-division=chapter --listings --filter ./filter.py $f
  fi
done
