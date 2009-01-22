import sys
import pprint
import os
from xml.dom import minidom

class Rspec():

    def __init__(self, xml = None, xsd = None):
	self.xsd = xsd
        self.rootNode = None
	if xml:
	    self.parse_string(xml)
	    

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

    def parseDict(self, rdict):
	"""
	convert a dict object into a dom object.
	"""
	doc = minidom.Document()

	
	def elementDict(rd):
	    for key in rd.keys():
		if isinstance(rd[key], dict):
		    elementFromDict(rd[key])
	 		    	
	for key in dict.keys():    
	    doc.appendChild(dictElement(rdict))
        self.rootNode = doc


	
