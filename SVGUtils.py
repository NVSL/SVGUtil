from lxml import etree as ET
import XMLUtil
import InkscapeNS
import re

def stripStyleByClass(root, c, styleAttr):
    if c is not None:
        p = ".//*[@class='" + c + "']"
    else:
        p = ".//*"
#    print p
    s = root.xpath(p,namespaces=InkscapeNS.namespaces)
 #   print s
    for i in s:
        if i.get(styleAttr) is not None:
            del i.attrib[styleAttr]
        s = i.get("style")
        if s is not None:
#            print s
            s = re.sub(styleAttr+"\s*:\s*[^;]*;?","",s)
 #           print s
            if s == "":
                del i.attrib["style"]
            else:
                i.set("style", s)
  #      ET.dump(i)

def appendSVGStyleSheet(root,c,text) :
    p = ".//svg:style[@class='" + c + "']"
#    print p
    s = root.xpath(p,namespaces=InkscapeNS.namespaces)
#    print s
    for i in s:
        if i.text is None:
            i.text = ""
        i.text +=  "\n" +text

def replaceSVGStyleSheet(root,c,text,repl) :
    p = ".//svg:style[@class='" + c + "']"
#    print p
    s = root.xpath(p,namespaces=InkscapeNS.namespaces)
#    print s
    for i in s:
        if i.text is None:
            i.text = ""
        i.text = i.text.replace(text,repl)

def scrubGradients(root):
    # remove unused gradients.  We could do better by compacting them by follwing xlinks, but that'd be a lot of work.

    inuse ={}
    for e in root.xpath("//svg:linearGradient",namespaces=InkscapeNS.namespaces):
        inuse[e.get("id")] = False
    for e in root.xpath("//svg:radialGradient",namespaces=InkscapeNS.namespaces):
        inuse[e.get("id")] = False

    for e in root.iter():
        l = e.get("{http://www.w3.org/1999/xlink}href")
        if l is not None:
            for g in inuse:
                if re.search(g,l):
                    inuse[g] = True
                    
        if e.get("style") is not None:
            s = e.get("style")
            if re.search("radient", s) is not None:
                for g in inuse:
                    if re.search(g,s):
                        inuse[g] = True

    for e in root.xpath("//svg:linearGradient",namespaces=InkscapeNS.namespaces):
        if not inuse[e.get("id")]:
            e.getparent().remove(e)
    for e in root.xpath("//svg:radialGradient",namespaces=InkscapeNS.namespaces):
        if not inuse[e.get("id")]:
            e.getparent().remove(e)

                        
def uniquifyGradients(root,prefix):
    # ad a prefix to all the gradient names.
    gradients = {}

    def replace(x):
        if re.search("radient", x) is not None:
            #print x
            for g in gradients:
                x = re.sub("#"+g,"#"+gradients[g], x)
            #print x
        return x

    for e in root.xpath("//svg:linearGradient",namespaces=InkscapeNS.namespaces):
        gradients[e.get("id")] = prefix+e.get("id")
        e.set("id",prefix+e.get("id"))

        l = e.get("{http://www.w3.org/1999/xlink}href")
        if l is not None:
            l = replace(l)
            e.set("{http://www.w3.org/1999/xlink}href",l)

    for e in root.xpath("//svg:radialGradient",namespaces=InkscapeNS.namespaces):
        gradients[e.get("id")] = prefix+e.get("id")
        e.set("id",prefix+e.get("id"))

        l = e.get("{http://www.w3.org/1999/xlink}href")
        if l is not None:
            l = replace(l)
            e.set("{http://www.w3.org/1999/xlink}href",l)

    for e in root.iter():
        if e.get("style") is not None:
            s = e.get("style")
            s = ";".join([ replace(x) for x in s.split(";")])
            e.set("style",s)

