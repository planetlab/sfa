import re

from sfa.util.faults import *
from sfa.util.sfalogging import sfa_logger

# for convenience and smoother translation
def get_leaf(hrn): return Xrn(hrn=hrn,type='any').get_leaf()
def get_authority(hrn): return Xrn(hrn=hrn,type='any').get_authority_hrn()
def urn_to_hrn(urn): xrn=Xrn(urn=urn); return (xrn.hrn, xrn.type)
def hrn_to_urn(hrn,type): return Xrn(hrn=hrn, type=type).urn

class Xrn:

    ########## basic tools on HRNs
    # split a HRN-like string into pieces
    # this is like split('.') except for escaped (backslashed) dots
    # e.g. hrn_split ('a\.b.c.d') -> [ 'a\.b','c','d']
    @staticmethod
    def hrn_split(hrn):
        return [ x.replace('--sep--','\\.') for x in hrn.replace('\\.','--sep--').split('.') ]

    # e.g. hrn_leaf ('a\.b.c.d') -> 'd'
    @staticmethod
    def hrn_leaf(hrn): return Xrn.hrn_split(hrn)[-1]

    # e.g. hrn_path_list ('a\.b.c.d') -> ['a\.b', 'c']
    @staticmethod
    def hrn_path_list(hrn): return Xrn.hrn_split(hrn)[0:-1]
    
    # e.g. hrn_path ('a\.b.c.d') -> 'a\.b.c'
    @staticmethod
    def hrn_path(hrn): return '.'.join(Xrn.hrn_path_list(hrn))
    
    # e.g. escape ('a.b') -> 'a\.b'
    @staticmethod
    def escape(token): return re.sub(r'([^\\])\.', r'\1\.', token)
    # e.g. unescape ('a\.b') -> 'a.b'
    @staticmethod
    def unescape(token): return token.replace('\\.','.')
        
    URN_PREFIX = "urn:publicid:IDN"

    ########## basic tools on URNs
    @staticmethod
    def urn_full (urn):
        if urn.startswith(Xrn.URN_PREFIX): return urn
        else: return Xrn.URN_PREFIX+URN
    @staticmethod
    def urn_meaningful (urn):
        if urn.startswith(Xrn.URN_PREFIX): return urn[len(Xrn.URN_PREFIX):]
        else: return urn
    @staticmethod
    def urn_split (urn):
        return Xrn.urn_meaningful(urn).split('+')

    # provide either urn, or (hrn + type)
    def __init__ (self, urn=None, hrn=None, type=None):
        if urn: 
            self.urn=urn
            self.urn_to_hrn()
        elif hrn and type: 
            self.hrn=hrn
            self.type=type
            self.hrn_to_urn()
        else:
            raise SfaAPIError,"Xrn.__init__"

    def get_urn(self): return self.urn
    def get_hrn(self): return (self.hrn, self.type)

    def get_leaf(self):
        if not self.hrn: raise SfaAPIError, "Xrn.get_leaf"
        if not hasattr(self,'leaf'): 
            self.leaf=Xrn.hrn_split(self.hrn)[-1]
        return self.leaf

    def get_authority_hrn(self): 
        if not self.hrn: raise SfaAPIError, "Xrn.get_authority_hrn"
        # self.authority keeps a list
        if not hasattr(self,'authority'): 
            self.authority=Xrn.hrn_path_list(self.hrn)
        return '.'.join( self.authority )
    
    def get_authority_urn(self): 
        if not self.hrn: raise SfaAPIError, "Xrn.get_authority_urn"
        # self.authority keeps a list
        if not hasattr(self,'authority'): 
            self.authority=Xrn.hrn_path_list(self.hrn)
        return ':'.join( [Xrn.unescape(x) for x in self.authority] )
    
    def urn_to_hrn(self):
        """
        compute tuple (hrn, type) from urn
        """
        
        if not self.urn or not self.urn.startswith(Xrn.URN_PREFIX):
            raise SfaAPIError, "Xrn.urn_to_hrn"

        parts = Xrn.urn_split(self.urn)
        type=parts.pop(2)
        # Remove the authority name (e.g. '.sa')
        if type == 'authority': parts.pop()

        # convert parts (list) into hrn (str) by doing the following
        # 1. remove blank parts
        # 2. escape dots inside parts
        # 3. replace ':' with '.' inside parts
        # 3. join parts using '.' 
        hrn = '.'.join([Xrn.escape(part).replace(':','.') for part in parts if part]) 

        self.hrn=str(hrn)
        self.type=str(type)
    
    def hrn_to_urn(self):
        """
        compute urn from (hrn, type)
        """

        if not self.hrn or self.hrn.startswith(Xrn.URN_PREFIX):
            raise SfaAPIError, "Xrn.hrn_to_urn"

        if self.type == 'authority':
            self.authority = Xrn.hrn_split(self.hrn)
            name = 'sa'   
        else:
            self.authority = Xrn.hrn_path_list(self.hrn)
            name = Xrn.hrn_leaf(self.hrn)

        authority_string = self.get_authority_urn()

        if self.type == None:
            urn = "+".join(['',authority_string,name])
        else:
            urn = "+".join(['',authority_string,self.type,name])
        
        self.urn = Xrn.URN_PREFIX + urn

    def dump_string(self):
        result="-------------------- XRN\n"
        result += "URN=%s\n"%self.urn
        result += "HRN=%s\n"%self.hrn
        result += "TYPE=%s\n"%self.type
        result += "LEAF=%s\n"%self.get_leaf()
        result += "AUTH(hrn format)=%s\n"%self.get_authority_hrn()
        result += "AUTH(urn format)=%s\n"%self.get_authority_urn()
        return result
        
