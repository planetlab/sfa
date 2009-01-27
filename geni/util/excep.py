
class MalformedHrnException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class TreeException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class NonexistingRecord(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ExistingRecord(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
        
class NonexistingCredType(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class NonexistingFile(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class InvalidRPCParams(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

# SMBAKER exceptions follow

class ConnectionKeyGIDMismatch(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class MissingCallerGID(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RecordNotFound(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class UnknownGeniType(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class MissingAuthority(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class PlanetLabRecordDoesNotExist(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class PermissionError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class InsufficientRights(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class MissingDelegateBit(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ChildRightsNotSubsetOfParent(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class CertMissingParent(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class CertNotSignedByParent(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class GidInvalidParentHrn(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class SliverDoesNotExist(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

