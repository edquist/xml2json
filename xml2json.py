#!/usr/bin/python

import xml.etree.ElementTree as et

import collections
import json
import sys
import os
import re

children_name = 'find'
items_name    = 'get'
text_name     = 'text'


def strip_or_none(maybetxt):
    return maybetxt and maybetxt.strip()


def check_sanity(text, children, tail):
    if tail:
        RuntimeError("no tails allowed")

    if text and children:
        raise RuntimeError("bad mix of text and tags")


def xform_element(elt):
    attrs    = dict(elt.items())
    text     = strip_or_none(elt.text)
    children = list(elt.getchildren())
    tail     = strip_or_none(elt.tail)

    check_sanity(text, children, tail)

    d = {}
    if attrs:    d[items_name]    = attrs
    if text:     d[text_name]     = text
    if children: d[children_name] = more_tags(children)
    return d


def more_tags(children):
    ld = collections.defaultdict(list)
    for elt in children:
        name = re.sub(r'\{.*\}', '', elt.tag)
        ld[name].append(xform_element(elt))
    return ld


def main():
    inf = sys.argv[1]
    xmltxt = open(inf).read()
    xmltree = et.fromstring(xmltxt)
    dat = xform_element(xmltree)
    print(json.dumps(dat, sort_keys=1, indent=2))


if __name__ == '__main__':
    main()

