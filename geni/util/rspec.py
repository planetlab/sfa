import sys
import pprint
import os
import httplib
from xml.dom import minidom
from types import StringTypes, ListType

class Rspec():

    def __init__(self, xml = None, xsd = None, NSURL = None):
        '''
        Class to manipulate RSpecs.  Reads and parses rspec xml into python dicts
        and reads python dicts and writes rspec xml

        self.xsd = # Schema.  Can be local or remote file.
        self.NSURL = # If schema is remote, Name Space URL to query (full path minus filename)
        self.rootNode = # root of the DOM
        self.dict = # dict of the RSpec.
        self.schemaDict = {} # dict of the Schema
        '''
 
        self.xsd = xsd
        self.rootNode = None
        self.dict = {}
        self.schemaDict = {}
        self.NSURL = NSURL 
        if xml: 
            if type(xml) == file:
                self.parseFile(xml)
            if type(xml) == str:
                self.parseString(xml)
            self.dict = self.toDict() 
        if xsd:
            self._parseXSD(self.NSURL + self.xsd)


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

 
    def _httpGetXSD(self, xsdURI):
        # split the URI into relevant parts
        host = xsdURI.split("/")[2]
        if xsdURI.startswith("https"):
            conn = httplib.HTTPSConnection(host,
                httplib.HTTPSConnection.default_port)
        elif xsdURI.startswith("http"):
            conn = httplib.HTTPConnection(host,
                httplib.HTTPConnection.default_port)
        conn.request("GET", xsdURI)
        # If we can't download the schema, raise an exception
        r1 = conn.getresponse()
        if r1.status != 200: 
            raise Exception
        return r1.read().replace('\n', '').replace('\t', '').strip() 


    def _parseXSD(self, xsdURI):
        """
        Download XSD from URL, or if file, read local xsd file and set schemaDict
        """
        # Since the schema definiton is a global namespace shared by and agreed upon by
        # others, this should probably be a URL.  Check for URL, download xsd, parse, or 
        # if local file, use local file.
        schemaDom = None
        if xsdURI.startswith("http"):
            try: 
                schemaDom = minidom.parseString(self._httpGetXSD(xsdURI))
            except Exception, e:
                # logging.debug("%s: web file not found" % xsdURI)
                # logging.debug("Using local file %s" % self.xsd")
                print e
                print "Can't find %s on the web. Continuing." % xsdURI
        if not schemaDom:
            if os.path.exists(xsdURI):
                # logging.debug("using local copy.")
                print "Using local %s" % xsdURI
                schemaDom = minidom.parse(xsdURI)
            else:
                raise Exception("Can't find xsd locally")
        self.schemaDict = self.toDict(schemaDom.childNodes[0])


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

    def getDictByTagNameValue(self, tagname, value, dom = None):
        """
        Search the dom for the first element with the specified tagname
        and value and return it as a dict.
        """
        tempdict = {}
        if not dom:
            dom = self.rootNode
        dicts = self.getDictsByTagName(tagname, dom)
        
        for rdict in dicts:
            if rdict.has_key('name') and rdict['name'] in [value]:
                return rdict
              
        return tempdict


    def filter(self, tagname, attribute, blacklist = [], whitelist = [], dom = None):
        """
        Removes all elements where:
        1. tagname matches the element tag
        2. attribute matches the element attribte
        3. attribute value is in valuelist  
        """

        tempdict = {}
        if not dom:
            dom = self.rootNode
       
        if dom.localName in [tagname] and dom.attributes.has_key(attribute):
            if whitelist and dom.attributes.get(attribute).value not in whitelist:
                dom.parentNode.removeChild(dom)
            if blacklist and dom.attributes.get(attribute).value in blacklist:
                dom.parentNode.removeChild(dom)
           
        if dom.hasChildNodes():
            for child in dom.childNodes:
                self.filter(tagname, attribute, blacklist, whitelist, child) 

# vim:ts=4:expandtab
