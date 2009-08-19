from sfa.util.rspec import Rspec
from sfa.rspecs.aggregates.vini.utils import *
import sys

SFA_VINI_DEFAULT_RSPEC = '/etc/sfa/vini.rspec'

class ViniRspec(Rspec):
    def __init__(self):
        Rspec.__init__(self)
        self.parseFile(SFA_VINI_DEFAULT_RSPEC)
        
    def updateCapacity(self, sites, nodes):
        d = self.toDict()
        sitespecs = []
        sitelinkspecs = []
        for s in sites:
            site = sites[s]
            if not site.public:
                continue
            sdict = {}
            nodespecs = []
            for node in site.get_sitenodes(nodes):
                if not node.tag:
                    continue
                ndict = {}
                ndict['hostname'] = [node.hostname]
                ndict['name'] = node.tag
                ndict['bw'] = ['999Mbit']
                nodespecs.append(ndict)
            sdict['NodeSpec'] = nodespecs
            sdict['name'] = site.name
            sitespecs.append(sdict)
            
            for sl in site.sitelinks:
                if sl.site1 == site:
                    sldict = {}
                    sldict['endpoint'] = [sl.site1.name, sl.site2.name]
                    sldict['bw'] = [str(sl.availMbps) + "Mbit"]
                    sitelinkspecs.append(sldict)
                    
        d['Rspec']['Capacity'][0]['NetSpec'][0]['SiteSpec'] = sitespecs
        d['Rspec']['Capacity'][0]['NetSpec'][0]['SiteLinkSpec'] = sitelinkspecs
        self.parseDict(d)


    def updateRequest(self, slice, nodes, tags):
        endpoints = []
        for node in slice.get_nodes(nodes):
            linktag = slice.get_tag('topo_rspec', tags, node)
            if linktag:
                l = eval(linktag.value)
                for (id, realip, bw, lvip, rvip, vnet) in l:
                    endpoints.append((node.id, id, bw))
            
        if endpoints:
            linkspecs = []
            for (l, r, bw) in endpoints:
                if (r, l, bw) in endpoints:
                    if l < r:
                        edict = {}
                        edict['endpoint'] = [nodes[l].tag, nodes[r].tag]
                        edict['bw'] = [bw]
                        linkspecs.append(edict)

            d = self.toDict()
            d['Rspec']['Request'][0]['NetSpec'][0]['LinkSpec'] = linkspecs
            d['Rspec']['Request'][0]['NetSpec'][0]['name'] = slice.hrn
            self.parseDict(d)