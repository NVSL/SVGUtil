#!/usr/bin/env python

import argparse
from lxml import etree as ET
import XMLUtil
import InkscapeNS
import sys
import re

parser = argparse.ArgumentParser(description="Tool for extracting component positioning information from an svg file.")

parser.add_argument("--in", required=True,  type=str, nargs=1, dest='svgIn', help="input file")
parser.add_argument("--out", required=True,  type=str, nargs=1, dest='svgOut', help="output file")
parser.add_argument("--style", required=True,  type=str, nargs=1, dest='styleAttr', help="style field to modify")
parser.add_argument("--value", required=True,  type=str, nargs=1, dest='value', help="new value")
parser.add_argument("--class", required=True,  type=str, nargs='+', dest='classes', help="tag classes to edit")

args = parser.parse_args()

b = ET.parse(args.svgIn[0]);

for c in args.classes:
    p = ".//*[@class='" + c + "']"
  #  print p
    for t in b.getroot().xpath(p, namespaces=InkscapeNS.namespaces):
        pat = args.styleAttr[0]+":[^;]*;"
#        print pat
        n = re.sub(pat, args.styleAttr[0]+":"+args.value[0] +";", t.get("style"))
 #       print n
        t.set("style", n)

XMLUtil.formatAndWrite(b, args.svgOut[0])
