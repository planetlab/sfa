import org.python.core.*;

public class yapm extends java.lang.Object {
    static String[] jpy$mainProperties = new String[] {"python.modules.builtin", "exceptions:org.python.core.exceptions"};
    static String[] jpy$proxyProperties = new String[] {"python.modules.builtin", "exceptions:org.python.core.exceptions", "python.options.showJavaExceptions", "true"};
    static String[] jpy$packages = new String[] {"java.net", null, "java.lang", null, "org.python.core", null, "java.io", null, "java.util.zip", null};
    
    public static class _PyInner extends PyFunctionTable implements PyRunnable {
        private static PyObject s$0;
        private static PyObject s$1;
        private static PyObject s$2;
        private static PyObject s$3;
        private static PyObject s$4;
        private static PyObject i$5;
        private static PyObject s$6;
        private static PyObject i$7;
        private static PyObject s$8;
        private static PyFunctionTable funcTable;
        private static PyCode c$0___init__;
        private static PyCode c$1_findClass;
        private static PyCode c$2_findAllPackages;
        private static PyCode c$3_filterByName;
        private static PyCode c$4_filterByAccess;
        private static PyCode c$5_doDir;
        private static PyCode c$6_packageExists;
        private static PyCode c$7_YaPM;
        private static PyCode c$8_main;
        private static void initConstants() {
            s$0 = Py.newString("python.packages.paths");
            s$1 = Py.newString("java.class.path");
            s$2 = Py.newString(",");
            s$3 = Py.newString("sun.boot.class.path");
            s$4 = Py.newString("python.packages.fakepath");
            i$5 = Py.newInteger(0);
            s$6 = Py.newString("$");
            i$7 = Py.newInteger(1);
            s$8 = Py.newString("/usr/share/jython/Tools/jythonc/yapm.py");
            funcTable = new _PyInner();
            c$0___init__ = Py.newCode(2, new String[] {"self", "registry"}, "/usr/share/jython/Tools/jythonc/yapm.py", "__init__", false, false, funcTable, 0, null, null, 0, 1);
            c$1_findClass = Py.newCode(3, new String[] {"self", "pkg", "name"}, "/usr/share/jython/Tools/jythonc/yapm.py", "findClass", false, false, funcTable, 1, null, null, 0, 1);
            c$2_findAllPackages = Py.newCode(2, new String[] {"self", "registry", "e", "p", "fakepath", "paths"}, "/usr/share/jython/Tools/jythonc/yapm.py", "findAllPackages", false, false, funcTable, 2, null, null, 0, 1);
            c$3_filterByName = Py.newCode(3, new String[] {"self", "name", "pkg"}, "/usr/share/jython/Tools/jythonc/yapm.py", "filterByName", false, false, funcTable, 3, null, null, 0, 1);
            c$4_filterByAccess = Py.newCode(3, new String[] {"self", "name", "acc"}, "/usr/share/jython/Tools/jythonc/yapm.py", "filterByAccess", false, false, funcTable, 4, null, null, 0, 1);
            c$5_doDir = Py.newCode(4, new String[] {"self", "jpkg", "instantiate", "exclpkgs", "basic", "ret"}, "/usr/share/jython/Tools/jythonc/yapm.py", "doDir", false, false, funcTable, 5, null, null, 0, 1);
            c$6_packageExists = Py.newCode(3, new String[] {"self", "pkg", "name"}, "/usr/share/jython/Tools/jythonc/yapm.py", "packageExists", false, false, funcTable, 6, null, null, 0, 1);
            c$7_YaPM = Py.newCode(0, new String[] {}, "/usr/share/jython/Tools/jythonc/yapm.py", "YaPM", false, false, funcTable, 7, null, null, 0, 0);
            c$8_main = Py.newCode(0, new String[] {}, "/usr/share/jython/Tools/jythonc/yapm.py", "main", false, false, funcTable, 8, null, null, 0, 0);
        }
        
        
        public PyCode getMain() {
            if (c$8_main == null) _PyInner.initConstants();
            return c$8_main;
        }
        
        public PyObject call_function(int index, PyFrame frame) {
            switch (index){
                case 0:
                return _PyInner.__init__$1(frame);
                case 1:
                return _PyInner.findClass$2(frame);
                case 2:
                return _PyInner.findAllPackages$3(frame);
                case 3:
                return _PyInner.filterByName$4(frame);
                case 4:
                return _PyInner.filterByAccess$5(frame);
                case 5:
                return _PyInner.doDir$6(frame);
                case 6:
                return _PyInner.packageExists$7(frame);
                case 7:
                return _PyInner.YaPM$8(frame);
                case 8:
                return _PyInner.main$9(frame);
                default:
                return null;
            }
        }
        
        private static PyObject __init__$1(PyFrame frame) {
            frame.getlocal(0).invoke("findAllPackages", frame.getlocal(1));
            return Py.None;
        }
        
        private static PyObject findClass$2(PyFrame frame) {
            return frame.getglobal("None");
        }
        
        private static PyObject findAllPackages$3(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            frame.setlocal(5, frame.getlocal(1).invoke("getProperty", s$0, s$1));
            frame.setlocal(5, frame.getlocal(5).invoke("split", s$2));
            if (s$3._in(frame.getlocal(5)).__nonzero__()) {
                frame.getlocal(5).invoke("remove", s$3);
            }
            frame.setlocal(4, frame.getlocal(1).invoke("getProperty", s$4, frame.getglobal("None")));
            t$0$int = 0;
            t$1$PyObject = frame.getlocal(5);
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                frame.setlocal(3, t$0$PyObject);
                frame.setlocal(2, frame.getlocal(1).invoke("getProperty", frame.getlocal(3)));
                if (frame.getlocal(2)._ne(frame.getglobal("None")).__nonzero__()) {
                    frame.getlocal(0).invoke("addClassPath", frame.getlocal(2));
                }
            }
            if (frame.getlocal(4)._ne(frame.getglobal("None")).__nonzero__()) {
                frame.getlocal(0).invoke("addClassPath", frame.getlocal(4));
            }
            return Py.None;
        }
        
        private static PyObject filterByName$4(PyFrame frame) {
            return i$5;
        }
        
        private static PyObject filterByAccess$5(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject;
            
            // Code
            return ((t$0$PyObject = frame.getlocal(1).invoke("find", s$6)._ne(i$7.__neg__())).__nonzero__() ? t$0$PyObject : frame.getlocal(2)._and(i$7)._eq(i$5)).__not__();
        }
        
        private static PyObject doDir$6(PyFrame frame) {
            frame.setlocal(4, frame.getlocal(0).invoke("basicDoDir", new PyObject[] {frame.getlocal(1), i$5, frame.getlocal(3)}));
            frame.setlocal(5, new PyList(new PyObject[] {}));
            frame.getlocal(0).invoke("super__doDir", new PyObject[] {frame.getlocal(0).__getattr__("searchPath"), frame.getlocal(5), frame.getlocal(1), i$5, frame.getlocal(3)});
            frame.getlocal(0).invoke("super__doDir", new PyObject[] {frame.getglobal("sys").__getattr__("path"), frame.getlocal(5), frame.getlocal(1), i$5, frame.getlocal(3)});
            return frame.getlocal(0).invoke("merge", frame.getlocal(4), frame.getlocal(5));
        }
        
        private static PyObject packageExists$7(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject;
            
            // Code
            return (t$0$PyObject = frame.getlocal(0).invoke("super__packageExists", new PyObject[] {frame.getlocal(0).__getattr__("searchPath"), frame.getlocal(1), frame.getlocal(2)})).__nonzero__() ? t$0$PyObject : frame.getlocal(0).invoke("super__packageExists", new PyObject[] {frame.getglobal("sys").__getattr__("path"), frame.getlocal(1), frame.getlocal(2)});
        }
        
        private static PyObject YaPM$8(PyFrame frame) {
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {}, c$0___init__));
            frame.setlocal("findClass", new PyFunction(frame.f_globals, new PyObject[] {}, c$1_findClass));
            frame.setlocal("findAllPackages", new PyFunction(frame.f_globals, new PyObject[] {}, c$2_findAllPackages));
            frame.setlocal("filterByName", new PyFunction(frame.f_globals, new PyObject[] {}, c$3_filterByName));
            frame.setlocal("filterByAccess", new PyFunction(frame.f_globals, new PyObject[] {}, c$4_filterByAccess));
            frame.setlocal("doDir", new PyFunction(frame.f_globals, new PyObject[] {}, c$5_doDir));
            frame.setlocal("packageExists", new PyFunction(frame.f_globals, new PyObject[] {}, c$6_packageExists));
            return frame.getf_locals();
        }
        
        private static PyObject main$9(PyFrame frame) {
            frame.setglobal("__file__", s$8);
            
            PyObject[] imp_accu;
            // Code
            frame.setlocal("sys", org.python.core.imp.importOne("sys", frame));
            frame.setlocal("os", org.python.core.imp.importOne("os", frame));
            imp_accu = org.python.core.imp.importFrom("string", new String[] {"strip"}, frame);
            frame.setlocal("strip", imp_accu[0]);
            imp_accu = null;
            imp_accu = org.python.core.imp.importFrom("java", new String[] {"io"}, frame);
            frame.setlocal("io", imp_accu[0]);
            imp_accu = null;
            imp_accu = org.python.core.imp.importFrom("org.python.core", new String[] {"PathPackageManager"}, frame);
            frame.setlocal("PathPackageManager", imp_accu[0]);
            imp_accu = null;
            frame.setlocal("YaPM", Py.makeClass("YaPM", new PyObject[] {frame.getname("PathPackageManager")}, c$7_YaPM, null, YaPM.class));
            return Py.None;
        }
        
    }
    public static class YaPM extends org.python.core.PathPackageManager implements org.python.core.PyProxy, org.python.core.ClassDictInit {
        public void addJar(java.lang.String arg0, boolean arg1) {
            PyObject inst = Py.jgetattr(this, "addJar");
            inst._jcall(new Object[] {arg0, Py.newBoolean(arg1)});
        }
        
        public void addJarDir(java.lang.String arg0, boolean arg1) {
            PyObject inst = Py.jgetattr(this, "addJarDir");
            inst._jcall(new Object[] {arg0, Py.newBoolean(arg1)});
        }
        
        public org.python.core.PyList basicDoDir(org.python.core.PyJavaPackage arg0, boolean arg1, boolean arg2) {
            return super.basicDoDir(arg0, arg1, arg2);
        }
        
        public java.lang.Object clone() throws java.lang.CloneNotSupportedException {
            return super.clone();
        }
        
        public void comment(java.lang.String arg0) {
            super.comment(arg0);
        }
        
        public void debug(java.lang.String arg0) {
            super.debug(arg0);
        }
        
        public void deleteCacheFile(java.lang.String arg0) {
            super.deleteCacheFile(arg0);
        }
        
        public void super__doDir(org.python.core.PyList arg0, org.python.core.PyList arg1, org.python.core.PyJavaPackage arg2, boolean arg3, boolean arg4) {
            super.doDir(arg0, arg1, arg2, arg3, arg4);
        }
        
        public void doDir(org.python.core.PyList arg0, org.python.core.PyList arg1, org.python.core.PyJavaPackage arg2, boolean arg3, boolean arg4) {
            PyObject inst = Py.jfindattr(this, "doDir");
            if (inst != null) inst._jcall(new Object[] {arg0, arg1, arg2, Py.newBoolean(arg3), Py.newBoolean(arg4)});
            else super.doDir(arg0, arg1, arg2, arg3, arg4);
        }
        
        public org.python.core.PyList super__doDir(org.python.core.PyJavaPackage arg0, boolean arg1, boolean arg2) {
            return super.doDir(arg0, arg1, arg2);
        }
        
        public org.python.core.PyList doDir(org.python.core.PyJavaPackage arg0, boolean arg1, boolean arg2) {
            PyObject inst = Py.jfindattr(this, "doDir");
            if (inst != null) return (org.python.core.PyList)Py.tojava(inst._jcall(new Object[] {arg0, Py.newBoolean(arg1), Py.newBoolean(arg2)}), org.python.core.PyList.class);
            else return super.doDir(arg0, arg1, arg2);
        }
        
        public boolean super__filterByAccess(java.lang.String arg0, int arg1) {
            return super.filterByAccess(arg0, arg1);
        }
        
        public boolean filterByAccess(java.lang.String arg0, int arg1) {
            PyObject inst = Py.jfindattr(this, "filterByAccess");
            if (inst != null) return Py.py2boolean(inst._jcall(new Object[] {arg0, Py.newInteger(arg1)}));
            else return super.filterByAccess(arg0, arg1);
        }
        
        public boolean super__filterByName(java.lang.String arg0, boolean arg1) {
            return super.filterByName(arg0, arg1);
        }
        
        public boolean filterByName(java.lang.String arg0, boolean arg1) {
            PyObject inst = Py.jfindattr(this, "filterByName");
            if (inst != null) return Py.py2boolean(inst._jcall(new Object[] {arg0, Py.newBoolean(arg1)}));
            else return super.filterByName(arg0, arg1);
        }
        
        public void finalize() throws java.lang.Throwable {
            super.finalize();
        }
        
        public java.lang.Class super__findClass(java.lang.String arg0, java.lang.String arg1) {
            return super.findClass(arg0, arg1);
        }
        
        public java.lang.Class findClass(java.lang.String arg0, java.lang.String arg1) {
            PyObject inst = Py.jfindattr(this, "findClass");
            if (inst != null) return (java.lang.Class)Py.tojava(inst._jcall(new Object[] {arg0, arg1}), java.lang.Class.class);
            else return super.findClass(arg0, arg1);
        }
        
        public java.lang.Class findClass(java.lang.String arg0, java.lang.String arg1, java.lang.String arg2) {
            PyObject inst = Py.jgetattr(this, "findClass");
            return (java.lang.Class)Py.tojava(inst._jcall(new Object[] {arg0, arg1, arg2}), java.lang.Class.class);
        }
        
        public java.io.DataInputStream inOpenCacheFile(java.lang.String arg0) throws java.io.IOException {
            return super.inOpenCacheFile(arg0);
        }
        
        public java.io.DataInputStream inOpenIndex() throws java.io.IOException {
            return super.inOpenIndex();
        }
        
        public void initCache() {
            super.initCache();
        }
        
        public org.python.core.PyList merge(org.python.core.PyList arg0, org.python.core.PyList arg1) {
            return super.merge(arg0, arg1);
        }
        
        public void message(java.lang.String arg0) {
            super.message(arg0);
        }
        
        public java.io.DataOutputStream outCreateCacheFile(org.python.core.CachedJarsPackageManager.JarXEntry arg0, boolean arg1) throws java.io.IOException {
            return super.outCreateCacheFile(arg0, arg1);
        }
        
        public java.io.DataOutputStream outOpenIndex() throws java.io.IOException {
            return super.outOpenIndex();
        }
        
        public boolean super__packageExists(java.lang.String arg0, java.lang.String arg1) {
            return super.packageExists(arg0, arg1);
        }
        
        public boolean packageExists(java.lang.String arg0, java.lang.String arg1) {
            PyObject inst = Py.jfindattr(this, "packageExists");
            if (inst != null) return Py.py2boolean(inst._jcall(new Object[] {arg0, arg1}));
            else return super.packageExists(arg0, arg1);
        }
        
        public boolean super__packageExists(org.python.core.PyList arg0, java.lang.String arg1, java.lang.String arg2) {
            return super.packageExists(arg0, arg1, arg2);
        }
        
        public boolean packageExists(org.python.core.PyList arg0, java.lang.String arg1, java.lang.String arg2) {
            PyObject inst = Py.jfindattr(this, "packageExists");
            if (inst != null) return Py.py2boolean(inst._jcall(new Object[] {arg0, arg1, arg2}));
            else return super.packageExists(arg0, arg1, arg2);
        }
        
        public boolean useCacheDir(java.io.File arg0) {
            return super.useCacheDir(arg0);
        }
        
        public void warning(java.lang.String arg0) {
            super.warning(arg0);
        }
        
        public YaPM() {
            super();
            __initProxy__(new Object[] {});
        }
        
        private PyInstance __proxy;
        public void _setPyInstance(PyInstance inst) {
            __proxy = inst;
        }
        
        public PyInstance _getPyInstance() {
            return __proxy;
        }
        
        private PySystemState __sysstate;
        public void _setPySystemState(PySystemState inst) {
            __sysstate = inst;
        }
        
        public PySystemState _getPySystemState() {
            return __sysstate;
        }
        
        public void __initProxy__(Object[] args) {
            Py.initProxy(this, "yapm", "YaPM", args, yapm.jpy$packages, yapm.jpy$proxyProperties, "", new String[] {"string", "random", "util", "traceback", "sre_compile", "atexit", "sre", "sre_constants", "StringIO", "javaos", "socket", "yapm", "calendar", "repr", "copy_reg", "SocketServer", "server", "re", "linecache", "javapath", "UserDict", "copy", "threading", "stat", "PathVFS", "sre_parse"});
        }
        
        static public void classDictInit(PyObject dict) {
            dict.__setitem__("__supernames__", Py.java2py(new String[] {"deleteCacheFile", "finalize", "super__doDir", "comment", "super__filterByAccess", "initCache", "outCreateCacheFile", "merge", "super__filterByName", "useCacheDir", "message", "super__packageExists", "debug", "inOpenIndex", "warning", "super__findClass", "clone", "outOpenIndex", "basicDoDir", "inOpenCacheFile"}));
        }
        
    }
    public static void moduleDictInit(PyObject dict) {
        dict.__setitem__("__name__", new PyString("yapm"));
        Py.runCode(new _PyInner().getMain(), dict, dict);
    }
    
    public static void main(String[] args) throws java.lang.Exception {
        String[] newargs = new String[args.length+1];
        newargs[0] = "yapm";
        System.arraycopy(args, 0, newargs, 1, args.length);
        Py.runMain(yapm._PyInner.class, newargs, yapm.jpy$packages, yapm.jpy$mainProperties, "", new String[] {"string", "random", "util", "traceback", "sre_compile", "atexit", "sre", "sre_constants", "StringIO", "javaos", "socket", "yapm", "calendar", "repr", "copy_reg", "SocketServer", "server", "re", "linecache", "javapath", "UserDict", "copy", "threading", "stat", "PathVFS", "sre_parse"});
    }
    
}
