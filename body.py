#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re

if __name__ == "__main__":
    print('\\frontmatter')
    print('\\input{./target/foreword.tex}')
    print('\\tableofcontents')
    print('\\mainmatter')
    print('\\setcounter{secnumdepth}{3}')
    
    for line in sys.stdin:
        r = re.search(r'\[.*\]\((.*)\.md\)$', line)
        if r is not None and not r.group(1) == 'foreword':
            src = r.group(1)
            print('\\input{./target/' + src + '.tex}')
