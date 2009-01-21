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
import httplib

logger = Logger

NSURL = "www.planet-lab.org"
xsd = "planetlab.xsd"

def getText(nodelist):
    rc = ""
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc

# The rspec is comprised of 2 parts, and 1 reference:
# attributes/elements describe individual resources
# complexTypes are used to describe a set of attributes/elements
# complexTypes can include a reference to other complexTypes.


class Schema():
    def __init__(self):
        # _getSchema()
        pass

    def _getSchema(self):
        h1 = httplib.HTTPConnection(NSURL)
        h1.request("GET", "/" + xsd)
        r1 = h1.read()
        self.schemadom = minidom.parseString(r1)

    def getName(self, node):
        '''Gets name of node.  Raises NameError exception if no name'''
        if node.attributes.has_key("name"):
            name = node.attributes.get("name").value
        else: raise Exception("Can't find 'name'")
        return name 
    
    # complexType: a supernode comprised of attribute and/or element nodes below it.
    def complexTypeDict(self, cmpTypeDom):
        '''Traverse complex node.  Create a dict 
        {name : [{attributename : {name: value,}, sequence]}'''
        children = [] # array of dicts.  1 for each element/attribute.
        if cmpTypeDom.hasChildNodes():
            for child in cmpTypeDom.childNodes:
                # attributes have tags and values.  get {tag: value}
                if child.localName in ("attribute", "element"): 
                    children.append(self.attributeDict(child))
                # sequence is a list of elements.  append dict to list
                elif child.localName == "sequence": children.append(self.sequenceList(child))
                elif child.localName == "simpleType":  pass #unsure what this type is used for.
                elif child.localName == "complexContent": 
                else: Exception("Unknown type: %s" % child.localName)
        node = { self.getName(cmpTypeDom) : children}
        return node

    def complexContent(self, ccontentDom):
        '''Traverse complexContent.  Return {extention, element}'''
        if ccontentDom.localName == "complexContent":
            for child in ccontentDom.childNodes: pass
        else: raise Exception("%s is not complexContent" % contentDom.localName)
        return node 

    # Attribute.  {name : nameofattribute, {items: values})
    def attributeDict(self, attributeDom):
        '''Traverse single attribute node.  Create a dict {attributename : {name: value,}]}'''
        node = {} # parsed dict
        for attr in attributeDom.attributes.keys():
            node[attr] = attributeDom.attributes.get(attr).value
        attribute = {self.getName(attributeDom) : node}
        return attribute

    # Sequence. [{tag:value},]
    def sequenceList(self, sequenceDom):
        '''Return list of elements/attributes in sequence list'''
        sequence = []
        if sequenceDom.localName == "sequence": 
            # for sanity
            if sequenceDom.hasChildNodes:
                for seqitm in sequenceDom.childNodes:
                    if seqitm.localName in ("element", "attribute"): 
                        sequence.append(self.attributeDict(seqitm))
                    else: print "Idunno what %s is" % seqitm.localName
        else: raise NameError
        return sequence 
    
    def schemaDict(self, document):
        self.schema = {}
        '''Parse the given schema and produce a dict of types'''
        if document.hasChildNodes():
            for i in document.childNodes:
                if i.localName in ('element', 'attribute'): 
                    self.schema.update(self.attributeDict(i))
                elif i.localName == "complexType": 
                    self.schema.update(self.complexTypeDict(i))                
                else: print "Idunno what %s is" % i.localName
        return self.schema



    
def main(fname):
    pp = pprint.PrettyPrinter(indent=4)
    dom = minidom.parse(fname)
    print "Testing Complex Type:"
    s = Schema()
    pp.pprint(s.complexTypeDict(dom.childNodes[0].childNodes[21]))
    print "Testing Whole doc:"
    pp.pprint(s.schemaDict(dom.childNodes[0]))

if __name__ == '__main__':  
    main(fname="planetlab.xsd")
