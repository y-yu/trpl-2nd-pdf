#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys, base64, re
from pandocfilters import toJSONFilter, Header

reload(sys)
sys.setdefaultencoding('utf8')

def action(key, value, fmt, meta):
    # Header Int Attr [Inline]
    if key == 'Header':
        level, attr, inlines = value
        return Header(level + 1, attr, inlines)

if __name__ == "__main__":
    toJSONFilter(action)
