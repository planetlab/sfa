import sys
import pprint
import os
from xml.dom import minidom
from types import StringTypes

class Rspec():

    def __init__(self, xml = None, xsd = None):
        self.xsd = xsd # schema
        self.rootNode = None # root of the dom
        self.dict = {} # dict of the rspec.
        if xml: 
            if type(xml) == file:
                self.parseFile(xml)
            if type(xml) == str:
                self.parseString(xml)
            self.dict = self.toDict() 
  
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
        name = None
        if not node.nodeName.startswith("#"):
            if node.localName:
                name = node.localName
            elif node.attributes.has_key("name"):
                name = node.attributes.get("name").value
        return name     
 
 
    # Attribute.  {name : nameofattribute, {items: values})
    def _attributeDict(self, attributeDom):
        '''Traverse single attribute node.  Create a dict {attributename : {name: value,}]}'''
        node = {} # parsed dict
        for attr in attributeDom.attributes.keys():
            node[attr] = attributeDom.attributes.get(attr).value
        return node
  
 
    def toDict(self, nodeDom = None):
        """
        convert this rspec to a dict and return it.
        """
        node = {}
        if not nodeDom:
             nodeDom = self.rootNode
  
        elementName = nodeDom.nodeName
        if elementName and not elementName.startswith("#"):
            # attributes have tags and values.  get {tag: value}, else {type: value}
            node[elementName] = self._attributeDict(nodeDom)
            #node.update(self._attributeDict(nodeDom))
            # resolve the child nodes.
            if nodeDom.hasChildNodes():
                for child in nodeDom.childNodes:
                    childName = self._getName(child)
                    if not childName:
                        continue
                    if not node[elementName].has_key(childName):
                        node[elementName][childName] = []       
                        #node[childName] = []
                    childdict = self.toDict(child)
                    for value in childdict.values():
                        node[elementName][childName].append(value)
                    #node[childName].append(self.toDict(child))
        return node

  
    def toxml(self):
        """
        convert this rspec to an xml string and return it.
        """
        return self.rootNode.toxml()

  
    def toprettyxml(self):
        """
        print this rspec in xml in a pretty format.
        """
        return self.rootNode.toprettyxml()

  
    def parseFile(self, filename):
        """
        read a local xml file and store it as a dom object.
        """
        dom = minidom.parse(filename)
        self.rootNode = dom.childNodes[0]
  
  
    def parseString(self, xml):
        """
        read an xml string and store it as a dom object.
        """
        xml = xml.replace('\n', '').replace('\t', '').strip()
        dom = minidom.parseString(xml)
        self.rootNode = dom.childNodes[0]

 
    def dict2dom(self, rdict, include_doc = False):
        """
        convert a dict object into a dom object.
        """
     
    def elementNode(tagname, rd):
        element = minidom.Element(tagname)   
        for key in rd.keys():
            if isinstance(rd[key], StringTypes):
                element.setAttribute(key, rd[key])
            elif isinstance(rd[key], dict):
                 child = elementNode(key, rd[key])
                 element.appendChild(child)
            elif isinstance(rd[key], list):
                 for item in rd[key]:
                     child = elementNode(key, item)
                     element.appendChild(child)
        return element
                     
        node = elementNode(rdict.keys()[0], rdict.values()[0])
        if include_doc:
            rootNode = minidom.Document()
            rootNode.appendChild(node)
        else:
            rootNode = node
        return rootNode

 
    def parseDict(self, rdict, include_doc = True):
        """
        Convert a dictionary into a dom object and store it.
        """
        self.rootNode = self.dict2dom(rdict, include_doc)
 
 
    def getDictsByTagName(self, tagname, dom = None):
        """
        Search the dom for all elements with the specified tagname
        and return them as a list of dicts
        """
        if not dom:
            dom = self.rootNode
        dicts = []
        doms = dom.getElementsByTagName(tagname)
        dictlist = [self.toDict(d) for d in doms]
        for item in dictlist:
            for value in item.values():
                dicts.append(value)
        return dicts

# vim:ts=4:expandtab
