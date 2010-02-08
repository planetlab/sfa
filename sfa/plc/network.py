from __future__ import with_statement
import re
import socket
from sfa.util.namespace import *
from sfa.util.faults import *
from xmlbuilder import XMLBuilder
from lxml import etree
import sys
from StringIO import StringIO


class Sliver:
    def __init__(self, node):
        self.node = node
        self.network = node.network
        self.slice = node.network.slice
        
    def toxml(self, xml):
        with xml.sliver:
            self.slice.tags_to_xml(xml, self.node)

        
class Iface:
    def __init__(self, network, iface):
        self.network = network
        self.id = iface['interface_id']
        self.idtag = "i%s" % self.id
        self.ipv4 = iface['ip']
        self.bwlimit = iface['bwlimit']
        self.hostname = iface['hostname']

    """
    Just print out bwlimit right now
    """
    def toxml(self, xml):
        if self.bwlimit:
            with xml.bw_limit(units="kbps"):
                xml << str(self.bwlimit / 1000)


class Node:
    def __init__(self, network, node, bps = 1000 * 1000000):
        self.network = network
        self.id = node['node_id']
        self.idtag = "n%s" % self.id
        self.hostname = node['hostname']
        self.site_id = node['site_id']
        self.iface_ids = node['interface_ids']
        self.sliver = None
        self.whitelist = node['slice_ids_whitelist']

    def get_ifaces(self):
        i = []
        for id in self.iface_ids:
            i.append(self.network.lookupIface(id))
            # Only return the first interface
            break
        return i
        
    def get_site(self):
        return self.network.lookupSite(self.site_id)
    
    def add_sliver(self):
        self.sliver = Sliver(self)

    def toxml(self, xml):
        slice = self.network.slice
        if self.whitelist and not self.sliver:
            if not slice or slice.id not in self.whitelist:
                return

        with xml.node(id = self.idtag):
            with xml.hostname:
                xml << self.hostname
            if self.network.type == "VINI":
                with xml.kbps:
                    xml << str(int(self.bps/1000))
            for iface in self.get_ifaces():
                iface.toxml(xml)
            if self.sliver:
                self.sliver.toxml(xml)
    

class Site:
    def __init__(self, network, site):
        self.network = network
        self.id = site['site_id']
        self.idtag = "s%s" % self.id
        self.node_ids = site['node_ids']
        self.node_ids.sort()
        self.name = site['abbreviated_name']
        self.tag = site['login_base']
        self.public = site['is_public']
        self.enabled = site['enabled']
        self.links = set()
        self.whitelist = False

    def get_sitenodes(self):
        n = []
        for i in self.node_ids:
            n.append(self.network.lookupNode(i))
        return n
    
    def toxml(self, xml):
        if not (self.public and self.enabled and self.node_ids):
            return
        with xml.site(id = self.idtag):
            with xml.name:
                xml << self.name
            for node in self.get_sitenodes():
                node.toxml(xml)
   
    
class Slice:
    def __init__(self, network, hrn, slice):
        self.hrn = hrn
        self.network = network
        self.id = slice['slice_id']
        self.name = slice['name']
        self.node_ids = set(slice['node_ids'])
        self.slice_tag_ids = slice['slice_tag_ids']
    
    """
    Use with tags that can have more than one instance
    """
    def get_multi_tag(self, tagname, node = None):
        tags = []
        for i in self.slice_tag_ids:
            tag = self.network.lookupSliceTag(i)
            if tag.tagname == tagname:
                if not (node and node.id != tag.node_id):
                    tags.append(tag)
        return tags
        
    """
    Use with tags that have only one instance
    """
    def get_tag(self, tagname, node = None):
        for i in self.slice_tag_ids:
            tag = self.network.lookupSliceTag(i)
            if tag.tagname == tagname:
                if (not node) or (node.id == tag.node_id):
                    return tag
        return None
        
    def get_nodes(self):
        n = []
        for id in self.node_ids:
            n.append(self.network.nodes[id])
        return n
  
    # Add a new slice tag   
    def add_tag(self, tagname, value, node = None):
        record = {'slice_tag_id':None, 'slice_id':self.id, 'tagname':tagname, 'value':value}
        if node:
            record['node_id'] = node.id
        else:
            record['node_id'] = None
        tag = Slicetag(record)
        self.network.tags[tag.id] = tag
        self.slice_tag_ids.append(tag.id)
        tag.changed = True       
        tag.updated = True
        return tag
    
    # Update a slice tag if it exists, else add it             
    def update_tag(self, tagname, value, node = None):
        tag = self.get_tag(tagname, node)
        if tag and tag.value == value:
            value = "no change"
        elif tag:
            tag.value = value
            tag.changed = True
        else:
            tag = self.add_tag(tagname, value, node)
        tag.updated = True
            
    def update_multi_tag(self, tagname, value, node = None):
        tags = self.get_multi_tag(tagname, node)
        for tag in tags:
            if tag and tag.value == value:
                value = "no change"
                break
        else:
            tag = self.add_tag(tagname, value, node)
        tag.updated = True
            
    def tags_to_xml(self, xml, node = None):
        tagtypes = self.network.getTagTypes()
        for tt in tagtypes:
            if tt.multi:
                tags = self.get_multi_tag(tt.tagname, node)
                for tag in tags:
                    if not tag.deleted:  ### Debugging
                        xml << (tag.tagname, tag.value)
            else:
                tag = self.get_tag(tt.tagname, node)
                if tag:
                    if not tag.deleted:   ### Debugging
                        xml << (tag.tagname, tag.value)

    def toxml(self, xml):
        with xml.sliver_defaults:
            self.tags_to_xml(xml)


class Slicetag:
    newid = -1 
    def __init__(self, tag):
        self.id = tag['slice_tag_id']
        if not self.id:
            # Make one up for the time being...
            self.id = Slicetag.newid
            Slicetag.newid -= 1
        self.slice_id = tag['slice_id']
        self.tagname = tag['tagname']
        self.value = tag['value']
        self.node_id = tag['node_id']
        self.updated = False
        self.changed = False
        self.deleted = False
    
    # Mark a tag as deleted
    def delete(self):
        self.deleted = True
        self.updated = True
    
    def write(self, api):
        if self.changed:
            if int(self.id) > 0:
                api.plshell.UpdateSliceTag(api.plauth, self.id, self.value)
            else:
                api.plshell.AddSliceTag(api.plauth, self.slice_id, 
                                        self.tagname, self.value, self.node_id)
        elif self.deleted and int(self.id) > 0:
            api.plshell.DeleteSliceTag(api.plauth, self.id)


class TagType:
    def __init__(self, tagtype):
        self.id = tagtype['tag_type_id']
        self.tagname = tagtype['tagname']
        if self.tagname in ['codemux', 'ip_addresses', 'vsys']:
            self.multi = True
        else:
            self.multi = False


"""
A Network is a compound object consisting of:
* a dictionary mapping site IDs to Site objects
* a dictionary mapping node IDs to Node objects
* a dictionary mapping interface IDs to Iface objects
"""
class Network:
    def __init__(self, api, type = "PlanetLab"):
        self.api = api
        self.type = type
        self.sites = self.get_sites(api)
        self.nodes = self.get_nodes(api)
        self.ifaces = self.get_ifaces(api)
        self.tags = self.get_slice_tags(api)
        self.tagtypes = self.get_tag_types(api)
        self.slice = None
    
    """ Lookup site based on id or idtag value """
    def lookupSite(self, id):
        val = None
        if isinstance(id, basestring):
            id = int(id.lstrip('s'))
        try:
            val = self.sites[id]
        except:
            raise InvalidRSpec("site ID %s not found" % id)
        return val
    
    def getSites(self):
        sites = []
        for s in self.sites:
            sites.append(self.sites[s])
        return sites
        
    """ Lookup node based on id or idtag value """
    def lookupNode(self, id):
        val = None
        if isinstance(id, basestring):
            id = int(id.lstrip('n'))
        try:
            val = self.nodes[id]
        except:
            raise InvalidRSpec("node ID %s not found" % id)
        return val
    
    def getNodes(self):
        nodes = []
        for n in self.nodes:
            nodes.append(self.nodes[n])
        return nodes
    
    """ Lookup iface based on id or idtag value """
    def lookupIface(self, id):
        val = None
        if isinstance(id, basestring):
            id = int(id.lstrip('i'))
        try:
            val = self.ifaces[id]
        except:
            raise InvalidRSpec("interface ID %s not found" % id)
        return val
    
    def getIfaces(self):
        ifaces = []
        for i in self.ifaces:
            ifaces.append(self.ifaces[i])
        return ifaces
    
    def nodesWithSlivers(self):
        nodes = []
        for n in self.nodes:
            node = self.nodes[n]
            if node.sliver:
                nodes.append(node)
        return nodes
            
    def lookupSliceTag(self, id):
        val = None
        try:
            val = self.tags[id]
        except:
            raise InvalidRSpec("slicetag ID %s not found" % id)
        return val
    
    def getSliceTags(self):
        tags = []
        for t in self.tags:
            tags.append(self.tags[t])
        return tags
    
    def lookupTagType(self, name):
        val = None
        try:
            val = self.tagstypes[name]
        except:
            raise InvalidRSpec("tag %s not found" % name)
        return val
    
    def getTagTypes(self):
        tags = []
        for t in self.tagtypes:
            tags.append(self.tagtypes[t])
        return tags
    
    def __process_attributes(self, element, node=None):
        # Do we need to check caller's role before update???
        tagtypes = self.getTagTypes()
        for tt in tagtypes:
            if tt.multi:
                for e in element.iterfind("./" + tt.tagname):
                    self.slice.update_multi_tag(tt.tagname, e.text, node)
            else:
                e = element.find("./" + tt.tagname)
                if e is not None:
                    self.slice.update_tag(tt.tagname, e.text, node)

    """
    Annotate the objects in the Network with information from the RSpec
    """
    def addRSpec(self, xml, schema=None):
        nodedict = {}
        for node in self.getNodes():
            nodedict[node.idtag] = node
            
        try:
            tree = etree.parse(StringIO(xml))
        except etree.XMLSyntaxError:
            message = str(sys.exc_info()[1])
            raise InvalidRSpec(message)

        if schema:
            # Validate the incoming request against the RelaxNG schema
            relaxng_doc = etree.parse(schema)
            relaxng = etree.RelaxNG(relaxng_doc)
        
            if not relaxng(tree):
                error = relaxng.error_log.last_error
                message = "%s (line %s)" % (error.message, error.line)
                raise InvalidRSpec(message)

        rspec = tree.getroot()

        defaults = rspec.find("./network/sliver_defaults")
        self.__process_attributes(defaults)

        # Find slivers under node elements
        for sliver in rspec.iterfind("./network/site/node/sliver"):
            elem = sliver.getparent()
            try:
                node = self.lookupNode(elem.get("id"))
            except:
                # Don't worry about nodes from other aggregates
                pass
            else:
                node.add_sliver()
                self.__process_attributes(sliver, node)

        # Find slivers that specify nodeid
        for sliver in rspec.iterfind("./request/sliver[@nodeid]"):
            try:
                node = self.lookupNode(sliver.get("nodeid"))
            except:
                # Don't worry about nodes from other aggregates
                pass
            else:
                node.add_sliver()
                self.__process_attributes(sliver, node)

        return

    """
    Annotate the objects in the Network with information from the slice
    """
    def addSlice(self):
        slice = self.slice
        if not slice:
            raise InvalidRSpec("no slice associated with network")

        for node in slice.get_nodes():
            node.add_sliver()

    """
    Write any slice tags that have been added or modified back to the DB
    """
    def updateSliceTags(self):
        # Update slice tags in database
        for tag in self.getSliceTags():
            if tag.slice_id == self.slice.id:
                if not tag.updated:
                    tag.delete()
                #tag.write(self.api)  ### Debugging

    """
    Produce XML directly from the topology specification.
    """
    def toxml(self):
        xml = XMLBuilder(format = True, tab_step = "  ")
        with xml.RSpec(type=self.type):
            name = "Public_" + self.type
            if self.slice:
                element = xml.network(name=name, slice=self.slice.hrn)
            else:
                element = xml.network(name=name)
                
            with element:
                if self.slice:
                    self.slice.toxml(xml)
                for site in self.getSites():
                    site.toxml(xml)

        header = '<?xml version="1.0"?>\n'
        return header + str(xml)

    """
    Create a dictionary of site objects keyed by site ID
    """
    def get_sites(self, api):
        tmp = []
        for site in api.plshell.GetSites(api.plauth, {'peer_id': None}):
            t = site['site_id'], Site(self, site)
            tmp.append(t)
        return dict(tmp)


    """
    Create a dictionary of node objects keyed by node ID
    """
    def get_nodes(self, api):
        tmp = []
        for node in api.plshell.GetNodes(api.plauth, {'peer_id': None}):
            t = node['node_id'], Node(self, node)
            tmp.append(t)
        return dict(tmp)

    """
    Create a dictionary of node objects keyed by node ID
    """
    def get_ifaces(self, api):
        tmp = []
        for iface in api.plshell.GetInterfaces(api.plauth):
            t = iface['interface_id'], Iface(self, iface)
            tmp.append(t)
        return dict(tmp)

    """
    Create a dictionary of slicetag objects keyed by slice tag ID
    """
    def get_slice_tags(self, api):
        tmp = []
        for tag in api.plshell.GetSliceTags(api.plauth):
            t = tag['slice_tag_id'], Slicetag(tag)
            tmp.append(t)
        return dict(tmp)
    
    """
    Create a list of tagtype obects keyed by tag name
    """
    def get_tag_types(self, api):
        tmp = []
        for tag in api.plshell.GetTagTypes(api.plauth):
            if tag['category'] == 'slice/rspec':
                t = tag['tagname'], TagType(tag)
                tmp.append(t)
        return dict(tmp)
    
    """
    Return a Slice object for a single slice
    """
    def get_slice(self, api, hrn):
        slicename = hrn_to_pl_slicename(hrn)
        slice = api.plshell.GetSlices(api.plauth, [slicename])
        if slice:
            self.slice = Slice(self, slicename, slice[0])
            return self.slice
        else:
            return None
    

