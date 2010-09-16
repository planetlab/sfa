import sfa.methods


methods = sfa.methods.all

def callable(method):
    classname = method.split(".")[-1]
    module = __import__("sfa.methods." + method, globals(), locals(), [classname])
    callablemethod = getattr(module, classname)(None)
    return getattr(module, classname)(None)


