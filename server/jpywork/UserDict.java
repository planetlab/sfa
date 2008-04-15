import org.python.core.*;

public class UserDict extends java.lang.Object {
    static String[] jpy$mainProperties = new String[] {"python.modules.builtin", "exceptions:org.python.core.exceptions"};
    static String[] jpy$proxyProperties = new String[] {"python.modules.builtin", "exceptions:org.python.core.exceptions", "python.options.showJavaExceptions", "true"};
    static String[] jpy$packages = new String[] {"java.net", null, "java.lang", null, "org.python.core", null, "java.io", null, "java.util.zip", null};
    
    public static class _PyInner extends PyFunctionTable implements PyRunnable {
        private static PyObject s$0;
        private static PyObject s$1;
        private static PyFunctionTable funcTable;
        private static PyCode c$0___init__;
        private static PyCode c$1___repr__;
        private static PyCode c$2___cmp__;
        private static PyCode c$3___len__;
        private static PyCode c$4___getitem__;
        private static PyCode c$5___setitem__;
        private static PyCode c$6___delitem__;
        private static PyCode c$7_clear;
        private static PyCode c$8_copy;
        private static PyCode c$9_keys;
        private static PyCode c$10_items;
        private static PyCode c$11_values;
        private static PyCode c$12_has_key;
        private static PyCode c$13_update;
        private static PyCode c$14_get;
        private static PyCode c$15_setdefault;
        private static PyCode c$16_popitem;
        private static PyCode c$17_UserDict;
        private static PyCode c$18_main;
        private static void initConstants() {
            s$0 = Py.newString("A more or less complete user-defined wrapper around dictionary objects.");
            s$1 = Py.newString("/usr/share/jython/Lib-cpython/UserDict.py");
            funcTable = new _PyInner();
            c$0___init__ = Py.newCode(2, new String[] {"self", "dict"}, "/usr/share/jython/Lib-cpython/UserDict.py", "__init__", false, false, funcTable, 0, null, null, 0, 1);
            c$1___repr__ = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/UserDict.py", "__repr__", false, false, funcTable, 1, null, null, 0, 1);
            c$2___cmp__ = Py.newCode(2, new String[] {"self", "dict"}, "/usr/share/jython/Lib-cpython/UserDict.py", "__cmp__", false, false, funcTable, 2, null, null, 0, 1);
            c$3___len__ = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/UserDict.py", "__len__", false, false, funcTable, 3, null, null, 0, 1);
            c$4___getitem__ = Py.newCode(2, new String[] {"self", "key"}, "/usr/share/jython/Lib-cpython/UserDict.py", "__getitem__", false, false, funcTable, 4, null, null, 0, 1);
            c$5___setitem__ = Py.newCode(3, new String[] {"self", "key", "item"}, "/usr/share/jython/Lib-cpython/UserDict.py", "__setitem__", false, false, funcTable, 5, null, null, 0, 1);
            c$6___delitem__ = Py.newCode(2, new String[] {"self", "key"}, "/usr/share/jython/Lib-cpython/UserDict.py", "__delitem__", false, false, funcTable, 6, null, null, 0, 1);
            c$7_clear = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/UserDict.py", "clear", false, false, funcTable, 7, null, null, 0, 1);
            c$8_copy = Py.newCode(1, new String[] {"self", "copy"}, "/usr/share/jython/Lib-cpython/UserDict.py", "copy", false, false, funcTable, 8, null, null, 0, 1);
            c$9_keys = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/UserDict.py", "keys", false, false, funcTable, 9, null, null, 0, 1);
            c$10_items = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/UserDict.py", "items", false, false, funcTable, 10, null, null, 0, 1);
            c$11_values = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/UserDict.py", "values", false, false, funcTable, 11, null, null, 0, 1);
            c$12_has_key = Py.newCode(2, new String[] {"self", "key"}, "/usr/share/jython/Lib-cpython/UserDict.py", "has_key", false, false, funcTable, 12, null, null, 0, 1);
            c$13_update = Py.newCode(2, new String[] {"self", "dict", "v", "k"}, "/usr/share/jython/Lib-cpython/UserDict.py", "update", false, false, funcTable, 13, null, null, 0, 1);
            c$14_get = Py.newCode(3, new String[] {"self", "key", "failobj"}, "/usr/share/jython/Lib-cpython/UserDict.py", "get", false, false, funcTable, 14, null, null, 0, 1);
            c$15_setdefault = Py.newCode(3, new String[] {"self", "key", "failobj"}, "/usr/share/jython/Lib-cpython/UserDict.py", "setdefault", false, false, funcTable, 15, null, null, 0, 1);
            c$16_popitem = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/UserDict.py", "popitem", false, false, funcTable, 16, null, null, 0, 1);
            c$17_UserDict = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/UserDict.py", "UserDict", false, false, funcTable, 17, null, null, 0, 0);
            c$18_main = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/UserDict.py", "main", false, false, funcTable, 18, null, null, 0, 0);
        }
        
        
        public PyCode getMain() {
            if (c$18_main == null) _PyInner.initConstants();
            return c$18_main;
        }
        
        public PyObject call_function(int index, PyFrame frame) {
            switch (index){
                case 0:
                return _PyInner.__init__$1(frame);
                case 1:
                return _PyInner.__repr__$2(frame);
                case 2:
                return _PyInner.__cmp__$3(frame);
                case 3:
                return _PyInner.__len__$4(frame);
                case 4:
                return _PyInner.__getitem__$5(frame);
                case 5:
                return _PyInner.__setitem__$6(frame);
                case 6:
                return _PyInner.__delitem__$7(frame);
                case 7:
                return _PyInner.clear$8(frame);
                case 8:
                return _PyInner.copy$9(frame);
                case 9:
                return _PyInner.keys$10(frame);
                case 10:
                return _PyInner.items$11(frame);
                case 11:
                return _PyInner.values$12(frame);
                case 12:
                return _PyInner.has_key$13(frame);
                case 13:
                return _PyInner.update$14(frame);
                case 14:
                return _PyInner.get$15(frame);
                case 15:
                return _PyInner.setdefault$16(frame);
                case 16:
                return _PyInner.popitem$17(frame);
                case 17:
                return _PyInner.UserDict$18(frame);
                case 18:
                return _PyInner.main$19(frame);
                default:
                return null;
            }
        }
        
        private static PyObject __init__$1(PyFrame frame) {
            frame.getlocal(0).__setattr__("data", new PyDictionary(new PyObject[] {}));
            if (frame.getlocal(1)._isnot(frame.getglobal("None")).__nonzero__()) {
                frame.getlocal(0).invoke("update", frame.getlocal(1));
            }
            return Py.None;
        }
        
        private static PyObject __repr__$2(PyFrame frame) {
            return frame.getglobal("repr").__call__(frame.getlocal(0).__getattr__("data"));
        }
        
        private static PyObject __cmp__$3(PyFrame frame) {
            if (frame.getglobal("isinstance").__call__(frame.getlocal(1), frame.getglobal("UserDict")).__nonzero__()) {
                return frame.getglobal("cmp").__call__(frame.getlocal(0).__getattr__("data"), frame.getlocal(1).__getattr__("data"));
            }
            else {
                return frame.getglobal("cmp").__call__(frame.getlocal(0).__getattr__("data"), frame.getlocal(1));
            }
        }
        
        private static PyObject __len__$4(PyFrame frame) {
            return frame.getglobal("len").__call__(frame.getlocal(0).__getattr__("data"));
        }
        
        private static PyObject __getitem__$5(PyFrame frame) {
            return frame.getlocal(0).__getattr__("data").__getitem__(frame.getlocal(1));
        }
        
        private static PyObject __setitem__$6(PyFrame frame) {
            frame.getlocal(0).__getattr__("data").__setitem__(frame.getlocal(1), frame.getlocal(2));
            return Py.None;
        }
        
        private static PyObject __delitem__$7(PyFrame frame) {
            frame.getlocal(0).__getattr__("data").__delitem__(frame.getlocal(1));
            return Py.None;
        }
        
        private static PyObject clear$8(PyFrame frame) {
            frame.getlocal(0).__getattr__("data").invoke("clear");
            return Py.None;
        }
        
        private static PyObject copy$9(PyFrame frame) {
            if (frame.getlocal(0).__getattr__("__class__")._is(frame.getglobal("UserDict")).__nonzero__()) {
                return frame.getglobal("UserDict").__call__(frame.getlocal(0).__getattr__("data"));
            }
            frame.setlocal(1, org.python.core.imp.importOne("copy", frame));
            return frame.getlocal(1).__getattr__("copy").__call__(frame.getlocal(0));
        }
        
        private static PyObject keys$10(PyFrame frame) {
            return frame.getlocal(0).__getattr__("data").invoke("keys");
        }
        
        private static PyObject items$11(PyFrame frame) {
            return frame.getlocal(0).__getattr__("data").invoke("items");
        }
        
        private static PyObject values$12(PyFrame frame) {
            return frame.getlocal(0).__getattr__("data").invoke("values");
        }
        
        private static PyObject has_key$13(PyFrame frame) {
            return frame.getlocal(0).__getattr__("data").invoke("has_key", frame.getlocal(1));
        }
        
        private static PyObject update$14(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyObject[] t$0$PyObject__;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            if (frame.getglobal("isinstance").__call__(frame.getlocal(1), frame.getglobal("UserDict")).__nonzero__()) {
                frame.getlocal(0).__getattr__("data").invoke("update", frame.getlocal(1).__getattr__("data"));
            }
            else if (frame.getglobal("isinstance").__call__(frame.getlocal(1), frame.getglobal("type").__call__(frame.getlocal(0).__getattr__("data"))).__nonzero__()) {
                frame.getlocal(0).__getattr__("data").invoke("update", frame.getlocal(1));
            }
            else {
                t$0$int = 0;
                t$1$PyObject = frame.getlocal(1).invoke("items");
                while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                    t$0$PyObject__ = org.python.core.Py.unpackSequence(t$0$PyObject, 2);
                    frame.setlocal(3, t$0$PyObject__[0]);
                    frame.setlocal(2, t$0$PyObject__[1]);
                    frame.getlocal(0).__getattr__("data").__setitem__(frame.getlocal(3), frame.getlocal(2));
                }
            }
            return Py.None;
        }
        
        private static PyObject get$15(PyFrame frame) {
            return frame.getlocal(0).__getattr__("data").invoke("get", frame.getlocal(1), frame.getlocal(2));
        }
        
        private static PyObject setdefault$16(PyFrame frame) {
            if (frame.getlocal(0).__getattr__("data").invoke("has_key", frame.getlocal(1)).__not__().__nonzero__()) {
                frame.getlocal(0).__getattr__("data").__setitem__(frame.getlocal(1), frame.getlocal(2));
            }
            return frame.getlocal(0).__getattr__("data").__getitem__(frame.getlocal(1));
        }
        
        private static PyObject popitem$17(PyFrame frame) {
            return frame.getlocal(0).__getattr__("data").invoke("popitem");
        }
        
        private static PyObject UserDict$18(PyFrame frame) {
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$0___init__));
            frame.setlocal("__repr__", new PyFunction(frame.f_globals, new PyObject[] {}, c$1___repr__));
            frame.setlocal("__cmp__", new PyFunction(frame.f_globals, new PyObject[] {}, c$2___cmp__));
            frame.setlocal("__len__", new PyFunction(frame.f_globals, new PyObject[] {}, c$3___len__));
            frame.setlocal("__getitem__", new PyFunction(frame.f_globals, new PyObject[] {}, c$4___getitem__));
            frame.setlocal("__setitem__", new PyFunction(frame.f_globals, new PyObject[] {}, c$5___setitem__));
            frame.setlocal("__delitem__", new PyFunction(frame.f_globals, new PyObject[] {}, c$6___delitem__));
            frame.setlocal("clear", new PyFunction(frame.f_globals, new PyObject[] {}, c$7_clear));
            frame.setlocal("copy", new PyFunction(frame.f_globals, new PyObject[] {}, c$8_copy));
            frame.setlocal("keys", new PyFunction(frame.f_globals, new PyObject[] {}, c$9_keys));
            frame.setlocal("items", new PyFunction(frame.f_globals, new PyObject[] {}, c$10_items));
            frame.setlocal("values", new PyFunction(frame.f_globals, new PyObject[] {}, c$11_values));
            frame.setlocal("has_key", new PyFunction(frame.f_globals, new PyObject[] {}, c$12_has_key));
            frame.setlocal("update", new PyFunction(frame.f_globals, new PyObject[] {}, c$13_update));
            frame.setlocal("get", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$14_get));
            frame.setlocal("setdefault", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$15_setdefault));
            frame.setlocal("popitem", new PyFunction(frame.f_globals, new PyObject[] {}, c$16_popitem));
            return frame.getf_locals();
        }
        
        private static PyObject main$19(PyFrame frame) {
            frame.setglobal("__file__", s$1);
            
            /* A more or less complete user-defined wrapper around dictionary objects. */
            frame.setlocal("UserDict", Py.makeClass("UserDict", new PyObject[] {}, c$17_UserDict, null));
            return Py.None;
        }
        
    }
    public static void moduleDictInit(PyObject dict) {
        dict.__setitem__("__name__", new PyString("UserDict"));
        Py.runCode(new _PyInner().getMain(), dict, dict);
    }
    
    public static void main(String[] args) throws java.lang.Exception {
        String[] newargs = new String[args.length+1];
        newargs[0] = "UserDict";
        System.arraycopy(args, 0, newargs, 1, args.length);
        Py.runMain(UserDict._PyInner.class, newargs, UserDict.jpy$packages, UserDict.jpy$mainProperties, "", new String[] {"string", "random", "util", "traceback", "sre_compile", "atexit", "sre", "sre_constants", "StringIO", "javaos", "socket", "yapm", "calendar", "repr", "copy_reg", "SocketServer", "server", "re", "linecache", "javapath", "UserDict", "copy", "threading", "stat", "PathVFS", "sre_parse"});
    }
    
}
