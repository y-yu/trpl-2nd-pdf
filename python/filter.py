#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# pandoc は実行ビットの立っていないフィルタの shebang を読まないので注意
# https://github.com/jgm/pandoc/issues/3174

import os
import sys, base64
import re
from pandocfilters import toJSONFilters, CodeBlock, RawBlock, Str, RawInline, Para

# エスケープ文字にはソースには使われていない文字を指定する
# 大きなコードポイントを指定するとうまくいかない
LISTINGS_ESCAPE = '\u00C0'  # ソースには使われていない文字

# 文字クラスで Unicode エスケープを使うには python 3.3 以降が必要
# https://docs.python.org/3/whatsnew/3.3.html#re
RE_SCRIPT = re.compile(r'''
        # ここに正規表現を追加する際は RE_TEX_SPECIALS の範囲の外を指定すること
        # (?P<cyrillic>[\u0400-\u04FF]+) |
        (?P<hebrew>[\u0590-\u05FF]+) |
        (?P<arabic>[\u0600-\u06FF]+) |
        (?P<devanagari>[\u0900-\u097F]+) |
        (?P<letterlike>[\u2100-\u214F]+) |  # Letterlike Symbols
        # (?P<cjkunified>[\u4E00-\u9FFF]+) |  # CJK Unified Ideographs
        (?P<cjkunified>\u7B80+) | # '简'
        (?P<hangul>[\uAC00-\uD7A3]+) |
        # Misc Symbols and Emojis
        (?P<emoji>[\U0001F330-\U0001F5FF\U0001F600-\U0001F64F]+)
        ''', re.VERBOSE)

RE_TEX_SPECIALS = re.compile(r'([\\&%$#_{}~^])')

# for \texttt
def escape_tex(s):
    return RE_TEX_SPECIALS.sub(r'\\\1', s)

def force_alchars(s):
    return ''.join(r'\ltjalchar%d' % ord(c) for c in s)

def scriptify(s, delim=LISTINGS_ESCAPE):
    def f(m):
        script = [k for k, v in m.groupdict().items() if v][0]
        if script == 'letterlike':
            text = force_alchars(m[script])
        else:
            text = m[script]
        return r'%s\%stext{%s}%s' % (delim, script, text, delim)
    return RE_SCRIPT.sub(f, s)

def mkListingsEnvironment(code, style=''):
    if style:
        style = '[style=%s]' % style
    return RawBlock('latex', '\n'.join(
        (r'\begin{lstlisting}' + style, scriptify(code), r'\end{lstlisting}')
        ) + '\n')

def mkInputListings(src):
    return RawInline('latex', "\\lstinputlisting[style=rust]{" \
            + scriptify(src) + "}")

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

def mkBeginSup():
    return RawInline('latex', '\\textsuperscript{')

def mkEndSup():
    return RawInline('latex', '}')

import json

def filter(key, value, fmt, meta):
    if key == 'Header':
        return RawBlock('header-json', json.dumps(value))
    elif key == 'CodeBlock':  # CodeBlock Attr String
        value[1] = value[1].replace('\uFFFD', '?')
        [[ident, classes, kvs], code] = value
        c = classes[0].split(',')[0]
        if c == 'rust':
            return mkListingsEnvironment(code, c)
        else:
            return mkListingsEnvironment(code)
    elif key == 'Link':  # Link Attr [Inline] Target
        [_, inlines, [href, _]] = value
        if inlines == [Str("include")]:
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
        value = value.replace('\uFFFD', '?').replace('〜', '～')
        value = escape_tex(value)
        value = scriptify(value, '')
        return RawInline('latex', value)
    elif key == 'Code':  # Code Attr String
        value[1] = value[1].replace('\uFFFD', '?')
        value[1] = value[1].replace('+CHARPIPE+', '|')
        # \lstinline 内では LaTeX コマンドが使えないので \texttt を使う
        if RE_SCRIPT.search(value[1]):
            s = escape_tex(value[1])
            s = scriptify(s, '')
            return RawInline('latex', r'\texttt{%s}' % s)
    elif key == 'RawInline':
        [t, s] = value
        if t == 'html' and '<img' in s:
            src = re.search(r'src="img/(.+?)"', s).group(1)
            return mkIncludegraphics(src)
        elif t == 'html' and s == '<sup>':
            return mkBeginSup()
        elif t == 'html' and s == '</sup>':
            return mkEndSup()
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
            elif fmt == 'html' and 'class="caption"' in content:
                return [Para(value), RawBlock('latex', r'\vspace{1em}')]
            elif fmt == 'html' and 'class="filename"' in content:
                return [RawBlock('latex', r'\vspace{1em}'), Para(value)]

def filter1(key, value, fmt, meta):
    if key == 'RawBlock' and value[0] == 'header-json':
        value = json.loads(value[1])
        [level, _, _] = value
        if level == 1:
            file_name = os.getenv('FILENAME', "FILE_DOES_NOT_EXIST")
            value[1][0] = file_name
        return {'t': 'Header', 'c': value}

if __name__ == "__main__":
    toJSONFilters((filter, filter1))
