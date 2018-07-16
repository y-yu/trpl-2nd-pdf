#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

re_include_graphics = re.compile(
        r'\\includegraphics\[width=\\unitlength,page=(\d+)\]')
re_end_picture = re.compile(r'\\end\{picture\}')

inside = False
num_pages = int(sys.argv[1])
for line in sys.stdin:
    if not inside:
        m = re_include_graphics.search(line)
        if m and int(m.group(1)) > num_pages:
            inside = True
            sys.stderr.write('skip: %s' % line)
            continue
    else:
        if re_end_picture.search(line):
            inside = False
        else:
            sys.stderr.write('skip: %s' % line)
            continue
    print(line)

