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

def mkFigure(path, align=None, scale=None):
    scale = '' if scale is None else '%.2f' % scale

    if not os.path.exists(path):
        return [RawBlock('latex', '\fbox{Image File does not exist}'),
                RawBlock('latex', '\message{Image File `%s` does not exist}' % path)]

    root, ext = os.path.splitext(path)
    if ext == '.svg':
        svgwidth = r'\def\svgwidth{%s\textwidth}' % scale
        input_ = r'\input{%s}' % (os.path.basename(root) + '.pdf_tex')
        if align == 'center':
            return RawBlock('latex', '\n'.join(
                (r'\begin{center}', svgwidth, input_, r'\end{center}')))
        else:
            return RawBlock('latex', svgwidth + '\n' + input_)
    else:
        return RawBlock('latex', r'\includegraphics{%s}' % path)

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
        elif (not href.startswith("http")) and href.endswith(".md"):
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
    elif key == 'RawInline':
        [t, s] = value
        if t == 'html' and '<img' in s:
            src = re.search(r'src="img/(.+?)"', s).group(1)
            return mkIncludegraphics(src)
    elif key == 'Para':
        if value[0]['t'] == 'RawInline':
            fmt, content = value[0]['c']
            if fmt == 'html' and '<img' in content:
                src = re.search(r'src="(img/.+?)"', content).group(1)
                cls = re.search(r'class="(.+?)"', content)
                if cls:
                    cls = cls.group(1)
                width = re.search(r'style="width: *(\d+)%;?', content)
                if width:
                    width = float(width.group(1)) / 100
                return mkFigure(src, align=cls, scale=width)

if __name__ == "__main__":
    toJSONFilter(filter)
