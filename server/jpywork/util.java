import org.python.core.*;

public class util extends java.lang.Object {
    static String[] jpy$mainProperties = new String[] {"python.modules.builtin", "exceptions:org.python.core.exceptions"};
    static String[] jpy$proxyProperties = new String[] {"python.modules.builtin", "exceptions:org.python.core.exceptions", "python.options.showJavaExceptions", "true"};
    static String[] jpy$packages = new String[] {"java.net", null, "java.lang", null, "org.python.core", null, "java.io", null, "java.util.zip", null};
    
    public static class _PyInner extends PyFunctionTable implements PyRunnable {
        private static PyObject s$0;
        private static PyObject i$1;
        private static PyObject i$2;
        private static PyObject s$3;
        private static PyObject s$4;
        private static PyObject s$5;
        private static PyObject s$6;
        private static PyFunctionTable funcTable;
        private static PyCode c$0_lookup;
        private static PyCode c$1_getzip;
        private static PyCode c$2_closezips;
        private static PyCode c$3_findClass;
        private static PyCode c$4_reportPublicPlainClasses;
        private static PyCode c$5_openResource;
        private static PyCode c$6_listAllClasses;
        private static PyCode c$7_main;
        private static void initConstants() {
            s$0 = Py.newString(".");
            i$1 = Py.newInteger(0);
            i$2 = Py.newInteger(1);
            s$3 = Py.newString("java class");
            s$4 = Py.newString("__name__");
            s$5 = Py.newString(",");
            s$6 = Py.newString("/usr/share/jython/Tools/jythonc/util.py");
            funcTable = new _PyInner();
            c$0_lookup = Py.newCode(1, new String[] {"name", "top", "names"}, "/usr/share/jython/Tools/jythonc/util.py", "lookup", false, false, funcTable, 0, null, null, 0, 1);
            c$1_getzip = Py.newCode(1, new String[] {"filename", "zipfile"}, "/usr/share/jython/Tools/jythonc/util.py", "getzip", false, false, funcTable, 1, null, null, 0, 1);
            c$2_closezips = Py.newCode(0, new String[] {"zf"}, "/usr/share/jython/Tools/jythonc/util.py", "closezips", false, false, funcTable, 2, null, null, 0, 1);
            c$3_findClass = Py.newCode(1, new String[] {"c"}, "/usr/share/jython/Tools/jythonc/util.py", "findClass", false, false, funcTable, 3, null, null, 0, 1);
            c$4_reportPublicPlainClasses = Py.newCode(1, new String[] {"jpkg", "classes"}, "/usr/share/jython/Tools/jythonc/util.py", "reportPublicPlainClasses", false, false, funcTable, 4, null, null, 0, 1);
            c$5_openResource = Py.newCode(1, new String[] {"res"}, "/usr/share/jython/Tools/jythonc/util.py", "openResource", false, false, funcTable, 5, null, null, 0, 1);
            c$6_listAllClasses = Py.newCode(1, new String[] {"jpkg", "classes", "classes2", "pkg2"}, "/usr/share/jython/Tools/jythonc/util.py", "listAllClasses", false, false, funcTable, 6, null, null, 0, 1);
            c$7_main = Py.newCode(0, new String[] {}, "/usr/share/jython/Tools/jythonc/util.py", "main", false, false, funcTable, 7, null, null, 0, 0);
        }
        
        
        public PyCode getMain() {
            if (c$7_main == null) _PyInner.initConstants();
            return c$7_main;
        }
        
        public PyObject call_function(int index, PyFrame frame) {
            switch (index){
                case 0:
                return _PyInner.lookup$1(frame);
                case 1:
                return _PyInner.getzip$2(frame);
                case 2:
                return _PyInner.closezips$3(frame);
                case 3:
                return _PyInner.findClass$4(frame);
                case 4:
                return _PyInner.reportPublicPlainClasses$5(frame);
                case 5:
                return _PyInner.openResource$6(frame);
                case 6:
                return _PyInner.listAllClasses$7(frame);
                case 7:
                return _PyInner.main$8(frame);
                default:
                return null;
            }
        }
        
        private static PyObject lookup$1(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            frame.setlocal(2, frame.getlocal(0).invoke("split", s$0));
            frame.setlocal(1, frame.getglobal("__import__").__call__(frame.getlocal(2).__getitem__(i$1)));
            t$0$int = 0;
            t$1$PyObject = frame.getlocal(2).__getslice__(i$2, null, null);
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                frame.setlocal(0, t$0$PyObject);
                frame.setlocal(1, frame.getglobal("getattr").__call__(frame.getlocal(1), frame.getlocal(0)));
            }
            return frame.getlocal(1);
        }
        
        private static PyObject getzip$2(PyFrame frame) {
            if (frame.getglobal("zipfiles").invoke("has_key", frame.getlocal(0)).__nonzero__()) {
                return frame.getglobal("zipfiles").__getitem__(frame.getlocal(0));
            }
            frame.setlocal(1, frame.getglobal("ZipFile").__call__(frame.getlocal(0)));
            frame.getglobal("zipfiles").__setitem__(frame.getlocal(0), frame.getlocal(1));
            return frame.getlocal(1);
        }
        
        private static PyObject closezips$3(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            t$0$int = 0;
            t$1$PyObject = frame.getglobal("zipfiles").invoke("values");
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                frame.setlocal(0, t$0$PyObject);
                frame.getlocal(0).invoke("close");
            }
            frame.getglobal("zipfiles").invoke("clear");
            return Py.None;
        }
        
        private static PyObject findClass$4(PyFrame frame) {
            return frame.getglobal("Py").__getattr__("findClassEx").__call__(frame.getlocal(0), s$3);
        }
        
        private static PyObject reportPublicPlainClasses$5(PyFrame frame) {
            frame.setlocal(1, frame.getglobal("sys").__getattr__("packageManager").__getattr__("doDir").__call__(frame.getlocal(0), i$1, i$2));
            frame.getlocal(1).invoke("remove", s$4);
            return frame.getglobal("string").__getattr__("join").__call__(frame.getlocal(1), s$5);
        }
        
        private static PyObject openResource$6(PyFrame frame) {
            // global _path_vfs
            if (frame.getglobal("_path_vfs").__not__().__nonzero__()) {
                frame.setglobal("_path_vfs", frame.getglobal("PathVFS").__call__(frame.getglobal("sys").__getattr__("registry")));
            }
            return frame.getglobal("_path_vfs").invoke("open", frame.getlocal(0));
        }
        
        private static PyObject listAllClasses$7(PyFrame frame) {
            // global _ypm
            frame.setlocal(1, frame.getglobal("sys").__getattr__("packageManager").__getattr__("doDir").__call__(frame.getlocal(0), i$1, i$2));
            frame.getlocal(1).invoke("remove", s$4);
            if (frame.getglobal("_ypm")._is(frame.getglobal("None")).__nonzero__()) {
                frame.setglobal("_ypm", frame.getglobal("YaPM").__call__(frame.getglobal("sys").__getattr__("registry")));
            }
            frame.setlocal(3, frame.getglobal("_ypm").invoke("lookupName", frame.getlocal(0).__getattr__("__name__")));
            frame.setlocal(2, frame.getglobal("_ypm").invoke("doDir", new PyObject[] {frame.getlocal(3), i$1, i$2}));
            frame.getlocal(2).invoke("remove", s$4);
            frame.getlocal(1).invoke("extend", frame.getlocal(2));
            return frame.getlocal(1);
        }
        
        private static PyObject main$8(PyFrame frame) {
            frame.setglobal("__file__", s$6);
            
            PyObject[] imp_accu;
            // Code
            frame.setlocal("lookup", new PyFunction(frame.f_globals, new PyObject[] {}, c$0_lookup));
            imp_accu = org.python.core.imp.importFrom("java.util.zip", new String[] {"ZipFile"}, frame);
            frame.setlocal("ZipFile", imp_accu[0]);
            imp_accu = null;
            frame.setlocal("zipfiles", new PyDictionary(new PyObject[] {}));
            frame.setlocal("getzip", new PyFunction(frame.f_globals, new PyObject[] {}, c$1_getzip));
            frame.setlocal("closezips", new PyFunction(frame.f_globals, new PyObject[] {}, c$2_closezips));
            frame.setlocal("sys", org.python.core.imp.importOne("sys", frame));
            frame.setlocal("string", org.python.core.imp.importOne("string", frame));
            imp_accu = org.python.core.imp.importFrom("org.python.core", new String[] {"Py"}, frame);
            frame.setlocal("Py", imp_accu[0]);
            imp_accu = null;
            imp_accu = org.python.core.imp.importFrom("yapm", new String[] {"YaPM"}, frame);
            frame.setlocal("YaPM", imp_accu[0]);
            imp_accu = null;
            imp_accu = org.python.core.imp.importFrom("PathVFS", new String[] {"PathVFS"}, frame);
            frame.setlocal("PathVFS", imp_accu[0]);
            imp_accu = null;
            frame.setlocal("findClass", new PyFunction(frame.f_globals, new PyObject[] {}, c$3_findClass));
            frame.setlocal("reportPublicPlainClasses", new PyFunction(frame.f_globals, new PyObject[] {}, c$4_reportPublicPlainClasses));
            frame.setlocal("_path_vfs", frame.getname("None"));
            frame.setlocal("openResource", new PyFunction(frame.f_globals, new PyObject[] {}, c$5_openResource));
            frame.setlocal("_ypm", frame.getname("None"));
            frame.setlocal("listAllClasses", new PyFunction(frame.f_globals, new PyObject[] {}, c$6_listAllClasses));
            return Py.None;
        }
        
    }
    public static void moduleDictInit(PyObject dict) {
        dict.__setitem__("__name__", new PyString("util"));
        Py.runCode(new _PyInner().getMain(), dict, dict);
    }
    
    public static void main(String[] args) throws java.lang.Exception {
        String[] newargs = new String[args.length+1];
        newargs[0] = "util";
        System.arraycopy(args, 0, newargs, 1, args.length);
        Py.runMain(util._PyInner.class, newargs, util.jpy$packages, util.jpy$mainProperties, "", new String[] {"string", "random", "util", "traceback", "sre_compile", "atexit", "sre", "sre_constants", "StringIO", "javaos", "socket", "yapm", "calendar", "repr", "copy_reg", "SocketServer", "server", "re", "linecache", "javapath", "UserDict", "copy", "threading", "stat", "PathVFS", "sre_parse"});
    }
    
}
