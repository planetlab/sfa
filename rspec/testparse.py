"""Read in a DOM instance, convert it to a Python object
"""
from xml.dom.utils import FileReader

class PyObject: pass

def pyobj_printer(py_obj, level=0):
    """Return a "deep" string description of a Python object"""
    from string import join, split
    import types
    descript = ''
    for membname in dir(py_obj):
        member = getattr(py_obj,membname)
        if type(member) == types.InstanceType:
            descript = descript + (' '*level) + '{'+membname+'}\n'
            descript = descript + pyobj_printer(member, level+3)
        elif type(member) == types.ListType:
            descript = descript + (' '*level) + '['+membname+']\n'
            for i in range(len(member)):
                descript = descript+(' '*level)+str(i+1)+': '+ \
                           pyobj_printer(member[i],level+3)
        else:
            descript = descript + membname+'='
            descript = descript + join(split(str(member)[:50]))+'...\n'
    return descript

def pyobj_from_dom(dom_node):
    """Converts a DOM tree to a "native" Python object"""
    py_obj = PyObject()
    py_obj.PCDATA = ''
    for node in dom_node.get_childNodes():
        if node.name == '#text':
            py_obj.PCDATA = py_obj.PCDATA + node.value
        elif hasattr(py_obj, node.name):
            getattr(py_obj, node.name).append(pyobj_from_dom(node))
        else:
            setattr(py_obj, node.name, [pyobj_from_dom(node)])
    return py_obj

# Main test
dom_obj = FileReader("sample_rspec.xml").document
py_obj = pyobj_from_dom(dom_obj)
if __name__ == "__main__":
    print pyobj_printer(py_obj)