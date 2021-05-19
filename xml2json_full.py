#!/usr/bin/python

import xml.etree.ElementTree as et

import json
import sys
import os
import re

def strip_or_none(maybetxt):
    return maybetxt and maybetxt.strip()

def xform_element(elt):
    name = re.sub(r'\{.*\}', '', elt.tag)
    attr = [ dict(key=k, value=v) for k,v in elt.items() ]
    text = strip_or_none(elt.text)
    elts = elt.getchildren()
    tail = strip_or_none(elt.tail)
    body = list(xform_element_body_gen(text, elts, tail))
    return dict(type='tag', name=name, attr=attr, body=body)


def xform_element_body_gen(text, elts, tail):
    if text:
        yield dict(type='text', value=text)
    for elt in elts:
        yield xform_element(elt)
    if tail:
        yield dict(type='text', value=tail)

def main(args):
    if not args or args[0] == '--help':
        print("usage: %s file.xml [--noindent]" % os.path.basename(__file__))
        sys.exit()
    indent = None if args[1:] == ['--noindent'] else 2
    inf = args[0]
    xmltxt = open(inf).read()
    xmltree = et.fromstring(xmltxt)
    dat = xform_element(xmltree)
    print(json.dumps(dat, sort_keys=1, indent=indent))

if __name__ == '__main__':
    main(sys.argv[1:])

