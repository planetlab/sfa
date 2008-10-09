class GacksError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class GacksMultipleRecordCollision(GacksError):
    pass

class GacksResourceNotFound(GacksError):
    pass

class GacksConflictingInsert(GacksError):
    pass
