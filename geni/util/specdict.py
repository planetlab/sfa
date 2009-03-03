##
# SpecDict
#
# SpecDict defines a means for converting a dictionary with plc specific keys
# to a dict with rspec specific keys. 
#
# SpecDict.fields dict defines all the rspec specific attribute and their 
# expected type. 
# 
# SpecDict.plc_fields defines a one to one mapping of plc attribute to rspec 
# attribute

from types import StringTypes, ListType


class SpecDict(dict):
    """
    Base class of SpecDict objects. 
    """
    fields = {}
    plc_fields = {}
    type = None
        
    def __init__(self, spec_dict):
        # convert plc dict and initialize self
        sdict = self.plcToSpec(spec_dict)
        dict.__init__(self, sdict)


    def plcToSpec(self, spec_dict):
        """
        Defines how to convert a plc dict to rspec dict
        """
        spec = {}
        for field in self.fields:
            value = ""
            expected = self.fields[field]
            if isinstance(expected, StringTypes):
                if self.plc_fields.has_key(field):
                    plc_field = self.plc_fields[field]
                    if spec_dict.has_key(plc_field):
                        value = spec_dict[plc_field]
            elif isinstance(expected, ListType):
                expected = expected[0]
                if self.plc_fields.has_key(field):
                    plc_field = self.plc_fields[field]
                    if spec_dict.has_key(plc_field):
                        value = [expected(value) for value in spec_dict[plc_field]]
            spec[field] = value
        return {self.type: spec}
    
class IfSpecDict(SpecDict):
    type = 'IfSpec'
    fields = {'name': '',
              'addr': '',
              'type': '',
              'init_params': '',
              'min_rate': '',
              'max_rate': '',
              'max_kbyte': '',
              'ip_spoof': ''}
    plc_fields = {'name': 'is_primary',
                 'addr': 'ip',
                 'type': 'type'}
 
class LinkSpecDict(SpecDict):
    type = 'IfSpec'
    fields = {'name': '',
              'addr': '',
              'type': '',
              'init_params': '',
              'min_rate': '',
              'max_rate': '',
              'max_kbyte': ''}
    plc_fields = {}
                 
            
class NodeSpecDict(SpecDict):
    type = 'NodeSpec'
    fields = {'name': '',
              'type': '',
              'init_params': '',
              'cpu_min': '',
              'cpu_share': '',
              'cpu_pct': '',
              'disk_max': '',
              'start_time': '',
              'duration': '',
              'net_if': [IfSpecDict]}

    plc_fields = {'name': 'hostname',
                  'net_if': 'interfaces'}  

class NetSpecDict(SpecDict):
    type = 'NetSpec'
    fields = {'name': '',
              'start_time': '',
              'duration': '',
              'nodes': [NodeSpecDict],
             }
    plc_fields = {'name': 'name',
                  'start_time': 'start_time',
                  'duration': 'duration',
                  'nodes': 'nodes'}

class RspecDict(SpecDict):
    type = 'RSpec'
    fields = {'start_time': '',
              'duration': '',
              'networks': [NetSpecDict]
             }
    plc_fields = {'networks': 'networks',
                  'start_time': 'start_tim',
                  'duration': 'duration'
                 }

# vim:ts=4:expandtab
