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

def buildDict(document):
	if document.hasChildNodes():
		for i in document.childNodes: buildDict(i)
	print document.localName

def main(fname):
	buildDict(minidom.parse(fname))

if __name__ == '__main__':  
	main(fname="planetlab.xsd")
