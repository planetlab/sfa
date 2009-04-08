#
# GeniAPI XML-RPC faults
#
#

import xmlrpclib

class GeniFault(xmlrpclib.Fault):
    def __init__(self, faultCode, faultString, extra = None):
        if extra:
            faultString += ": " + extra
        xmlrpclib.Fault.__init__(self, faultCode, faultString)

class GeniInvalidAPIMethod(GeniFault):
    def __init__(self, method, role = None, extra = None):
        faultString = "Invalid method " + method
        if role:
            faultString += " for role " + role
        GeniFault.__init__(self, 100, faultString, extra)

class GeniInvalidArgumentCount(GeniFault):
    def __init__(self, got, min, max = min, extra = None):
        if min != max:
            expected = "%d-%d" % (min, max)
        else:
            expected = "%d" % min
        faultString = "Expected %s arguments, got %d" % \
                      (expected, got)
        GeniFault.__init__(self, 101, faultString, extra)

class GeniInvalidArgument(GeniFault):
    def __init__(self, extra = None, name = None):
        if name is not None:
            faultString = "Invalid %s value" % name
        else:
            faultString = "Invalid argument"
        GeniFault.__init__(self, 102, faultString, extra)

class GeniAuthenticationFailure(GeniFault):
    def __init__(self, extra = None):
        faultString = "Failed to authenticate call"
        GeniFault.__init__(self, 103, faultString, extra)

class GeniDBError(GeniFault):
    def __init__(self, extra = None):
        faultString = "Database error"
        GeniFault.__init__(self, 106, faultString, extra)

class GeniPermissionDenied(GeniFault):
    def __init__(self, extra = None):
        faultString = "Permission denied"
        GeniFault.__init__(self, 108, faultString, extra)

class GeniNotImplemented(GeniFault):
    def __init__(self, extra = None):
        faultString = "Not fully implemented"
        GeniFault.__init__(self, 109, faultString, extra)

class GeniAPIError(GeniFault):
    def __init__(self, extra = None):
        faultString = "Internal API error"
        GeniFault.__init__(self, 111, faultString, extra)
