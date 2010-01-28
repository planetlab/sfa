from sfa.util.rspec import RSpec
from sfa.rspecs.aggregates.vini.utils import *
import sys

SFA_VINI_DEFAULT_RSPEC = '/etc/sfa/vini.rspec'

class ViniRSpec(RSpec):
    def __init__(self, xml = None, xsd = None, NSURL = None):
        RSpec.__init__(self, xml, xsd, NSURL)
        if not xml:
            self.parseFile(SFA_VINI_DEFAULT_RSPEC)
        
    def updateCapacity(self, topo):
        d = self.toDict()
        sitespecs = []
        sitelinkspecs = []
        for site in topo.getSites():
            if not site.public:
                continue
            sdict = {}
            nodespecs = []
            for node in site.get_sitenodes(topo.nodes):
                if not node.tag:
                    continue
                ndict = {}
                ndict['hostname'] = [node.hostname]
                ndict['name'] = node.tag
                ndict['kbps'] = [int(node.bps/1000)] 
                nodespecs.append(ndict)
            sdict['NodeSpec'] = nodespecs
            sdict['name'] = site.name
            sitespecs.append(sdict)
            
            for sl in site.links:
                if sl.end1 == site:
                    sldict = {}
                    sldict['endpoint'] = [sl.end1.name, sl.end2.name]
                    sldict['kbps'] = [int(sl.bps/1000)]
                    sitelinkspecs.append(sldict)
                    
        d['RSpec']['Capacity'][0]['NetSpec'][0]['SiteSpec'] = sitespecs
        d['RSpec']['Capacity'][0]['NetSpec'][0]['SiteLinkSpec'] = sitelinkspecs
        self.parseDict(d)


    def updateRequest(self, slice, topo):
        linkspecs = []
        for link in topo.nodelinks:
            edict = {}
            edict['endpoint'] = [link.end1.tag, link.end2.tag]
            edict['kbps'] = [int(link.bps/1000)]
            linkspecs.append(edict)

        d = self.toDict()
        d['RSpec']['Request'][0]['NetSpec'][0]['LinkSpec'] = linkspecs
        d['RSpec']['Request'][0]['NetSpec'][0]['name'] = slice.hrn
        self.parseDict(d)
