import geni.methods


methods = geni.methods.all

def callable(method):
    classname = method.split(".")[-1]
    module = __import__("geni.methods." + method, globals(), locals(), [classname])
    callablemethod = getattr(module, classname)(None)
    return getattr(module, classname)(None)


