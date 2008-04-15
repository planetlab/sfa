import org.python.core.*;

public class StringIO extends java.lang.Object {
    static String[] jpy$mainProperties = new String[] {"python.modules.builtin", "exceptions:org.python.core.exceptions"};
    static String[] jpy$proxyProperties = new String[] {"python.modules.builtin", "exceptions:org.python.core.exceptions", "python.options.showJavaExceptions", "true"};
    static String[] jpy$packages = new String[] {"java.net", null, "java.lang", null, "org.python.core", null, "java.io", null, "java.util.zip", null};
    
    public static class _PyInner extends PyFunctionTable implements PyRunnable {
        private static PyObject s$0;
        private static PyObject i$1;
        private static PyObject s$2;
        private static PyObject i$3;
        private static PyObject s$4;
        private static PyObject i$5;
        private static PyObject s$6;
        private static PyObject i$7;
        private static PyObject s$8;
        private static PyObject s$9;
        private static PyObject s$10;
        private static PyObject s$11;
        private static PyObject s$12;
        private static PyObject s$13;
        private static PyObject s$14;
        private static PyObject s$15;
        private static PyObject s$16;
        private static PyObject s$17;
        private static PyObject s$18;
        private static PyObject s$19;
        private static PyObject s$20;
        private static PyObject s$21;
        private static PyObject s$22;
        private static PyObject s$23;
        private static PyFunctionTable funcTable;
        private static PyCode c$0___init__;
        private static PyCode c$1_close;
        private static PyCode c$2_isatty;
        private static PyCode c$3_seek;
        private static PyCode c$4_tell;
        private static PyCode c$5_read;
        private static PyCode c$6_readline;
        private static PyCode c$7_readlines;
        private static PyCode c$8_truncate;
        private static PyCode c$9_write;
        private static PyCode c$10_writelines;
        private static PyCode c$11_flush;
        private static PyCode c$12_getvalue;
        private static PyCode c$13_StringIO;
        private static PyCode c$14_test;
        private static PyCode c$15_main;
        private static void initConstants() {
            s$0 = Py.newString("File-like objects that read from or write to a string buffer.\012\012This implements (nearly) all stdio methods.\012\012f = StringIO()      # ready for writing\012f = StringIO(buf)   # ready for reading\012f.close()           # explicitly release resources held\012flag = f.isatty()   # always false\012pos = f.tell()      # get current position\012f.seek(pos)         # set current position\012f.seek(pos, mode)   # mode 0: absolute; 1: relative; 2: relative to EOF\012buf = f.read()      # read until EOF\012buf = f.read(n)     # read up to n bytes\012buf = f.readline()  # read until end of line ('\012') or EOF\012list = f.readlines()# list of f.readline() results until EOF\012f.truncate([size])  # truncate file at to at most size (default: current pos)\012f.write(buf)        # write at current position\012f.writelines(list)  # for line in list: f.write(line)\012f.getvalue()        # return whole file's contents as a string\012\012Notes:\012- Using a real file is often faster (but less convenient).\012- There's also a much faster implementation in C, called cStringIO, but\012  it's not subclassable.\012- fileno() is left unimplemented so that code which uses it triggers\012  an exception early.\012- Seeking far beyond EOF and then writing will insert real null\012  bytes that occupy space in the buffer.\012- There's a simple test set (see end of this file).\012");
            i$1 = Py.newInteger(22);
            s$2 = Py.newString("StringIO");
            i$3 = Py.newInteger(0);
            s$4 = Py.newString("");
            i$5 = Py.newInteger(1);
            s$6 = Py.newString("I/O operation on closed file");
            i$7 = Py.newInteger(2);
            s$8 = Py.newString("\012");
            s$9 = Py.newString("Negative size not allowed");
            s$10 = Py.newString("\000");
            s$11 = Py.newString("/etc/passwd");
            s$12 = Py.newString("r");
            s$13 = Py.newString("write failed");
            s$14 = Py.newString("File length =");
            s$15 = Py.newString("First line =");
            s$16 = Py.newString("Second line =");
            s$17 = Py.newString("bad result after seek back");
            s$18 = Py.newString("bad result after seek back from EOF");
            s$19 = Py.newString("Read");
            s$20 = Py.newString("more lines");
            s$21 = Py.newString("bad length");
            s$22 = Py.newString("__main__");
            s$23 = Py.newString("/usr/share/jython/Lib-cpython/StringIO.py");
            funcTable = new _PyInner();
            c$0___init__ = Py.newCode(2, new String[] {"self", "buf"}, "/usr/share/jython/Lib-cpython/StringIO.py", "__init__", false, false, funcTable, 0, null, null, 0, 1);
            c$1_close = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/StringIO.py", "close", false, false, funcTable, 1, null, null, 0, 1);
            c$2_isatty = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/StringIO.py", "isatty", false, false, funcTable, 2, null, null, 0, 1);
            c$3_seek = Py.newCode(3, new String[] {"self", "pos", "mode"}, "/usr/share/jython/Lib-cpython/StringIO.py", "seek", false, false, funcTable, 3, null, null, 0, 1);
            c$4_tell = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/StringIO.py", "tell", false, false, funcTable, 4, null, null, 0, 1);
            c$5_read = Py.newCode(2, new String[] {"self", "n", "r", "newpos"}, "/usr/share/jython/Lib-cpython/StringIO.py", "read", false, false, funcTable, 5, null, null, 0, 1);
            c$6_readline = Py.newCode(2, new String[] {"self", "length", "i", "r", "newpos"}, "/usr/share/jython/Lib-cpython/StringIO.py", "readline", false, false, funcTable, 6, null, null, 0, 1);
            c$7_readlines = Py.newCode(2, new String[] {"self", "sizehint", "line", "lines", "total"}, "/usr/share/jython/Lib-cpython/StringIO.py", "readlines", false, false, funcTable, 7, null, null, 0, 1);
            c$8_truncate = Py.newCode(2, new String[] {"self", "size"}, "/usr/share/jython/Lib-cpython/StringIO.py", "truncate", false, false, funcTable, 8, null, null, 0, 1);
            c$9_write = Py.newCode(2, new String[] {"self", "s", "newpos"}, "/usr/share/jython/Lib-cpython/StringIO.py", "write", false, false, funcTable, 9, null, null, 0, 1);
            c$10_writelines = Py.newCode(2, new String[] {"self", "list"}, "/usr/share/jython/Lib-cpython/StringIO.py", "writelines", false, false, funcTable, 10, null, null, 0, 1);
            c$11_flush = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/StringIO.py", "flush", false, false, funcTable, 11, null, null, 0, 1);
            c$12_getvalue = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/StringIO.py", "getvalue", false, false, funcTable, 12, null, null, 0, 1);
            c$13_StringIO = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/StringIO.py", "StringIO", false, false, funcTable, 13, null, null, 0, 0);
            c$14_test = Py.newCode(0, new String[] {"length", "file", "f", "list", "here", "line2", "text", "sys", "lines", "line"}, "/usr/share/jython/Lib-cpython/StringIO.py", "test", false, false, funcTable, 14, null, null, 0, 1);
            c$15_main = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/StringIO.py", "main", false, false, funcTable, 15, null, null, 0, 0);
        }
        
        
        public PyCode getMain() {
            if (c$15_main == null) _PyInner.initConstants();
            return c$15_main;
        }
        
        public PyObject call_function(int index, PyFrame frame) {
            switch (index){
                case 0:
                return _PyInner.__init__$1(frame);
                case 1:
                return _PyInner.close$2(frame);
                case 2:
                return _PyInner.isatty$3(frame);
                case 3:
                return _PyInner.seek$4(frame);
                case 4:
                return _PyInner.tell$5(frame);
                case 5:
                return _PyInner.read$6(frame);
                case 6:
                return _PyInner.readline$7(frame);
                case 7:
                return _PyInner.readlines$8(frame);
                case 8:
                return _PyInner.truncate$9(frame);
                case 9:
                return _PyInner.write$10(frame);
                case 10:
                return _PyInner.writelines$11(frame);
                case 11:
                return _PyInner.flush$12(frame);
                case 12:
                return _PyInner.getvalue$13(frame);
                case 13:
                return _PyInner.StringIO$14(frame);
                case 14:
                return _PyInner.test$15(frame);
                case 15:
                return _PyInner.main$16(frame);
                default:
                return null;
            }
        }
        
        private static PyObject __init__$1(PyFrame frame) {
            frame.getlocal(0).__setattr__("buf", frame.getlocal(1));
            frame.getlocal(0).__setattr__("len", frame.getglobal("len").__call__(frame.getlocal(1)));
            frame.getlocal(0).__setattr__("buflist", new PyList(new PyObject[] {}));
            frame.getlocal(0).__setattr__("pos", i$3);
            frame.getlocal(0).__setattr__("closed", i$3);
            frame.getlocal(0).__setattr__("softspace", i$3);
            return Py.None;
        }
        
        private static PyObject close$2(PyFrame frame) {
            if (frame.getlocal(0).__getattr__("closed").__not__().__nonzero__()) {
                frame.getlocal(0).__setattr__("closed", i$5);
                frame.getlocal(0).__delattr__("buf");
                frame.getlocal(0).__delattr__("pos");
            }
            return Py.None;
        }
        
        private static PyObject isatty$3(PyFrame frame) {
            if (frame.getlocal(0).__getattr__("closed").__nonzero__()) {
                throw Py.makeException(frame.getglobal("ValueError"), s$6);
            }
            return i$3;
        }
        
        private static PyObject seek$4(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            if (frame.getlocal(0).__getattr__("closed").__nonzero__()) {
                throw Py.makeException(frame.getglobal("ValueError"), s$6);
            }
            if (frame.getlocal(0).__getattr__("buflist").__nonzero__()) {
                t$0$PyObject = s$4.invoke("join", frame.getlocal(0).__getattr__("buflist"));
                t$1$PyObject = frame.getlocal(0);
                t$1$PyObject.__setattr__("buf", t$1$PyObject.__getattr__("buf").__iadd__(t$0$PyObject));
                frame.getlocal(0).__setattr__("buflist", new PyList(new PyObject[] {}));
            }
            if (frame.getlocal(2)._eq(i$5).__nonzero__()) {
                t$0$PyObject = frame.getlocal(0).__getattr__("pos");
                frame.setlocal(1, frame.getlocal(1).__iadd__(t$0$PyObject));
            }
            else if (frame.getlocal(2)._eq(i$7).__nonzero__()) {
                t$0$PyObject = frame.getlocal(0).__getattr__("len");
                frame.setlocal(1, frame.getlocal(1).__iadd__(t$0$PyObject));
            }
            frame.getlocal(0).__setattr__("pos", frame.getglobal("max").__call__(i$3, frame.getlocal(1)));
            return Py.None;
        }
        
        private static PyObject tell$5(PyFrame frame) {
            if (frame.getlocal(0).__getattr__("closed").__nonzero__()) {
                throw Py.makeException(frame.getglobal("ValueError"), s$6);
            }
            return frame.getlocal(0).__getattr__("pos");
        }
        
        private static PyObject read$6(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            if (frame.getlocal(0).__getattr__("closed").__nonzero__()) {
                throw Py.makeException(frame.getglobal("ValueError"), s$6);
            }
            if (frame.getlocal(0).__getattr__("buflist").__nonzero__()) {
                t$0$PyObject = s$4.invoke("join", frame.getlocal(0).__getattr__("buflist"));
                t$1$PyObject = frame.getlocal(0);
                t$1$PyObject.__setattr__("buf", t$1$PyObject.__getattr__("buf").__iadd__(t$0$PyObject));
                frame.getlocal(0).__setattr__("buflist", new PyList(new PyObject[] {}));
            }
            if (frame.getlocal(1)._lt(i$3).__nonzero__()) {
                frame.setlocal(3, frame.getlocal(0).__getattr__("len"));
            }
            else {
                frame.setlocal(3, frame.getglobal("min").__call__(frame.getlocal(0).__getattr__("pos")._add(frame.getlocal(1)), frame.getlocal(0).__getattr__("len")));
            }
            frame.setlocal(2, frame.getlocal(0).__getattr__("buf").__getslice__(frame.getlocal(0).__getattr__("pos"), frame.getlocal(3), null));
            frame.getlocal(0).__setattr__("pos", frame.getlocal(3));
            return frame.getlocal(2);
        }
        
        private static PyObject readline$7(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            if (frame.getlocal(0).__getattr__("closed").__nonzero__()) {
                throw Py.makeException(frame.getglobal("ValueError"), s$6);
            }
            if (frame.getlocal(0).__getattr__("buflist").__nonzero__()) {
                t$0$PyObject = s$4.invoke("join", frame.getlocal(0).__getattr__("buflist"));
                t$1$PyObject = frame.getlocal(0);
                t$1$PyObject.__setattr__("buf", t$1$PyObject.__getattr__("buf").__iadd__(t$0$PyObject));
                frame.getlocal(0).__setattr__("buflist", new PyList(new PyObject[] {}));
            }
            frame.setlocal(2, frame.getlocal(0).__getattr__("buf").invoke("find", s$8, frame.getlocal(0).__getattr__("pos")));
            if (frame.getlocal(2)._lt(i$3).__nonzero__()) {
                frame.setlocal(4, frame.getlocal(0).__getattr__("len"));
            }
            else {
                frame.setlocal(4, frame.getlocal(2)._add(i$5));
            }
            if (frame.getlocal(1)._isnot(frame.getglobal("None")).__nonzero__()) {
                if (frame.getlocal(0).__getattr__("pos")._add(frame.getlocal(1))._lt(frame.getlocal(4)).__nonzero__()) {
                    frame.setlocal(4, frame.getlocal(0).__getattr__("pos")._add(frame.getlocal(1)));
                }
            }
            frame.setlocal(3, frame.getlocal(0).__getattr__("buf").__getslice__(frame.getlocal(0).__getattr__("pos"), frame.getlocal(4), null));
            frame.getlocal(0).__setattr__("pos", frame.getlocal(4));
            return frame.getlocal(3);
        }
        
        private static PyObject readlines$8(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject;
            
            // Code
            frame.setlocal(4, i$3);
            frame.setlocal(3, new PyList(new PyObject[] {}));
            frame.setlocal(2, frame.getlocal(0).invoke("readline"));
            while (frame.getlocal(2).__nonzero__()) {
                frame.getlocal(3).invoke("append", frame.getlocal(2));
                t$0$PyObject = frame.getglobal("len").__call__(frame.getlocal(2));
                frame.setlocal(4, frame.getlocal(4).__iadd__(t$0$PyObject));
                if ((i$3._lt(t$0$PyObject = frame.getlocal(1)).__nonzero__() ? t$0$PyObject._le(frame.getlocal(4)) : Py.Zero).__nonzero__()) {
                    break;
                }
                frame.setlocal(2, frame.getlocal(0).invoke("readline"));
            }
            return frame.getlocal(3);
        }
        
        private static PyObject truncate$9(PyFrame frame) {
            if (frame.getlocal(0).__getattr__("closed").__nonzero__()) {
                throw Py.makeException(frame.getglobal("ValueError"), s$6);
            }
            if (frame.getlocal(1)._is(frame.getglobal("None")).__nonzero__()) {
                frame.setlocal(1, frame.getlocal(0).__getattr__("pos"));
            }
            else if (frame.getlocal(1)._lt(i$3).__nonzero__()) {
                throw Py.makeException(frame.getglobal("IOError").__call__(frame.getglobal("EINVAL"), s$9));
            }
            else if (frame.getlocal(1)._lt(frame.getlocal(0).__getattr__("pos")).__nonzero__()) {
                frame.getlocal(0).__setattr__("pos", frame.getlocal(1));
            }
            frame.getlocal(0).__setattr__("buf", frame.getlocal(0).invoke("getvalue").__getslice__(null, frame.getlocal(1), null));
            return Py.None;
        }
        
        private static PyObject write$10(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            if (frame.getlocal(0).__getattr__("closed").__nonzero__()) {
                throw Py.makeException(frame.getglobal("ValueError"), s$6);
            }
            if (frame.getlocal(1).__not__().__nonzero__()) {
                return Py.None;
            }
            if (frame.getlocal(0).__getattr__("pos")._gt(frame.getlocal(0).__getattr__("len")).__nonzero__()) {
                frame.getlocal(0).__getattr__("buflist").invoke("append", s$10._mul(frame.getlocal(0).__getattr__("pos")._sub(frame.getlocal(0).__getattr__("len"))));
                frame.getlocal(0).__setattr__("len", frame.getlocal(0).__getattr__("pos"));
            }
            frame.setlocal(2, frame.getlocal(0).__getattr__("pos")._add(frame.getglobal("len").__call__(frame.getlocal(1))));
            if (frame.getlocal(0).__getattr__("pos")._lt(frame.getlocal(0).__getattr__("len")).__nonzero__()) {
                if (frame.getlocal(0).__getattr__("buflist").__nonzero__()) {
                    t$0$PyObject = s$4.invoke("join", frame.getlocal(0).__getattr__("buflist"));
                    t$1$PyObject = frame.getlocal(0);
                    t$1$PyObject.__setattr__("buf", t$1$PyObject.__getattr__("buf").__iadd__(t$0$PyObject));
                    frame.getlocal(0).__setattr__("buflist", new PyList(new PyObject[] {}));
                }
                frame.getlocal(0).__setattr__("buflist", new PyList(new PyObject[] {frame.getlocal(0).__getattr__("buf").__getslice__(null, frame.getlocal(0).__getattr__("pos"), null), frame.getlocal(1), frame.getlocal(0).__getattr__("buf").__getslice__(frame.getlocal(2), null, null)}));
                frame.getlocal(0).__setattr__("buf", s$4);
                if (frame.getlocal(2)._gt(frame.getlocal(0).__getattr__("len")).__nonzero__()) {
                    frame.getlocal(0).__setattr__("len", frame.getlocal(2));
                }
            }
            else {
                frame.getlocal(0).__getattr__("buflist").invoke("append", frame.getlocal(1));
                frame.getlocal(0).__setattr__("len", frame.getlocal(2));
            }
            frame.getlocal(0).__setattr__("pos", frame.getlocal(2));
            return Py.None;
        }
        
        private static PyObject writelines$11(PyFrame frame) {
            frame.getlocal(0).invoke("write", s$4.invoke("join", frame.getlocal(1)));
            return Py.None;
        }
        
        private static PyObject flush$12(PyFrame frame) {
            if (frame.getlocal(0).__getattr__("closed").__nonzero__()) {
                throw Py.makeException(frame.getglobal("ValueError"), s$6);
            }
            return Py.None;
        }
        
        private static PyObject getvalue$13(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            if (frame.getlocal(0).__getattr__("buflist").__nonzero__()) {
                t$0$PyObject = s$4.invoke("join", frame.getlocal(0).__getattr__("buflist"));
                t$1$PyObject = frame.getlocal(0);
                t$1$PyObject.__setattr__("buf", t$1$PyObject.__getattr__("buf").__iadd__(t$0$PyObject));
                frame.getlocal(0).__setattr__("buflist", new PyList(new PyObject[] {}));
            }
            return frame.getlocal(0).__getattr__("buf");
        }
        
        private static PyObject StringIO$14(PyFrame frame) {
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {s$4}, c$0___init__));
            frame.setlocal("close", new PyFunction(frame.f_globals, new PyObject[] {}, c$1_close));
            frame.setlocal("isatty", new PyFunction(frame.f_globals, new PyObject[] {}, c$2_isatty));
            frame.setlocal("seek", new PyFunction(frame.f_globals, new PyObject[] {i$3}, c$3_seek));
            frame.setlocal("tell", new PyFunction(frame.f_globals, new PyObject[] {}, c$4_tell));
            frame.setlocal("read", new PyFunction(frame.f_globals, new PyObject[] {i$5.__neg__()}, c$5_read));
            frame.setlocal("readline", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$6_readline));
            frame.setlocal("readlines", new PyFunction(frame.f_globals, new PyObject[] {i$3}, c$7_readlines));
            frame.setlocal("truncate", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$8_truncate));
            frame.setlocal("write", new PyFunction(frame.f_globals, new PyObject[] {}, c$9_write));
            frame.setlocal("writelines", new PyFunction(frame.f_globals, new PyObject[] {}, c$10_writelines));
            frame.setlocal("flush", new PyFunction(frame.f_globals, new PyObject[] {}, c$11_flush));
            frame.setlocal("getvalue", new PyFunction(frame.f_globals, new PyObject[] {}, c$12_getvalue));
            return frame.getf_locals();
        }
        
        private static PyObject test$15(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            frame.setlocal(7, org.python.core.imp.importOne("sys", frame));
            if (frame.getlocal(7).__getattr__("argv").__getslice__(i$5, null, null).__nonzero__()) {
                frame.setlocal(1, frame.getlocal(7).__getattr__("argv").__getitem__(i$5));
            }
            else {
                frame.setlocal(1, s$11);
            }
            frame.setlocal(8, frame.getglobal("open").__call__(frame.getlocal(1), s$12).invoke("readlines"));
            frame.setlocal(6, frame.getglobal("open").__call__(frame.getlocal(1), s$12).invoke("read"));
            frame.setlocal(2, frame.getglobal("StringIO").__call__());
            t$0$int = 0;
            t$1$PyObject = frame.getlocal(8).__getslice__(null, i$7.__neg__(), null);
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                frame.setlocal(9, t$0$PyObject);
                frame.getlocal(2).invoke("write", frame.getlocal(9));
            }
            frame.getlocal(2).invoke("writelines", frame.getlocal(8).__getslice__(i$7.__neg__(), null, null));
            if (frame.getlocal(2).invoke("getvalue")._ne(frame.getlocal(6)).__nonzero__()) {
                throw Py.makeException(frame.getglobal("RuntimeError"), s$13);
            }
            frame.setlocal(0, frame.getlocal(2).invoke("tell"));
            Py.printComma(s$14);
            Py.println(frame.getlocal(0));
            frame.getlocal(2).invoke("seek", frame.getglobal("len").__call__(frame.getlocal(8).__getitem__(i$3)));
            frame.getlocal(2).invoke("write", frame.getlocal(8).__getitem__(i$5));
            frame.getlocal(2).invoke("seek", i$3);
            Py.printComma(s$15);
            Py.println(frame.getlocal(2).invoke("readline").__repr__());
            frame.setlocal(4, frame.getlocal(2).invoke("tell"));
            frame.setlocal(9, frame.getlocal(2).invoke("readline"));
            Py.printComma(s$16);
            Py.println(frame.getlocal(9).__repr__());
            frame.getlocal(2).invoke("seek", frame.getglobal("len").__call__(frame.getlocal(9)).__neg__(), i$5);
            frame.setlocal(5, frame.getlocal(2).invoke("read", frame.getglobal("len").__call__(frame.getlocal(9))));
            if (frame.getlocal(9)._ne(frame.getlocal(5)).__nonzero__()) {
                throw Py.makeException(frame.getglobal("RuntimeError"), s$17);
            }
            frame.getlocal(2).invoke("seek", frame.getglobal("len").__call__(frame.getlocal(5)), i$5);
            frame.setlocal(3, frame.getlocal(2).invoke("readlines"));
            frame.setlocal(9, frame.getlocal(3).__getitem__(i$5.__neg__()));
            frame.getlocal(2).invoke("seek", frame.getlocal(2).invoke("tell")._sub(frame.getglobal("len").__call__(frame.getlocal(9))));
            frame.setlocal(5, frame.getlocal(2).invoke("read"));
            if (frame.getlocal(9)._ne(frame.getlocal(5)).__nonzero__()) {
                throw Py.makeException(frame.getglobal("RuntimeError"), s$18);
            }
            Py.printComma(s$19);
            Py.printComma(frame.getglobal("len").__call__(frame.getlocal(3)));
            Py.println(s$20);
            Py.printComma(s$14);
            Py.println(frame.getlocal(2).invoke("tell"));
            if (frame.getlocal(2).invoke("tell")._ne(frame.getlocal(0)).__nonzero__()) {
                throw Py.makeException(frame.getglobal("RuntimeError"), s$21);
            }
            frame.getlocal(2).invoke("close");
            return Py.None;
        }
        
        private static PyObject main$16(PyFrame frame) {
            frame.setglobal("__file__", s$23);
            
            PyObject[] imp_accu;
            // Temporary Variables
            PyException t$0$PyException;
            
            // Code
            /* File-like objects that read from or write to a string buffer.
            
            This implements (nearly) all stdio methods.
            
            f = StringIO()      # ready for writing
            f = StringIO(buf)   # ready for reading
            f.close()           # explicitly release resources held
            flag = f.isatty()   # always false
            pos = f.tell()      # get current position
            f.seek(pos)         # set current position
            f.seek(pos, mode)   # mode 0: absolute; 1: relative; 2: relative to EOF
            buf = f.read()      # read until EOF
            buf = f.read(n)     # read up to n bytes
            buf = f.readline()  # read until end of line ('
            ') or EOF
            list = f.readlines()# list of f.readline() results until EOF
            f.truncate([size])  # truncate file at to at most size (default: current pos)
            f.write(buf)        # write at current position
            f.writelines(list)  # for line in list: f.write(line)
            f.getvalue()        # return whole file's contents as a string
            
            Notes:
            - Using a real file is often faster (but less convenient).
            - There's also a much faster implementation in C, called cStringIO, but
              it's not subclassable.
            - fileno() is left unimplemented so that code which uses it triggers
              an exception early.
            - Seeking far beyond EOF and then writing will insert real null
              bytes that occupy space in the buffer.
            - There's a simple test set (see end of this file).
             */
            try {
                imp_accu = org.python.core.imp.importFrom("errno", new String[] {"EINVAL"}, frame);
                frame.setlocal("EINVAL", imp_accu[0]);
                imp_accu = null;
            }
            catch (Throwable x$0) {
                t$0$PyException = Py.setException(x$0, frame);
                if (Py.matchException(t$0$PyException, frame.getname("ImportError"))) {
                    frame.setlocal("EINVAL", i$1);
                }
                else throw t$0$PyException;
            }
            frame.setlocal("__all__", new PyList(new PyObject[] {s$2}));
            frame.setlocal("StringIO", Py.makeClass("StringIO", new PyObject[] {}, c$13_StringIO, null));
            frame.setlocal("test", new PyFunction(frame.f_globals, new PyObject[] {}, c$14_test));
            if (frame.getname("__name__")._eq(s$22).__nonzero__()) {
                frame.getname("test").__call__();
            }
            return Py.None;
        }
        
    }
    public static void moduleDictInit(PyObject dict) {
        dict.__setitem__("__name__", new PyString("StringIO"));
        Py.runCode(new _PyInner().getMain(), dict, dict);
    }
    
    public static void main(String[] args) throws java.lang.Exception {
        String[] newargs = new String[args.length+1];
        newargs[0] = "StringIO";
        System.arraycopy(args, 0, newargs, 1, args.length);
        Py.runMain(StringIO._PyInner.class, newargs, StringIO.jpy$packages, StringIO.jpy$mainProperties, "", new String[] {"string", "random", "util", "traceback", "sre_compile", "atexit", "sre", "sre_constants", "StringIO", "javaos", "socket", "yapm", "calendar", "repr", "copy_reg", "SocketServer", "server", "re", "linecache", "javapath", "UserDict", "copy", "threading", "stat", "PathVFS", "sre_parse"});
    }
    
}
