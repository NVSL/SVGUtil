#!/usr/bin/env python

import argparse
import re

import XMLUtil
from lxml import etree as ET

import InkscapeNS

parser = argparse.ArgumentParser(description="Tool for extracting component positioning information from an svg file.")

parser.add_argument("--in", required=True,  type=str, nargs=1, dest='svgIn', help="input file")
parser.add_argument("--out", required=True,  type=str, nargs=1, dest='svgOut', help="output file")
parser.add_argument("--style", required=False,  type=str, nargs=1, dest='styleAttr', help="style field to modify")
parser.add_argument("--attr", required=False,  type=str, nargs=1, dest='attr', help="attribute to modify")
parser.add_argument("--value", required=True,  type=str, nargs=1, dest='value', help="new value")
parser.add_argument("--class", required=False,  type=str, nargs='+', dest='classes', help="classes to edit")
parser.add_argument("--path", required=False,  type=str, nargs='+', dest='path', help="xpath expression")

args = parser.parse_args()

b = ET.parse(args.svgIn[0]);

if args.classes is not None:
    paths = [ ".//*[@class='" + c + "']" for c in args.classes ]
else:
    paths = args.path

for p in paths:
    #print p
    #print c
    for t in b.getroot().xpath(p, namespaces=InkscapeNS.namespaces):
        #print t
        if args.styleAttr is not None:
            pat = args.styleAttr[0]+":[^;]*;"
            #print pat
            if t.get("style") is None:
                t.set("style","")

            if re.match(pat, t.get("style")):
                n = re.sub(pat, args.styleAttr[0]+":"+args.value[0] +";", t.get("style"))
            else:
                if t.get("style") == "":
                    n = args.styleAttr[0]+":"+args.value[0]
                else:
                    n = t.get("style") + ";" +args.styleAttr[0]+":"+args.value[0]

#            print n
            t.set("style", n)
        elif args.attr is not None:
            t.set(args.attr[0], args.value[0])
            
XMLUtil.formatAndWrite(b, args.svgOut[0])
