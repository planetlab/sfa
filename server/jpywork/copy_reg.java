import org.python.core.*;

public class copy_reg extends java.lang.Object {
    static String[] jpy$mainProperties = new String[] {"python.modules.builtin", "exceptions:org.python.core.exceptions"};
    static String[] jpy$proxyProperties = new String[] {"python.modules.builtin", "exceptions:org.python.core.exceptions", "python.options.showJavaExceptions", "true"};
    static String[] jpy$packages = new String[] {"java.net", null, "java.lang", null, "org.python.core", null, "java.io", null, "java.util.zip", null};
    
    public static class _PyInner extends PyFunctionTable implements PyRunnable {
        private static PyObject s$0;
        private static PyObject s$1;
        private static PyObject s$2;
        private static PyObject s$3;
        private static PyObject s$4;
        private static PyObject s$5;
        private static PyObject i$6;
        private static PyObject j$7;
        private static PyObject s$8;
        private static PyFunctionTable funcTable;
        private static PyCode c$0_pickle;
        private static PyCode c$1_constructor;
        private static PyCode c$2_pickle_complex;
        private static PyCode c$3_main;
        private static void initConstants() {
            s$0 = Py.newString("Helper to provide extensibility for pickle/cPickle.\012\012This is only useful to add pickle support for extension types defined in\012C, not for instances of user-defined classes.\012");
            s$1 = Py.newString("pickle");
            s$2 = Py.newString("constructor");
            s$3 = Py.newString("copy_reg is not intended for use with classes");
            s$4 = Py.newString("reduction functions must be callable");
            s$5 = Py.newString("constructors must be callable");
            i$6 = Py.newInteger(1);
            j$7 = Py.newImaginary(1.0);
            s$8 = Py.newString("/usr/share/jython/Lib-cpython/copy_reg.py");
            funcTable = new _PyInner();
            c$0_pickle = Py.newCode(3, new String[] {"ob_type", "pickle_function", "constructor_ob"}, "/usr/share/jython/Lib-cpython/copy_reg.py", "pickle", false, false, funcTable, 0, null, null, 0, 1);
            c$1_constructor = Py.newCode(1, new String[] {"object"}, "/usr/share/jython/Lib-cpython/copy_reg.py", "constructor", false, false, funcTable, 1, null, null, 0, 1);
            c$2_pickle_complex = Py.newCode(1, new String[] {"c"}, "/usr/share/jython/Lib-cpython/copy_reg.py", "pickle_complex", false, false, funcTable, 2, null, null, 0, 1);
            c$3_main = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/copy_reg.py", "main", false, false, funcTable, 3, null, null, 0, 0);
        }
        
        
        public PyCode getMain() {
            if (c$3_main == null) _PyInner.initConstants();
            return c$3_main;
        }
        
        public PyObject call_function(int index, PyFrame frame) {
            switch (index){
                case 0:
                return _PyInner.pickle$1(frame);
                case 1:
                return _PyInner.constructor$2(frame);
                case 2:
                return _PyInner.pickle_complex$3(frame);
                case 3:
                return _PyInner.main$4(frame);
                default:
                return null;
            }
        }
        
        private static PyObject pickle$1(PyFrame frame) {
            if (frame.getglobal("type").__call__(frame.getlocal(0))._is(frame.getglobal("_ClassType")).__nonzero__()) {
                throw Py.makeException(frame.getglobal("TypeError").__call__(s$3));
            }
            if (frame.getglobal("callable").__call__(frame.getlocal(1)).__not__().__nonzero__()) {
                throw Py.makeException(frame.getglobal("TypeError").__call__(s$4));
            }
            frame.getglobal("dispatch_table").__setitem__(frame.getlocal(0), frame.getlocal(1));
            if (frame.getlocal(2)._isnot(frame.getglobal("None")).__nonzero__()) {
                frame.getglobal("constructor").__call__(frame.getlocal(2));
            }
            return Py.None;
        }
        
        private static PyObject constructor$2(PyFrame frame) {
            if (frame.getglobal("callable").__call__(frame.getlocal(0)).__not__().__nonzero__()) {
                throw Py.makeException(frame.getglobal("TypeError").__call__(s$5));
            }
            frame.getglobal("safe_constructors").__setitem__(frame.getlocal(0), i$6);
            return Py.None;
        }
        
        private static PyObject pickle_complex$3(PyFrame frame) {
            return new PyTuple(new PyObject[] {frame.getglobal("complex"), new PyTuple(new PyObject[] {frame.getlocal(0).__getattr__("real"), frame.getlocal(0).__getattr__("imag")})});
        }
        
        private static PyObject main$4(PyFrame frame) {
            frame.setglobal("__file__", s$8);
            
            PyObject[] imp_accu;
            // Code
            /* Helper to provide extensibility for pickle/cPickle.
            
            This is only useful to add pickle support for extension types defined in
            C, not for instances of user-defined classes.
             */
            imp_accu = org.python.core.imp.importFrom("types", new String[] {"ClassType"}, frame);
            frame.setlocal("_ClassType", imp_accu[0]);
            imp_accu = null;
            frame.setlocal("__all__", new PyList(new PyObject[] {s$1, s$2}));
            frame.setlocal("dispatch_table", new PyDictionary(new PyObject[] {}));
            frame.setlocal("safe_constructors", new PyDictionary(new PyObject[] {}));
            frame.setlocal("pickle", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$0_pickle));
            frame.setlocal("constructor", new PyFunction(frame.f_globals, new PyObject[] {}, c$1_constructor));
            frame.setlocal("pickle_complex", new PyFunction(frame.f_globals, new PyObject[] {}, c$2_pickle_complex));
            frame.getname("pickle").__call__(frame.getname("type").__call__(j$7), frame.getname("pickle_complex"), frame.getname("complex"));
            return Py.None;
        }
        
    }
    public static void moduleDictInit(PyObject dict) {
        dict.__setitem__("__name__", new PyString("copy_reg"));
        Py.runCode(new _PyInner().getMain(), dict, dict);
    }
    
    public static void main(String[] args) throws java.lang.Exception {
        String[] newargs = new String[args.length+1];
        newargs[0] = "copy_reg";
        System.arraycopy(args, 0, newargs, 1, args.length);
        Py.runMain(copy_reg._PyInner.class, newargs, copy_reg.jpy$packages, copy_reg.jpy$mainProperties, "", new String[] {"string", "random", "util", "traceback", "sre_compile", "atexit", "sre", "sre_constants", "StringIO", "javaos", "socket", "yapm", "calendar", "repr", "copy_reg", "SocketServer", "server", "re", "linecache", "javapath", "UserDict", "copy", "threading", "stat", "PathVFS", "sre_parse"});
    }
    
}
