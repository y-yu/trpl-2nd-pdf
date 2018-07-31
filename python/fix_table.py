#!/usr/bin/env python3
import re
import sys


for line in sys.stdin:
    line = line.rstrip()
    if re.search(r'[^-|]', line):
        print(re.sub(r'<code>(.*?)</code>',
              lambda m: '`%s`' % m.group(1).replace(r'\|', '+CHARPIPE+'),
              line))
    else:
        ncols = len(re.findall(r'-+\|', line))
        # http://pandoc.org/MANUAL.html#extension-pipe_tables
        if ncols == 4:  # Table B-1
            print('|-|---|---|--|')
        elif ncols == 2:
            print('|-|---|')
        else:
            print(line)
