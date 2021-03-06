#
# SFA API faults
#

import xmlrpclib

class SfaFault(xmlrpclib.Fault):
    def __init__(self, faultCode, faultString, extra = None):
        if extra:
            faultString += ": " + str(extra)
        xmlrpclib.Fault.__init__(self, faultCode, faultString)

class SfaInvalidAPIMethod(SfaFault):
    def __init__(self, method, interface = None, extra = None):
        faultString = "Invalid method " + method
        if interface:
            faultString += " for interface " + interface
        SfaFault.__init__(self, 100, faultString, extra)

class SfaInvalidArgumentCount(SfaFault):
    def __init__(self, got, min, max = min, extra = None):
        if min != max:
            expected = "%d-%d" % (min, max)
        else:
            expected = "%d" % min
        faultString = "Expected %s arguments, got %d" % \
                      (expected, got)
        SfaFault.__init__(self, 101, faultString, extra)

class SfaInvalidArgument(SfaFault):
    def __init__(self, extra = None, name = None):
        if name is not None:
            faultString = "Invalid %s value" % name
        else:
            faultString = "Invalid argument"
        SfaFault.__init__(self, 102, faultString, extra)

class SfaAuthenticationFailure(SfaFault):
    def __init__(self, extra = None):
        faultString = "Failed to authenticate call"
        SfaFault.__init__(self, 103, faultString, extra)

class SfaDBError(SfaFault):
    def __init__(self, extra = None):
        faultString = "Database error"
        SfaFault.__init__(self, 106, faultString, extra)

class SfaPermissionDenied(SfaFault):
    def __init__(self, extra = None):
        faultString = "Permission denied"
        SfaFault.__init__(self, 108, faultString, extra)

class SfaNotImplemented(SfaFault):
    def __init__(self, interface=None, extra = None):
        faultString = "Not implemented"
        if interface:
            faultString += " at interface " + interface 
        SfaFault.__init__(self, 109, faultString, extra)

class SfaAPIError(SfaFault):
    def __init__(self, extra = None):
        faultString = "Internal API error"
        SfaFault.__init__(self, 111, faultString, extra)

class MalformedHrnException(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Malformed HRN: %(value)s" % locals()
        SfaFault.__init__(self, 102, faultString, extra)
    def __str__(self):
        return repr(self.value)

class TreeException(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Tree Exception: %(value)s, " % locals()
        SfaFault.__init__(self, 111, faultString, extra)
    def __str__(self):
        return repr(self.value)

class NonExistingRecord(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Non exsiting record %(value)s, " % locals()
        SfaFault.__init__(self, 111, faultString, extra)
    def __str__(self):
        return repr(self.value)

class ExistingRecord(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Existing record: %(value)s, " % locals()
        SfaFault.__init__(self, 111, faultString, extra)
    def __str__(self):
        return repr(self.value)

    
class NonexistingCredType(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Non existing record: %(value)s, " % locals()
        SfaFault.__init__(self, 111, faultString, extra)
    def __str__(self):
        return repr(self.value)

class NonexistingFile(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Non existing file: %(value)s, " % locals()
        SfaFault.__init__(self, 111, faultString, extra)
    def __str__(self):
        return repr(self.value)

class InvalidRPCParams(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Invalid RPC Params: %(value)s, " % locals()
        SfaFault.__init__(self, 102, faultString, extra)
    def __str__(self):
        return repr(self.value)

# SMBAKER exceptions follow

class ConnectionKeyGIDMismatch(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Connection Key GID mismatch: %(value)s" % locals()
        SfaFault.__init__(self, 102, faultString, extra) 
    def __str__(self):
        return repr(self.value)

class MissingCallerGID(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Missing Caller GID: %(value)s" % locals()
        SfaFault.__init__(self, 102, faultString, extra) 
    def __str__(self):
        return repr(self.value)

class RecordNotFound(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Record not found: %(value)s" % locals()
        SfaFault.__init__(self, 102, faultString, extra)
    def __str__(self):
        return repr(self.value)

class UnknownSfaType(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Unknown SFA Type: %(value)s" % locals()
        SfaFault.__init__(self, 102, faultString, extra)
    def __str__(self):
        return repr(self.value)

class MissingAuthority(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Missing authority: %(value)s" % locals()
        SfaFault.__init__(self, 102, faultString, extra)
    def __str__(self):
        return repr(self.value)

class PlanetLabRecordDoesNotExist(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "PlanetLab record does not exist : %(value)s" % locals()
        SfaFault.__init__(self, 102, faultString, extra)
    def __str__(self):
        return repr(self.value)

class PermissionError(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Permission error: %(value)s" % locals()
        SfaFault.__init__(self, 108, faultString, extra)
    def __str__(self):
        return repr(self.value)

class InsufficientRights(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Insufficient rights: %(value)s" % locals()
        SfaFault.__init__(self, 108, faultString, extra)
    def __str__(self):
        return repr(self.value)

class MissingDelegateBit(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Missing delegate bit: %(value)s" % locals()
        SfaFault.__init__(self, 108, faultString, extra)
    def __str__(self):
        return repr(self.value)

class ChildRightsNotSubsetOfParent(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Child rights not subset of parent: %(value)s" % locals()
        SfaFault.__init__(self, 103, faultString, extra)
    def __str__(self):
        return repr(self.value)

class CertMissingParent(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Cert missing parent: %(value)s" % locals()
        SfaFault.__init__(self, 103, faultString, extra)
    def __str__(self):
        return repr(self.value)

class CertNotSignedByParent(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Cert not signed by parent: %(value)s" % locals()
        SfaFault.__init__(self, 103, faultString, extra)
    def __str__(self):
        return repr(self.value)
    
class GidParentHrn(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Cert URN is not an extension of its parent: %(value)s" % locals()
        SfaFault.__init__(self, 103, faultString, extra)
    def __str__(self):
        return repr(self.value)
        
class GidInvalidParentHrn(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "GID invalid parent hrn: %(value)s" % locals()
        SfaFault.__init__(self, 102, faultString, extra)
    def __str__(self):
        return repr(self.value)

class SliverDoesNotExist(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Sliver does not exist : %(value)s" % locals()
        SfaFault.__init__(self, 102, faultString, extra)
    def __str__(self):
        return repr(self.value)

class BadRequestHash(xmlrpclib.Fault):
    def __init__(self, hash = None, extra = None):
        faultString = "bad request hash: " + str(hash)
        xmlrpclib.Fault.__init__(self, 902, faultString)

class MissingTrustedRoots(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Trusted root directory does not exist: %(value)s" % locals()
        SfaFault.__init__(self, 102, faultString, extra) 
    def __str__(self):
        return repr(self.value)

class MissingSfaInfo(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Missing information: %(value)s" % locals()
        SfaFault.__init__(self, 102, faultString, extra) 
    def __str__(self):
        return repr(self.value)

class InvalidRSpec(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Invalid RSpec: %(value)s" % locals()
        SfaFault.__init__(self, 108, faultString, extra)
    def __str__(self):
        return repr(self.value)

class InvalidRSpecElement(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Invalid RSpec Element: %(value)s" % locals()
        SfaFault.__init__(self, 108, faultString, extra)
    def __str__(self):
        return repr(self.value)

class AccountNotEnabled(SfaFault):
    def __init__(self,  extra = None):
        faultString = "Account Disabled"
        SfaFault.__init__(self, 108, faultString, extra)
    def __str__(self):
        return repr(self.value)

class CredentialNotVerifiable(SfaFault):
    def __init__(self, value, extra = None):
        self.value = value
        faultString = "Unable to verify credential: %(value)s, " %locals()
        SfaFault.__init__(self, 115, faultString, extra)
    def __str__(self):
        return repr(self.value)

class CertExpired(SfaFault):
    def __init__(self, value, extra=None):
        self.value = value
        faultString = "%s cert is expired" % value
        SfaFault.__init__(self, 102, faultString, extra)
   
