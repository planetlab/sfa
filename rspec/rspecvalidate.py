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
from logging import Logger

logger = Logger

# The rspec is comprised of 2 parts, and 1 reference:
# attributes/elements describe individual resources
# complexTypes are used to describe a set of attributes/elements
# complexTypes can include a reference to other complexTypes.

def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

def getName(node):
    '''Gets name of node.  Raises NameError exception if no name'''
    if node.attributes.has_key("name"):
        name = node.attributes.get("name").value
    else: raise Exception("Can't find 'name'")
    return name 

# complexType: a supernode comprised of attribute and/or element nodes below it.
def complexTypeDict(cmpTypeDom):
    '''Traverse complex node.  Create a dict {name : [{attributename : {name: value,}, sequence]}'''
    children = [] # array of dicts.  1 for each element/attribute.
    if cmpTypeDom.hasChildNodes():
        for child in cmpTypeDom.childNodes:
            # attributes have tags and values.  get {tag: value}
            if child.localName in ("attribute", "element"): children.append(attributeDict(child))
            # sequence is a list of elements.  append dict to list
            elif child.localName == "sequence": children.append(sequenceList(child))
            elif child.localName == "simpleType":  pass #unsure what this type is used for.
            else: Exception("Unknown type: %s" % child.localName)
    node = { getName(cmpTypeDom) : children}
    return node

# Attribute.  {name : nameofattribute, {items: values})
def attributeDict(attributeDom):
    '''Traverse single attribute node.  Create a dict {attributename : {name: value,}]}'''
    node = {} # parsed dict
    for attr in attributeDom.attributes.keys():
        node[attr] = attributeDom.attributes.get(attr).value
    attribute = {getName(attributeDom) : node}
    return attribute

def sequenceList(sequenceDom):
    '''Return list of elements/attributes in sequence list'''
    sequence = []
    if sequenceDom.localName == "sequence": 
        # for sanity
        if sequenceDom.hasChildNodes:
            for seqitm in sequenceDom.childNodes:
                if seqitm.localName in ("element", "attribute"): 
                    sequence.append(attributeDict(seqitm))
                else: print "Idunno what %s is" % seqitm.localName
        else: raise NameError
    return sequence 

def schemaDict(document):
    schema = {}
    '''Parse the given schema and produce a dict of types'''
    if document.hasChildNodes():
        for i in document.childNodes:
            if i.localName in ('element', 'attribute'): 
                schema.update(attributeDict(i))
            elif i.localName == "complexType": 
                schema.update(complexTypeDict(i))                
            else: print "Idunno what %s is" % i.localName
    return schema

def main(fname):
    pp = pprint.PrettyPrinter(indent=4)
    dom = minidom.parse(fname)
    print "Testing Complex Type:"
    pp.pprint(complexTypeDict(dom.childNodes[0].childNodes[15]))
    print "Testing Whole doc:"
    pp.pprint(schemaDict(dom.childNodes[0]))

if __name__ == '__main__':  
    main(fname="planetlab.xsd")
