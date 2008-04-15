import org.python.core.*;

public class PathVFS extends java.lang.Object {
    static String[] jpy$mainProperties = new String[] {"python.modules.builtin", "exceptions:org.python.core.exceptions"};
    static String[] jpy$proxyProperties = new String[] {"python.modules.builtin", "exceptions:org.python.core.exceptions", "python.options.showJavaExceptions", "true"};
    static String[] jpy$packages = new String[] {"java.net", null, "java.lang", null, "org.python.core", null, "java.io", null, "java.util.zip", null};
    
    public static class _PyInner extends PyFunctionTable implements PyRunnable {
        private static PyObject s$0;
        private static PyObject s$1;
        private static PyObject s$2;
        private static PyObject s$3;
        private static PyObject i$4;
        private static PyObject s$5;
        private static PyObject s$6;
        private static PyObject s$7;
        private static PyObject s$8;
        private static PyObject s$9;
        private static PyObject s$10;
        private static PyObject s$11;
        private static PyFunctionTable funcTable;
        private static PyCode c$0___init__;
        private static PyCode c$1_open;
        private static PyCode c$2___repr__;
        private static PyCode c$3_JarVFS;
        private static PyCode c$4___init__;
        private static PyCode c$5_open;
        private static PyCode c$6___repr__;
        private static PyCode c$7_DirVFS;
        private static PyCode c$8_add_vfs;
        private static PyCode c$9___init__;
        private static PyCode c$10_open;
        private static PyCode c$11_PathVFS;
        private static PyCode c$12_main;
        private static void initConstants() {
            s$0 = Py.newString("<jar-vfs '%s'>");
            s$1 = Py.newString("");
            s$2 = Py.newString("/");
            s$3 = Py.newString("<dir-vfs '%s'>");
            i$4 = Py.newInteger(1);
            s$5 = Py.newString(".jar");
            s$6 = Py.newString(".zip");
            s$7 = Py.newString("python.packages.paths");
            s$8 = Py.newString("java.class.path");
            s$9 = Py.newString(",");
            s$10 = Py.newString("sun.boot.class.path");
            s$11 = Py.newString("/usr/share/jython/Tools/jythonc/PathVFS.py");
            funcTable = new _PyInner();
            c$0___init__ = Py.newCode(2, new String[] {"self", "fname"}, "/usr/share/jython/Tools/jythonc/PathVFS.py", "__init__", false, false, funcTable, 0, null, null, 0, 1);
            c$1_open = Py.newCode(2, new String[] {"self", "id", "ent"}, "/usr/share/jython/Tools/jythonc/PathVFS.py", "open", false, false, funcTable, 1, null, null, 0, 1);
            c$2___repr__ = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Tools/jythonc/PathVFS.py", "__repr__", false, false, funcTable, 2, null, null, 0, 1);
            c$3_JarVFS = Py.newCode(0, new String[] {}, "/usr/share/jython/Tools/jythonc/PathVFS.py", "JarVFS", false, false, funcTable, 3, null, null, 0, 0);
            c$4___init__ = Py.newCode(2, new String[] {"self", "dir"}, "/usr/share/jython/Tools/jythonc/PathVFS.py", "__init__", false, false, funcTable, 4, null, null, 0, 1);
            c$5_open = Py.newCode(2, new String[] {"self", "id", "f"}, "/usr/share/jython/Tools/jythonc/PathVFS.py", "open", false, false, funcTable, 5, null, null, 0, 1);
            c$6___repr__ = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Tools/jythonc/PathVFS.py", "__repr__", false, false, funcTable, 6, null, null, 0, 1);
            c$7_DirVFS = Py.newCode(0, new String[] {}, "/usr/share/jython/Tools/jythonc/PathVFS.py", "DirVFS", false, false, funcTable, 7, null, null, 0, 0);
            c$8_add_vfs = Py.newCode(2, new String[] {"self", "fname", "file", "canon"}, "/usr/share/jython/Tools/jythonc/PathVFS.py", "add_vfs", false, false, funcTable, 8, null, null, 0, 1);
            c$9___init__ = Py.newCode(2, new String[] {"self", "registry", "name", "p", "e", "paths", "path"}, "/usr/share/jython/Tools/jythonc/PathVFS.py", "__init__", false, false, funcTable, 9, null, null, 0, 1);
            c$10_open = Py.newCode(2, new String[] {"self", "id", "v", "stream"}, "/usr/share/jython/Tools/jythonc/PathVFS.py", "open", false, false, funcTable, 10, null, null, 0, 1);
            c$11_PathVFS = Py.newCode(0, new String[] {}, "/usr/share/jython/Tools/jythonc/PathVFS.py", "PathVFS", false, false, funcTable, 11, null, null, 0, 0);
            c$12_main = Py.newCode(0, new String[] {}, "/usr/share/jython/Tools/jythonc/PathVFS.py", "main", false, false, funcTable, 12, null, null, 0, 0);
        }
        
        
        public PyCode getMain() {
            if (c$12_main == null) _PyInner.initConstants();
            return c$12_main;
        }
        
        public PyObject call_function(int index, PyFrame frame) {
            switch (index){
                case 0:
                return _PyInner.__init__$1(frame);
                case 1:
                return _PyInner.open$2(frame);
                case 2:
                return _PyInner.__repr__$3(frame);
                case 3:
                return _PyInner.JarVFS$4(frame);
                case 4:
                return _PyInner.__init__$5(frame);
                case 5:
                return _PyInner.open$6(frame);
                case 6:
                return _PyInner.__repr__$7(frame);
                case 7:
                return _PyInner.DirVFS$8(frame);
                case 8:
                return _PyInner.add_vfs$9(frame);
                case 9:
                return _PyInner.__init__$10(frame);
                case 10:
                return _PyInner.open$11(frame);
                case 11:
                return _PyInner.PathVFS$12(frame);
                case 12:
                return _PyInner.main$13(frame);
                default:
                return null;
            }
        }
        
        private static PyObject __init__$1(PyFrame frame) {
            frame.getlocal(0).__setattr__("zipfile", frame.getglobal("zip").__getattr__("ZipFile").__call__(frame.getlocal(1)));
            return Py.None;
        }
        
        private static PyObject open$2(PyFrame frame) {
            frame.setlocal(2, frame.getlocal(0).__getattr__("zipfile").invoke("getEntry", frame.getlocal(1)));
            if (frame.getlocal(2).__nonzero__()) {
                return frame.getlocal(0).__getattr__("zipfile").invoke("getInputStream", frame.getlocal(2));
            }
            else {
                return frame.getglobal("None");
            }
        }
        
        private static PyObject __repr__$3(PyFrame frame) {
            return s$0._mod(frame.getlocal(0).__getattr__("zipfile").__getattr__("name"));
        }
        
        private static PyObject JarVFS$4(PyFrame frame) {
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {}, c$0___init__));
            frame.setlocal("open", new PyFunction(frame.f_globals, new PyObject[] {}, c$1_open));
            frame.setlocal("__repr__", new PyFunction(frame.f_globals, new PyObject[] {}, c$2___repr__));
            return frame.getf_locals();
        }
        
        private static PyObject __init__$5(PyFrame frame) {
            if (frame.getlocal(1)._eq(s$1).__nonzero__()) {
                frame.getlocal(0).__setattr__("pfx", frame.getglobal("None"));
            }
            else {
                frame.getlocal(0).__setattr__("pfx", frame.getlocal(1));
            }
            return Py.None;
        }
        
        private static PyObject open$6(PyFrame frame) {
            frame.setlocal(2, frame.getglobal("io").__getattr__("File").__call__(frame.getlocal(0).__getattr__("pfx"), frame.getlocal(1).invoke("replace", s$2, frame.getglobal("io").__getattr__("File").__getattr__("separator"))));
            if (frame.getlocal(2).__getattr__("file").__nonzero__()) {
                return frame.getglobal("io").__getattr__("BufferedInputStream").__call__(frame.getglobal("io").__getattr__("FileInputStream").__call__(frame.getlocal(2)));
            }
            return frame.getglobal("None");
        }
        
        private static PyObject __repr__$7(PyFrame frame) {
            return s$3._mod(frame.getlocal(0).__getattr__("pfx"));
        }
        
        private static PyObject DirVFS$8(PyFrame frame) {
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {}, c$4___init__));
            frame.setlocal("open", new PyFunction(frame.f_globals, new PyObject[] {}, c$5_open));
            frame.setlocal("__repr__", new PyFunction(frame.f_globals, new PyObject[] {}, c$6___repr__));
            return frame.getf_locals();
        }
        
        private static PyObject add_vfs$9(PyFrame frame) {
            // Temporary Variables
            PyException t$0$PyException;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            if (frame.getlocal(1)._eq(s$1).__nonzero__()) {
                if (frame.getlocal(0).__getattr__("once").invoke("has_key", s$1).__not__().__nonzero__()) {
                    frame.getlocal(0).__getattr__("once").__setitem__(s$1, i$4);
                    frame.getlocal(0).__getattr__("vfs").invoke("append", frame.getglobal("DirVFS").__call__(s$1));
                }
                return Py.None;
            }
            frame.setlocal(2, frame.getglobal("io").__getattr__("File").__call__(frame.getlocal(1)));
            frame.setlocal(3, frame.getlocal(2).__getattr__("canonicalPath"));
            if (frame.getlocal(0).__getattr__("once").invoke("has_key", frame.getlocal(3)).__not__().__nonzero__()) {
                frame.getlocal(0).__getattr__("once").__setitem__(frame.getlocal(3), i$4);
                try {
                    if (frame.getlocal(2).__getattr__("directory").__nonzero__()) {
                        frame.getlocal(0).__getattr__("vfs").invoke("append", frame.getglobal("DirVFS").__call__(frame.getlocal(1)));
                    }
                    else {
                        if (((t$0$PyObject = frame.getlocal(2).__getattr__("exists")).__nonzero__() ? ((t$1$PyObject = frame.getlocal(1).invoke("endswith", s$5)).__nonzero__() ? t$1$PyObject : frame.getlocal(1).invoke("endswith", s$6)) : t$0$PyObject).__nonzero__()) {
                            frame.getlocal(0).__getattr__("vfs").invoke("append", frame.getglobal("JarVFS").__call__(frame.getlocal(1)));
                        }
                    }
                }
                catch (Throwable x$0) {
                    t$0$PyException = Py.setException(x$0, frame);
                    // pass
                }
            }
            return Py.None;
        }
        
        private static PyObject __init__$10(PyFrame frame) {
            // Temporary Variables
            int t$0$int, t$1$int, t$2$int;
            PyObject t$0$PyObject, t$1$PyObject, t$2$PyObject, t$3$PyObject, t$4$PyObject, t$5$PyObject;
            
            // Code
            frame.getlocal(0).__setattr__("once", new PyDictionary(new PyObject[] {}));
            frame.getlocal(0).__setattr__("vfs", new PyList(new PyObject[] {}));
            frame.setlocal(5, frame.getlocal(1).invoke("getProperty", s$7, s$8));
            frame.setlocal(5, frame.getlocal(5).invoke("split", s$9));
            if (s$10._in(frame.getlocal(5)).__nonzero__()) {
                frame.getlocal(5).invoke("remove", s$10);
            }
            t$0$int = 0;
            t$1$PyObject = frame.getlocal(5);
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                frame.setlocal(3, t$0$PyObject);
                frame.setlocal(4, frame.getlocal(1).invoke("getProperty", frame.getlocal(3)));
                if (frame.getlocal(4)._ne(frame.getglobal("None")).__nonzero__()) {
                    frame.setlocal(6, frame.getlocal(4).invoke("split", frame.getglobal("io").__getattr__("File").__getattr__("pathSeparator")));
                    t$1$int = 0;
                    t$3$PyObject = frame.getlocal(6);
                    while ((t$2$PyObject = t$3$PyObject.__finditem__(t$1$int++)) != null) {
                        frame.setlocal(2, t$2$PyObject);
                        frame.getlocal(0).invoke("add_vfs", frame.getlocal(2));
                    }
                }
            }
            t$2$int = 0;
            t$5$PyObject = frame.getglobal("sys").__getattr__("path");
            while ((t$4$PyObject = t$5$PyObject.__finditem__(t$2$int++)) != null) {
                frame.setlocal(2, t$4$PyObject);
                frame.getlocal(0).invoke("add_vfs", frame.getlocal(2));
            }
            frame.getlocal(0).__delattr__("once");
            return Py.None;
        }
        
        private static PyObject open$11(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            t$0$int = 0;
            t$1$PyObject = frame.getlocal(0).__getattr__("vfs");
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                frame.setlocal(2, t$0$PyObject);
                frame.setlocal(3, frame.getlocal(2).invoke("open", frame.getlocal(1)));
                if (frame.getlocal(3).__nonzero__()) {
                    return frame.getlocal(3);
                }
            }
            return frame.getglobal("None");
        }
        
        private static PyObject PathVFS$12(PyFrame frame) {
            frame.setlocal("add_vfs", new PyFunction(frame.f_globals, new PyObject[] {}, c$8_add_vfs));
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {}, c$9___init__));
            frame.setlocal("open", new PyFunction(frame.f_globals, new PyObject[] {}, c$10_open));
            return frame.getf_locals();
        }
        
        private static PyObject main$13(PyFrame frame) {
            frame.setglobal("__file__", s$11);
            
            PyObject[] imp_accu;
            // Code
            frame.setlocal("sys", org.python.core.imp.importOne("sys", frame));
            imp_accu = org.python.core.imp.importFrom("java", new String[] {"io"}, frame);
            frame.setlocal("io", imp_accu[0]);
            imp_accu = null;
            imp_accu = org.python.core.imp.importFrom("java.util", new String[] {"zip"}, frame);
            frame.setlocal("zip", imp_accu[0]);
            imp_accu = null;
            frame.setlocal("JarVFS", Py.makeClass("JarVFS", new PyObject[] {}, c$3_JarVFS, null));
            frame.setlocal("DirVFS", Py.makeClass("DirVFS", new PyObject[] {}, c$7_DirVFS, null));
            frame.setlocal("PathVFS", Py.makeClass("PathVFS", new PyObject[] {}, c$11_PathVFS, null));
            return Py.None;
        }
        
    }
    public static void moduleDictInit(PyObject dict) {
        dict.__setitem__("__name__", new PyString("PathVFS"));
        Py.runCode(new _PyInner().getMain(), dict, dict);
    }
    
    public static void main(String[] args) throws java.lang.Exception {
        String[] newargs = new String[args.length+1];
        newargs[0] = "PathVFS";
        System.arraycopy(args, 0, newargs, 1, args.length);
        Py.runMain(PathVFS._PyInner.class, newargs, PathVFS.jpy$packages, PathVFS.jpy$mainProperties, "", new String[] {"string", "random", "util", "traceback", "sre_compile", "atexit", "sre", "sre_constants", "StringIO", "javaos", "socket", "yapm", "calendar", "repr", "copy_reg", "SocketServer", "server", "re", "linecache", "javapath", "UserDict", "copy", "threading", "stat", "PathVFS", "sre_parse"});
    }
    
}
