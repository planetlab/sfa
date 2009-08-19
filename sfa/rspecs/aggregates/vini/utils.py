import re
import socket
from sfa.rspecs.aggregates.vini.topology import *

# Taken from bwlimit.py
#
# See tc_util.c and http://physics.nist.gov/cuu/Units/binary.html. Be
# warned that older versions of tc interpret "kbps", "mbps", "mbit",
# and "kbit" to mean (in this system) "kibps", "mibps", "mibit", and
# "kibit" and that if an older version is installed, all rates will
# be off by a small fraction.
suffixes = {
    "":         1,
    "bit":	1,
    "kibit":	1024,
    "kbit":	1000,
    "mibit":	1024*1024,
    "mbit":	1000000,
    "gibit":	1024*1024*1024,
    "gbit":	1000000000,
    "tibit":	1024*1024*1024*1024,
    "tbit":	1000000000000,
    "bps":	8,
    "kibps":	8*1024,
    "kbps":	8000,
    "mibps":	8*1024*1024,
    "mbps":	8000000,
    "gibps":	8*1024*1024*1024,
    "gbps":	8000000000,
    "tibps":	8*1024*1024*1024*1024,
    "tbps":	8000000000000
}


def get_tc_rate(s):
    """
    Parses an integer or a tc rate string (e.g., 1.5mbit) into bits/second
    """

    if type(s) == int:
        return s
    m = re.match(r"([0-9.]+)(\D*)", s)
    if m is None:
        return -1
    suffix = m.group(2).lower()
    if suffixes.has_key(suffix):
        return int(float(m.group(1)) * suffixes[suffix])
    else:
        return -1


class Node:
    def __init__(self, node):
        self.id = node['node_id']
        self.hostname = node['hostname']
        self.shortname = self.hostname.replace('.vini-veritas.net', '')
        self.site_id = node['site_id']
        self.ipaddr = socket.gethostbyname(self.hostname)
        self.links = []

    def get_link_id(self, remote):
        if self.id < remote.id:
            link = (self.id<<7) + remote.id
        else:
            link = (remote.id<<7) + self.id
        return link
        
    def get_iface_id(self, remote):
        if self.id < remote.id:
            iface = 1
        else:
            iface = 2
        return iface
    
    def get_virt_ip(self, remote):
        link = self.get_link_id(remote)
        iface = self.get_iface_id(remote)
        first = link >> 6
        second = ((link & 0x3f)<<2) + iface
        return "192.168.%d.%d" % (first, second)

    def get_virt_net(self, remote):
        link = self.get_link_id(remote)
        first = link >> 6
        second = (link & 0x3f)<<2
        return "192.168.%d.%d/30" % (first, second)
        
    def get_site(self, sites):
        return sites[self.site_id]
    
    def init_links(self):
        self.links = []
        
    def add_link(self, remote, bw):
        my_ip = self.get_virt_ip(remote)
        remote_ip = remote.get_virt_ip(self)
        net = self.get_virt_net(remote)
        link = remote.id, remote.ipaddr, bw, my_ip, remote_ip, net
        self.links.append(link)
        
    def add_tag(self, sites):
        s = self.get_site(sites)
        words = self.hostname.split(".")
        index = words[0].replace("node", "")
        if index.isdigit():
            self.tag = s.tag + index
        else:
            self.tag = None
        

class SiteLink:
    def __init__(self, site1, site2, mbps = 1000):
        self.site1 = site1
        self.site2 = site2
        self.totalMbps = mbps
        self.availMbps = mbps
        
        site1.add_sitelink(self)
        site2.add_sitelink(self)
        
        
class Site:
    def __init__(self, site):
        self.id = site['site_id']
        self.node_ids = site['node_ids']
        self.name = site['abbreviated_name']
        self.tag = site['login_base']
        self.public = site['is_public']
        self.sitelinks = []

    def get_sitenodes(self, nodes):
        n = []
        for i in self.node_ids:
            n.append(nodes[i])
        return n
    
    def add_sitelink(self, link):
        self.sitelinks.append(link)
    
    
class Slice:
    def __init__(self, slice):
        self.id = slice['slice_id']
        self.name = slice['name']
        self.node_ids = set(slice['node_ids'])
        self.slice_tag_ids = slice['slice_tag_ids']
    
    def get_tag(self, tagname, slicetags, node = None):
        for i in self.slice_tag_ids:
            tag = slicetags[i]
            if tag.tagname == tagname:
                if (not node) or (node.id == tag.node_id):
                    return tag
        else:
            return None
        
    def get_nodes(self, nodes):
        n = []
        for id in self.node_ids:
            n.append(nodes[id])
        return n
             
    
    # Add a new slice tag   
    def add_tag(self, tagname, value, slicetags, node = None):
        record = {'slice_tag_id':None, 'slice_id':self.id, 'tagname':tagname, 'value':value}
        if node:
            record['node_id'] = node.id
        else:
            record['node_id'] = None
        tag = Slicetag(record)
        slicetags[tag.id] = tag
        self.slice_tag_ids.append(tag.id)
        tag.changed = True       
        tag.updated = True
        return tag
    
    # Update a slice tag if it exists, else add it             
    def update_tag(self, tagname, value, slicetags, node = None):
        tag = self.get_tag(tagname, slicetags, node)
        if tag and tag.value == value:
            value = "no change"
        elif tag:
            tag.value = value
            tag.changed = True
        else:
            tag = self.add_tag(tagname, value, slicetags, node)
        tag.updated = True
            
    def assign_egre_key(self, slicetags):
        if not self.get_tag('egre_key', slicetags):
            try:
                key = free_egre_key(slicetags)
                self.update_tag('egre_key', key, slicetags)
            except:
                # Should handle this case...
                pass
        return
            
    def turn_on_netns(self, slicetags):
        tag = self.get_tag('netns', slicetags)
        if (not tag) or (tag.value != '1'):
            self.update_tag('netns', '1', slicetags)
        return
   
    def turn_off_netns(self, slicetags):
        tag = self.get_tag('netns', slicetags)
        if tag and (tag.value != '0'):
            tag.delete()
        return
    
    def add_cap_net_admin(self, slicetags):
        tag = self.get_tag('capabilities', slicetags)
        if tag:
            caps = tag.value.split(',')
            for cap in caps:
                if cap == "CAP_NET_ADMIN":
                    return
            else:
                newcaps = "CAP_NET_ADMIN," + tag.value
                self.update_tag('capabilities', newcaps, slicetags)
        else:
            self.add_tag('capabilities', 'CAP_NET_ADMIN', slicetags)
        return
    
    def remove_cap_net_admin(self, slicetags):
        tag = self.get_tag('capabilities', slicetags)
        if tag:
            caps = tag.value.split(',')
            newcaps = []
            for cap in caps:
                if cap != "CAP_NET_ADMIN":
                    newcaps.append(cap)
            if newcaps:
                value = ','.join(newcaps)
                self.update_tag('capabilities', value, slicetags)
            else:
                tag.delete()
        return

    # Update the vsys/setup-link and vsys/setup-nat slice tags.
    def add_vsys_tags(self, slicetags):
        link = nat = False
        for i in self.slice_tag_ids:
            tag = slicetags[i]
            if tag.tagname == 'vsys':
                if tag.value == 'setup-link':
                    link = True
                elif tag.value == 'setup-nat':
                    nat = True
        if not link:
            self.add_tag('vsys', 'setup-link', slicetags)
        if not nat:
            self.add_tag('vsys', 'setup-nat', slicetags)
        return


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


"""
Create a dictionary of site objects keyed by site ID
"""
def get_sites(api):
    tmp = []
    for site in api.plshell.GetSites(api.plauth):
        t = site['site_id'], Site(site)
        tmp.append(t)
    return dict(tmp)


"""
Create a dictionary of node objects keyed by node ID
"""
def get_nodes(api):
    tmp = []
    for node in api.plshell.GetNodes(api.plauth):
        t = node['node_id'], Node(node)
        tmp.append(t)
    return dict(tmp)

"""
Create a dictionary of slice objects keyed by slice ID
"""
def get_slice(api, slicename):
    slice = api.plshell.GetSlices(api.plauth, [slicename])
    if slice:
        return Slice(slice[0])
    else:
        return None

"""
Create a dictionary of slicetag objects keyed by slice tag ID
"""
def get_slice_tags(api):
    tmp = []
    for tag in api.plshell.GetSliceTags(api.plauth):
        t = tag['slice_tag_id'], Slicetag(tag)
        tmp.append(t)
    return dict(tmp)
    
"""
Find a free EGRE key
"""
def free_egre_key(slicetags):
    used = set()
    for i in slicetags:
        tag = slicetags[i]
        if tag.tagname == 'egre_key':
            used.add(int(tag.value))
                
    for i in range(1, 256):
        if i not in used:
            key = i
            break
    else:
        raise KeyError("No more EGRE keys available")
        
    return "%s" % key
   
"""
Return the network topology.
The topology consists of:
* a dictionary mapping site IDs to Site objects
* a dictionary mapping node IDs to Node objects
* the Site objects are connected via SiteLink objects representing
  the physical topology and available bandwidth
"""
def get_topology(api):
    sites = get_sites(api)
    nodes = get_nodes(api)
    tags = get_slice_tags(api)
    
    for (s1, s2) in PhysicalLinks:
        SiteLink(sites[s1], sites[s2])

    for id in nodes:
        nodes[id].add_tag(sites)
        
    return (sites, nodes, tags)
