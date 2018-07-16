#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pandocfilters import toJSONFilter, Header

def action(key, value, fmt, meta):
    # Header Int Attr [Inline]
    if key == 'Header':
        level, attr, inlines = value
        return Header(level + 1, attr, inlines)

if __name__ == "__main__":
    toJSONFilter(action)
