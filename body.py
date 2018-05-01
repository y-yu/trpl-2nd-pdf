#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re

if __name__ == "__main__":
    print('\\frontmatter')
    print('\\tableofcontents')
    print('\\mainmatter')
    print('\\setcounter{secnumdepth}{3}')
    
    for line in sys.stdin:
        r = re.search(r'\[.*\]\((.*)\.md\)$', line)
        if r is not None:
            src = r.group(1)
            print('\\input{./target/' + src + '.tex}')
