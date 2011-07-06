from sfa.rspecs.elements.networks import Network

class PGv2Network(Network):

    def get_networks_names(self):
        networks = self.xml.xpath('//rspecv2:node[@component_manager_id]/@component_manager_id', namespaces=self.namespaces)
        return list(set(networks))
