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
import os
from xml.dom import minidom
import logging 
import httplib

logging.basicConfig(level=logging.DEBUG)


class Schema():
    '''Manipulates Rspec xsd into python dict'''
    def __init__(self):
        self.NSURL = "www.planet-lab.org"
        self.xsd = "planetlab.xsd"
        self.schemaDom = None # parsed schema file's DOM
        self.schemaDict = self.nodeDict()
       
    def _getSchema(self):
        '''If the schema doesn't exist at the NameSpace's URL, then use the 
           local file.'''
        conn = httplib.HTTPConnection(self.NSURL)
        conn.request("GET", "/" + self.xsd)
        r1 = conn.getresponse()
        if r1.status != 200:
            logging.debug("http://%s/%s: file not found" %(self.NSURL,self.xsd))
            if os.path.exists(self.xsd):
                logging.debug("using local copy.")
                self.schemaDom = minidom.parse(self.xsd)
        else:
            self.schemaDom = minidom.parseString(r1.read())
        # XML begings with a '#document'.  Just check to be safe.
        if self.schemaDom.nodeName == "#document": 
            self.schemaDom = self.schemaDom.childNodes[0]
 

    def _getText(self, nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc
    
    # The rspec is comprised of 2 parts, and 1 reference:
    # attributes/elements describe individual resources
    # complexTypes are used to describe a set of attributes/elements
    # complexTypes can include a reference to other complexTypes.
    
    
    def _getName(self, node):
        '''Gets name of node. If tag has no name, then return tag's localName'''
        if not node.nodeName.startswith("#"):
            if node.attributes.has_key("name"):
                name = node.attributes.get("name").value
            else: 
                name = node.localName
        return name

    def nodeDict(self, nodeDom = None):
        '''Traverse complex node.  Create a dict 
        {name : [{attributename : {name: value,}, sequence]}'''
        children = [] # array of dicts.  1 for each element/attribute.
        node = {}
        if not nodeDom: 
            self._getSchema()
            nodeDom = self.schemaDom
        if nodeDom.nodeName and not nodeDom.nodeName.startswith("#"):
            # attributes have tags and values.  get {tag: value}, else {type: value} 
            children.append(self._attributeDict(nodeDom))
            # resolve the child nodes.
            if nodeDom.hasChildNodes():
                for child in nodeDom.childNodes:
                        childelems = self.nodeDict(child)
                        if len(childelems): children.append(childelems)
            node = { self._getName(nodeDom) : children}
        return node
    
    
    # Attribute.  {name : nameofattribute, {items: values})
    def _attributeDict(self, attributeDom):
        '''Traverse single attribute node.  Create a dict {attributename : {name: value,}]}'''
        node = {} # parsed dict
        for attr in attributeDom.attributes.keys():
            node[attr] = attributeDom.attributes.get(attr).value
        return node

   
def main(fname):
    pp = pprint.PrettyPrinter(indent=4)
    dom = minidom.parse(fname)
    s = Schema()
    print "Testing Complex Type:"
    pp.pprint(s.nodeDict(dom.childNodes[0].childNodes[21]))

    print "Testing Whole Doc:"
    pp.pprint(s.nodeDict(dom.childNodes[0]))

    print "Testing URL ofWhole doc:"
    pp.pprint(s.schemaDict)

if __name__ == '__main__':  
    main(fname="planetlab.xsd")
