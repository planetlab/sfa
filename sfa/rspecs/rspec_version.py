#!/usr/bin/python
from sfa.util.sfalogging import _SfaLogger


class RSpecVersion:

    format = 'sfa'
    version = '1'
    schema = None
    namespace = None
    extensions = []

    def __init__(self, version_string):
        self.logger = _SfaLogger('/var/log/sfa.log') 
        self.parse_version_string(version_string)

    def parse_version_string(self, version_string):
        # version_raw is currently a string but will 
        # eventually be a struct.
        format_split = version_string.split(' ')
        try: self.format = format_split[0].lower()  
        except: pass
        try: self.version = format_split[1]
        except: pass
    

    def parse_version_struct(self, version_struct):
        try:
            pass
        except:
            pass
