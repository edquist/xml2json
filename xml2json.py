#!/usr/bin/python

import xml.etree.ElementTree as et

import json
import sys
import os
import re

def strip_or_none(maybetxt):
    return maybetxt and maybetxt.strip()

def xform_element(elt):
    name     = re.sub(r'\{.*\}', '', elt.tag)
    attrs    = list(elt.items())
    text     = strip_or_none(elt.text)
    children = elt.getchildren()
    tail     = strip_or_none(elt.tail)
    body     = list(xform_element_body_gen(text, children, tail))
    return ('tag', dict(name=name, attrs=attrs, body=body))


def xform_element_body_gen(text, children, tail):
    if text:
        yield ('text', text)
    for elt in children:
        yield xform_element(elt)
    if tail:
        yield ('text', tail)

def main():
    inf = sys.argv[1]
    xmltxt = open(inf).read()
    xmltree = et.fromstring(xmltxt)
    dat = xform_element(xmltree)
    print(json.dumps(dat, sort_keys=1, indent=2))

if __name__ == '__main__':
    main()

