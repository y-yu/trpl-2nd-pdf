#!/bin/bash

set -e

cp -r ./book/second-edition/src/img ./
for f in ./img/*.svg
do
  if [[ $f =~ \./img/(.*)\.svg ]]; then
    inkscape -z -D --file=`pwd`/img/${BASH_REMATCH[1]}.svg --export-pdf=`pwd`/${BASH_REMATCH[1]}.pdf
    # inkscape -z -D --file=`pwd`/${BASH_REMATCH[1]}.pdf --export-latex=`pwd`/${BASH_REMATCH[1]}.pdf_tex
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
