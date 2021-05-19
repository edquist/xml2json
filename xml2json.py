#!/usr/bin/python

import xml.etree.ElementTree as et

import collections
import json
import sys
import os
import re

attrs_name = 'attr'
elts_name  = 'tags'
text_name  = 'text'


def strip_or_none(maybetxt):
    return maybetxt and maybetxt.strip()


def check_sanity(text, elts, tail):
    if tail:
        RuntimeError("no tails allowed")

    if text and elts:
        raise RuntimeError("bad mix of text and tags")


def xform_element(elt):
    attrs = dict(elt.items())
    elts  = list(elt.getchildren())
    text  = strip_or_none(elt.text)
    tail  = strip_or_none(elt.tail)

    check_sanity(text, elts, tail)

    d = {}
    if attrs: d[attrs_name] = attrs
    if text:  d[text_name]  = text
    if elts:  d[elts_name]  = buckettize(elts)
    return d


def buckettize(elts):
    ld = collections.defaultdict(list)
    for elt in elts:
        name = re.sub(r'\{.*\}', '', elt.tag)
        ld[name].append(xform_element(elt))
    return ld


def main(args):
    indent = None if args[1:] == ['--noindent'] else 2
    inf = args[0]
    xmltxt = open(inf).read()
    xmltree = et.fromstring(xmltxt)
    dat = xform_element(xmltree)
    print(json.dumps(dat, sort_keys=1, indent=indent))


if __name__ == '__main__':
    main(sys.argv[1:])

