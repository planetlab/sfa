"""
Returns the request context required by sfatables. At some point, this mechanism should be changed
to refer to "contexts", which is the information that sfatables is requesting. But for now, we just
return the basic information needed in a dict.
"""
def fetch_context(slice_hrn, user_hrn, contexts):
    base_context = {'sfa':{'user':{'hrn':user_hrn}}}
    return base_context
