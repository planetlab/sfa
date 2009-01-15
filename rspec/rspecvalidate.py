#!/usr/bin/python

# $HeadURL$
# $Id$

#
# Validate RSPEC hiearchy, values, types, and names using supplied xsd.
#
# Faiyaz Ahmed <faiyaza at cs dot princeton dot edu>
#
# Copyright 2009 Princeton University
# http://www.planet-lab.org
#

import sys
import pprint
from xml.dom import minidom


def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

# complexType: a supernode comprised of element nodes below it.
def traverseComplexType(cmpTypeNode):
    _elements = {}
    if cmpTypeNode.hasChildNodes():
        for n in cmpTypeNode.getElementsByTagName("xsd:attribute"):
            _elements[n.getAttribute("name")] = {'type': n.getAttribute("type")}


# Element.  {name, value, default}
def Element(elementDom):
    node = {} #parsed dict
    for attr in elementDom.attributes.keys():
        node[attr] = elementDom.attributes.get(attr).value
    # set the name to the name of the element.  otherwise, node name.
    if elementDom.attributes.has_key("name"): 
        element = {(elementDom.localName, elementDom.attributes.get("name").value) : node}
    else:
        element = {elementDom.localName: node}
    # print repr(element)
    # print
    return element

# Sequence is a list of dicts.  Each dict is an element type with Type fields
def Sequence(sequenceNode):
    pass

def buildDict(document, docdict = {}):
    if document.hasChildNodes():
        for i in document.childNodes: 
            if i.attributes: docdict.update({ i.localName: buildDict(i, docdict)})
    if document.attributes: docdict.update(Element(document))
    return docdict

def main(fname):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(buildDict(minidom.parse(fname)))

if __name__ == '__main__':  
    main(fname="planetlab.xsd")
