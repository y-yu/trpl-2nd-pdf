#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys, base64, re
from pandocfilters import toJSONFilter, CodeBlock, RawBlock, Str, RawInline

reload(sys)  
sys.setdefaultencoding('utf8')

def mkListingsEnvironment(code):
    return RawBlock('latex', "\\begin{lstlisting}[style=rust]\n" + code + "\n\\end{lstlisting}\n")

def mkInputListings(src):
    return RawInline('latex', "\\lstinputlisting[style=rust]{" + src + "}")

def mkIncludegraphics(src):
    return RawInline('latex', "\\includegraphics{img/" + src + "}")

def mkRef(src):
    return RawInline('latex', "\\ref{" + src + u"}章")

def filter(key, value, fmt, meta):
    if key == 'CodeBlock':
        value[1] = value[1].replace(b'\xef\xbf\xbd', '?')
        [[ident, classes, kvs], code] = value
        c = classes[0].split(',')[0]
        if c == 'rust':
            return mkListingsEnvironment(code)
    elif key == 'Link':
        [_, text, [href, _]] = value
        if text == [Str("include")]:
            return mkInputListings(href)
        elif href.endswith(".md"):
            src = re.search(r'(?:./)?(.+\.md)', href).group(1)
            return mkRef(src)
    elif key == 'Image':
        [_, _, [src, _]] = value
        if src.startswith("http"):
            fileName = src.split("/")[-1]
            os.system("cd img && curl -O " + src)
            return mkIncludegraphics(fileName)
    elif key == 'Str':
        return(Str(value.replace(b'\xef\xbf\xbd', '?').replace(u"〜", u"～")))
    elif key == 'Code':
        value[1] = value[1].replace(b'\xef\xbf\xbd', '?')
    elif key == 'Header':
        [level, _, _] = value
        if level == 1:
            file_name = os.getenv('FILENAME', "FILE_DOES_NOT_EXIST")
            value[1][0] = file_name

if __name__ == "__main__":
    toJSONFilter(filter)
