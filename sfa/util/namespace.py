### $Id: namespace.py 15020 2009-09-14 23:11:37Z tmack $
### $URL: https://svn.planet-lab.org/svn/sfa/trunk/sfa/util/namespace.py $

from sfa.util.faults import *

URN_PREFIX = "urn:publicid:IDN"

def get_leaf(hrn):
    parts = hrn.split(".")
    return ".".join(parts[-1:])

def get_authority(hrn):
    parts = hrn.split(".")
    return ".".join(parts[:-1])

def hrn_to_pl_slicename(hrn):
    parts = hrn.split(".")
    return parts[-2] + "_" + parts[-1]

# assuming hrn is the hrn of an authority, return the plc authority name
def hrn_to_pl_authname(hrn):
    parts = hrn.split(".")
    return parts[-1]

# assuming hrn is the hrn of an authority, return the plc login_base
def hrn_to_pl_login_base(hrn):
    return hrn_to_pl_authname(hrn)

def hostname_to_hrn(auth_hrn, login_base, hostname):
    """
    Convert hrn to plantelab name.
    """
    genihostname = ".".join([auth_hrn, login_base, hostname.split(".")[0]])
    return genihostname

def slicename_to_hrn(auth_hrn, slicename):
    """
    Convert hrn to planetlab name.
    """
    parts = slicename.split("_")
    slice_hrn = ".".join([auth_hrn, parts[0]]) + "." + "_".join(parts[1:])

    return slice_hrn

def email_to_hrn(auth_hrn, email):
    parts = email.split("@")
    username = parts[0]
    username = username.replace(".", "_") 
    person_hrn = ".".join([auth_hrn, username])
    
    return person_hrn 

def urn_to_hrn(urn):
    """
    convert a urn to hrn
    return a tuple (hrn, type)
    """

    # if this is already a hrn dont do anything
    if not urn.startswith(URN_PREFIX):
        return urn, None
    name = urn[len(URN_PREFIX):]
    hrn_parts = name.split("+")
    
    # type is always the second to last element in the list
    type = hrn_parts.pop(-2)

    # convert hrn_parts (list) into hrn (str) by doing the following    
    # remove blank elements
    # replace ':' with '.'
    # join list elements using '.'
    hrn = '.'.join([part.replace(':', '.') for part in hrn_parts if part]) 
   
    return hrn, type 
    
    
def hrn_to_urn(hrn, type=None):
    """
    convert an hrn and type to a urn string
    """
    # if  this is already a urn dont do anything 
    if hrn.startswith(URN_PREFIX):
        return hrn

    authority = get_authority(hrn)
    name = get_leaf(hrn)
    urn = "+".join([unicode(part).replace('.', ':') \
                    for part in ['',authority,type,name]])

    return URN_PREFIX + urn
