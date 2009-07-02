### $Id$
### $URL$

from faults import *

SR_SUFFIX = '_srr'
CR_SUFFIX = '_crr'

global_sr_tree = None
global_cr_tree = None

def set_tree_globals(tree1, tree2):
    global global_sr_tree
    global global_cr_tree
    global_sr_tree = tree1
    global_cr_tree = tree2

def get_tree_globals():
    return (global_sr_tree, global_cr_tree)
    
#function converts a hierarchical name from geni format to array of strings
def geni_to_arr(name):        
    arrayName = []
    try:
        parts = name.split(".")
        for i in range(len(parts)):
            arrayName.append(parts[i])
        return arrayName
    except:
        raise MalformedHrnException(name)

#used to parse the function name and the parameters specified in "operation_request"
def msg_to_params(str):        
    try:
        return eval(str)
    except:
        raise InvalidRPCParams(str)

#returns the authority hrn of a given 'hrn'
def obtain_authority(hrn):
	parts = hrn.split(".")
	auth_str = ''
	if len(parts) > 1:
		auth_str = parts[0]+''
		for i in range(1, len(parts)-1):
			auth_str = auth_str + '.' + parts[i]
	return auth_str

#returns the last element of an hrn
def get_leaf(hrn):
    parts = hrn.split(".")
    return parts[len(parts)-1]

#checks whether the 'hrn_auth' is an authority of 'hrn'
def check_authority(hrn, hrn_auth):
    arr = geni_to_arr(hrn)
    arr_auth = geni_to_arr(hrn_auth)
    try:
        for i in range(len(arr_auth)):
            if arr[i] != arr_auth[i]:
                return False
    except: 
        return False
    return True
    
def hrn_to_tablename(hrn,type):
    hrn = hrn.replace(".","$")
    if type == 'slc':
        hrn = hrn + SR_SUFFIX
    else:
        hrn = hrn + CR_SUFFIX
    return  hrn
    
