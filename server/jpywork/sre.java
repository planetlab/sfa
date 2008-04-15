import org.python.core.*;

public class sre extends java.lang.Object {
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
        private static PyObject s$6;
        private static PyObject s$7;
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
        private static PyObject s$24;
        private static PyObject i$25;
        private static PyObject s$26;
        private static PyObject s$27;
        private static PyObject s$28;
        private static PyObject s$29;
        private static PyObject s$30;
        private static PyObject s$31;
        private static PyObject s$32;
        private static PyObject s$33;
        private static PyObject s$34;
        private static PyObject s$35;
        private static PyObject s$36;
        private static PyObject s$37;
        private static PyObject s$38;
        private static PyObject s$39;
        private static PyObject s$40;
        private static PyObject s$41;
        private static PyObject s$42;
        private static PyObject s$43;
        private static PyObject i$44;
        private static PyObject i$45;
        private static PyObject s$46;
        private static PyObject s$47;
        private static PyFunctionTable funcTable;
        private static PyCode c$0_match;
        private static PyCode c$1_search;
        private static PyCode c$2_sub;
        private static PyCode c$3_subn;
        private static PyCode c$4_split;
        private static PyCode c$5_findall;
        private static PyCode c$6_compile;
        private static PyCode c$7_purge;
        private static PyCode c$8_template;
        private static PyCode c$9_escape;
        private static PyCode c$10__join;
        private static PyCode c$11__compile;
        private static PyCode c$12__compile_repl;
        private static PyCode c$13__expand;
        private static PyCode c$14__sub;
        private static PyCode c$15_filter;
        private static PyCode c$16__subn;
        private static PyCode c$17__split;
        private static PyCode c$18__pickle;
        private static PyCode c$19___init__;
        private static PyCode c$20_scan;
        private static PyCode c$21_Scanner;
        private static PyCode c$22_main;
        private static void initConstants() {
            s$0 = Py.newString("match");
            s$1 = Py.newString("search");
            s$2 = Py.newString("sub");
            s$3 = Py.newString("subn");
            s$4 = Py.newString("split");
            s$5 = Py.newString("findall");
            s$6 = Py.newString("compile");
            s$7 = Py.newString("purge");
            s$8 = Py.newString("template");
            s$9 = Py.newString("escape");
            s$10 = Py.newString("I");
            s$11 = Py.newString("L");
            s$12 = Py.newString("M");
            s$13 = Py.newString("S");
            s$14 = Py.newString("X");
            s$15 = Py.newString("U");
            s$16 = Py.newString("IGNORECASE");
            s$17 = Py.newString("LOCALE");
            s$18 = Py.newString("MULTILINE");
            s$19 = Py.newString("DOTALL");
            s$20 = Py.newString("VERBOSE");
            s$21 = Py.newString("UNICODE");
            s$22 = Py.newString("error");
            s$23 = Py.newString("2.1b2");
            s$24 = Py.newString("Try to apply the pattern at the start of the string, returning\012    a match object, or None if no match was found.");
            i$25 = Py.newInteger(0);
            s$26 = Py.newString("Scan through string looking for a match to the pattern, returning\012    a match object, or None if no match was found.");
            s$27 = Py.newString("Return the string obtained by replacing the leftmost\012    non-overlapping occurrences of the pattern in string by the\012    replacement repl");
            s$28 = Py.newString("Return a 2-tuple containing (new_string, number).\012    new_string is the string obtained by replacing the leftmost\012    non-overlapping occurrences of the pattern in the source\012    string by the replacement repl.  number is the number of\012    substitutions that were made.");
            s$29 = Py.newString("Split the source string by the occurrences of the pattern,\012    returning a list containing the resulting substrings.");
            s$30 = Py.newString("Return a list of all non-overlapping matches in the string.\012\012    If one or more groups are present in the pattern, return a\012    list of groups; this will be a list of tuples if the pattern\012    has more than one group.\012\012    Empty matches are included in the result.");
            s$31 = Py.newString("Compile a regular expression pattern, returning a pattern object.");
            s$32 = Py.newString("Clear the regular expression cache");
            s$33 = Py.newString("Compile a template pattern, returning a pattern object");
            s$34 = Py.newString("Escape all non-alphanumeric characters in pattern.");
            s$35 = Py.newString("a");
            s$36 = Py.newString("z");
            s$37 = Py.newString("A");
            s$38 = Py.newString("Z");
            s$39 = Py.newString("0");
            s$40 = Py.newString("9");
            s$41 = Py.newString("\000");
            s$42 = Py.newString("\\000");
            s$43 = Py.newString("\\");
            i$44 = Py.newInteger(100);
            i$45 = Py.newInteger(1);
            s$46 = Py.newString("");
            s$47 = Py.newString("/usr/share/jython/Lib-cpython/sre.py");
            funcTable = new _PyInner();
            c$0_match = Py.newCode(3, new String[] {"pattern", "string", "flags"}, "/usr/share/jython/Lib-cpython/sre.py", "match", false, false, funcTable, 0, null, null, 0, 1);
            c$1_search = Py.newCode(3, new String[] {"pattern", "string", "flags"}, "/usr/share/jython/Lib-cpython/sre.py", "search", false, false, funcTable, 1, null, null, 0, 1);
            c$2_sub = Py.newCode(4, new String[] {"pattern", "repl", "string", "count"}, "/usr/share/jython/Lib-cpython/sre.py", "sub", false, false, funcTable, 2, null, null, 0, 1);
            c$3_subn = Py.newCode(4, new String[] {"pattern", "repl", "string", "count"}, "/usr/share/jython/Lib-cpython/sre.py", "subn", false, false, funcTable, 3, null, null, 0, 1);
            c$4_split = Py.newCode(3, new String[] {"pattern", "string", "maxsplit"}, "/usr/share/jython/Lib-cpython/sre.py", "split", false, false, funcTable, 4, null, null, 0, 1);
            c$5_findall = Py.newCode(3, new String[] {"pattern", "string", "maxsplit"}, "/usr/share/jython/Lib-cpython/sre.py", "findall", false, false, funcTable, 5, null, null, 0, 1);
            c$6_compile = Py.newCode(2, new String[] {"pattern", "flags"}, "/usr/share/jython/Lib-cpython/sre.py", "compile", false, false, funcTable, 6, null, null, 0, 1);
            c$7_purge = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/sre.py", "purge", false, false, funcTable, 7, null, null, 0, 1);
            c$8_template = Py.newCode(2, new String[] {"pattern", "flags"}, "/usr/share/jython/Lib-cpython/sre.py", "template", false, false, funcTable, 8, null, null, 0, 1);
            c$9_escape = Py.newCode(1, new String[] {"pattern", "i", "s", "c"}, "/usr/share/jython/Lib-cpython/sre.py", "escape", false, false, funcTable, 9, null, null, 0, 1);
            c$10__join = Py.newCode(2, new String[] {"seq", "sep"}, "/usr/share/jython/Lib-cpython/sre.py", "_join", false, false, funcTable, 10, null, null, 0, 1);
            c$11__compile = Py.newCode(1, new String[] {"key", "p", "flags", "pattern", "v"}, "/usr/share/jython/Lib-cpython/sre.py", "_compile", true, false, funcTable, 11, null, null, 0, 1);
            c$12__compile_repl = Py.newCode(1, new String[] {"key", "p", "repl", "pattern", "v"}, "/usr/share/jython/Lib-cpython/sre.py", "_compile_repl", true, false, funcTable, 12, null, null, 0, 1);
            c$13__expand = Py.newCode(3, new String[] {"pattern", "match", "template"}, "/usr/share/jython/Lib-cpython/sre.py", "_expand", false, false, funcTable, 13, null, null, 0, 1);
            c$14__sub = Py.newCode(4, new String[] {"pattern", "template", "string", "count"}, "/usr/share/jython/Lib-cpython/sre.py", "_sub", false, false, funcTable, 14, null, null, 0, 1);
            c$15_filter = Py.newCode(2, new String[] {"match", "template"}, "/usr/share/jython/Lib-cpython/sre.py", "filter", false, false, funcTable, 15, null, null, 0, 1);
            c$16__subn = Py.newCode(4, new String[] {"pattern", "template", "string", "count", "filter", "append", "n", "m", "i", "e", "c", "b", "s"}, "/usr/share/jython/Lib-cpython/sre.py", "_subn", false, false, funcTable, 16, null, null, 0, 1);
            c$17__split = Py.newCode(3, new String[] {"pattern", "string", "maxsplit", "append", "n", "m", "i", "g", "e", "extend", "c", "b", "s"}, "/usr/share/jython/Lib-cpython/sre.py", "_split", false, false, funcTable, 17, null, null, 0, 1);
            c$18__pickle = Py.newCode(1, new String[] {"p"}, "/usr/share/jython/Lib-cpython/sre.py", "_pickle", false, false, funcTable, 18, null, null, 0, 1);
            c$19___init__ = Py.newCode(2, new String[] {"self", "lexicon", "p", "SUBPATTERN", "phrase", "action", "BRANCH", "s"}, "/usr/share/jython/Lib-cpython/sre.py", "__init__", false, false, funcTable, 19, null, null, 0, 1);
            c$20_scan = Py.newCode(2, new String[] {"self", "string", "append", "m", "action", "j", "i", "match", "result"}, "/usr/share/jython/Lib-cpython/sre.py", "scan", false, false, funcTable, 20, null, null, 0, 1);
            c$21_Scanner = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/sre.py", "Scanner", false, false, funcTable, 21, null, null, 0, 0);
            c$22_main = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/sre.py", "main", false, false, funcTable, 22, null, null, 0, 0);
        }
        
        
        public PyCode getMain() {
            if (c$22_main == null) _PyInner.initConstants();
            return c$22_main;
        }
        
        public PyObject call_function(int index, PyFrame frame) {
            switch (index){
                case 0:
                return _PyInner.match$1(frame);
                case 1:
                return _PyInner.search$2(frame);
                case 2:
                return _PyInner.sub$3(frame);
                case 3:
                return _PyInner.subn$4(frame);
                case 4:
                return _PyInner.split$5(frame);
                case 5:
                return _PyInner.findall$6(frame);
                case 6:
                return _PyInner.compile$7(frame);
                case 7:
                return _PyInner.purge$8(frame);
                case 8:
                return _PyInner.template$9(frame);
                case 9:
                return _PyInner.escape$10(frame);
                case 10:
                return _PyInner._join$11(frame);
                case 11:
                return _PyInner._compile$12(frame);
                case 12:
                return _PyInner._compile_repl$13(frame);
                case 13:
                return _PyInner._expand$14(frame);
                case 14:
                return _PyInner._sub$15(frame);
                case 15:
                return _PyInner.filter$16(frame);
                case 16:
                return _PyInner._subn$17(frame);
                case 17:
                return _PyInner._split$18(frame);
                case 18:
                return _PyInner._pickle$19(frame);
                case 19:
                return _PyInner.__init__$20(frame);
                case 20:
                return _PyInner.scan$21(frame);
                case 21:
                return _PyInner.Scanner$22(frame);
                case 22:
                return _PyInner.main$23(frame);
                default:
                return null;
            }
        }
        
        private static PyObject match$1(PyFrame frame) {
            /* Try to apply the pattern at the start of the string, returning
                a match object, or None if no match was found. */
            return frame.getglobal("_compile").__call__(frame.getlocal(0), frame.getlocal(2)).invoke("match", frame.getlocal(1));
        }
        
        private static PyObject search$2(PyFrame frame) {
            /* Scan through string looking for a match to the pattern, returning
                a match object, or None if no match was found. */
            return frame.getglobal("_compile").__call__(frame.getlocal(0), frame.getlocal(2)).invoke("search", frame.getlocal(1));
        }
        
        private static PyObject sub$3(PyFrame frame) {
            /* Return the string obtained by replacing the leftmost
                non-overlapping occurrences of the pattern in string by the
                replacement repl */
            return frame.getglobal("_compile").__call__(frame.getlocal(0), i$25).invoke("sub", new PyObject[] {frame.getlocal(1), frame.getlocal(2), frame.getlocal(3)});
        }
        
        private static PyObject subn$4(PyFrame frame) {
            /* Return a 2-tuple containing (new_string, number).
                new_string is the string obtained by replacing the leftmost
                non-overlapping occurrences of the pattern in the source
                string by the replacement repl.  number is the number of
                substitutions that were made. */
            return frame.getglobal("_compile").__call__(frame.getlocal(0), i$25).invoke("subn", new PyObject[] {frame.getlocal(1), frame.getlocal(2), frame.getlocal(3)});
        }
        
        private static PyObject split$5(PyFrame frame) {
            /* Split the source string by the occurrences of the pattern,
                returning a list containing the resulting substrings. */
            return frame.getglobal("_compile").__call__(frame.getlocal(0), i$25).invoke("split", frame.getlocal(1), frame.getlocal(2));
        }
        
        private static PyObject findall$6(PyFrame frame) {
            /* Return a list of all non-overlapping matches in the string.
            
                If one or more groups are present in the pattern, return a
                list of groups; this will be a list of tuples if the pattern
                has more than one group.
            
                Empty matches are included in the result. */
            return frame.getglobal("_compile").__call__(frame.getlocal(0), i$25).invoke("findall", frame.getlocal(1), frame.getlocal(2));
        }
        
        private static PyObject compile$7(PyFrame frame) {
            /* Compile a regular expression pattern, returning a pattern object. */
            return frame.getglobal("_compile").__call__(frame.getlocal(0), frame.getlocal(1));
        }
        
        private static PyObject purge$8(PyFrame frame) {
            /* Clear the regular expression cache */
            frame.getglobal("_cache").invoke("clear");
            frame.getglobal("_cache_repl").invoke("clear");
            return Py.None;
        }
        
        private static PyObject template$9(PyFrame frame) {
            /* Compile a template pattern, returning a pattern object */
            return frame.getglobal("_compile").__call__(frame.getlocal(0), frame.getlocal(1)._or(frame.getglobal("T")));
        }
        
        private static PyObject escape$10(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyObject t$0$PyObject, t$1$PyObject, t$2$PyObject, t$3$PyObject, t$4$PyObject;
            
            // Code
            /* Escape all non-alphanumeric characters in pattern. */
            frame.setlocal(2, frame.getglobal("list").__call__(frame.getlocal(0)));
            t$0$int = 0;
            t$1$PyObject = frame.getglobal("range").__call__(frame.getglobal("len").__call__(frame.getlocal(0)));
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                frame.setlocal(1, t$0$PyObject);
                frame.setlocal(3, frame.getlocal(0).__getitem__(frame.getlocal(1)));
                if (((t$2$PyObject = ((t$3$PyObject = (s$35._le(t$4$PyObject = frame.getlocal(3)).__nonzero__() ? t$4$PyObject._le(s$36) : Py.Zero)).__nonzero__() ? t$3$PyObject : (s$37._le(t$4$PyObject = frame.getlocal(3)).__nonzero__() ? t$4$PyObject._le(s$38) : Py.Zero))).__nonzero__() ? t$2$PyObject : (s$39._le(t$3$PyObject = frame.getlocal(3)).__nonzero__() ? t$3$PyObject._le(s$40) : Py.Zero)).__not__().__nonzero__()) {
                    if (frame.getlocal(3)._eq(s$41).__nonzero__()) {
                        frame.getlocal(2).__setitem__(frame.getlocal(1), s$42);
                    }
                    else {
                        frame.getlocal(2).__setitem__(frame.getlocal(1), s$43._add(frame.getlocal(3)));
                    }
                }
            }
            return frame.getglobal("_join").__call__(frame.getlocal(2), frame.getlocal(0));
        }
        
        private static PyObject _join$11(PyFrame frame) {
            return frame.getglobal("string").__getattr__("join").__call__(frame.getlocal(0), frame.getlocal(1).__getslice__(null, i$25, null));
        }
        
        private static PyObject _compile$12(PyFrame frame) {
            // Temporary Variables
            PyObject[] t$0$PyObject__;
            PyException t$0$PyException;
            
            // Code
            frame.setlocal(1, frame.getglobal("_cache").invoke("get", frame.getlocal(0)));
            if (frame.getlocal(1)._isnot(frame.getglobal("None")).__nonzero__()) {
                return frame.getlocal(1);
            }
            t$0$PyObject__ = org.python.core.Py.unpackSequence(frame.getlocal(0), 2);
            frame.setlocal(3, t$0$PyObject__[0]);
            frame.setlocal(2, t$0$PyObject__[1]);
            if (frame.getglobal("type").__call__(frame.getlocal(3))._notin(frame.getglobal("sre_compile").__getattr__("STRING_TYPES")).__nonzero__()) {
                return frame.getlocal(3);
            }
            try {
                frame.setlocal(1, frame.getglobal("sre_compile").__getattr__("compile").__call__(frame.getlocal(3), frame.getlocal(2)));
            }
            catch (Throwable x$0) {
                t$0$PyException = Py.setException(x$0, frame);
                if (Py.matchException(t$0$PyException, frame.getglobal("error"))) {
                    frame.setlocal(4, t$0$PyException.value);
                    throw Py.makeException(frame.getglobal("error"), frame.getlocal(4));
                }
                else throw t$0$PyException;
            }
            if (frame.getglobal("len").__call__(frame.getglobal("_cache"))._ge(frame.getglobal("_MAXCACHE")).__nonzero__()) {
                frame.getglobal("_cache").invoke("clear");
            }
            frame.getglobal("_cache").__setitem__(frame.getlocal(0), frame.getlocal(1));
            return frame.getlocal(1);
        }
        
        private static PyObject _compile_repl$13(PyFrame frame) {
            // Temporary Variables
            PyObject[] t$0$PyObject__;
            PyException t$0$PyException;
            
            // Code
            frame.setlocal(1, frame.getglobal("_cache_repl").invoke("get", frame.getlocal(0)));
            if (frame.getlocal(1)._isnot(frame.getglobal("None")).__nonzero__()) {
                return frame.getlocal(1);
            }
            t$0$PyObject__ = org.python.core.Py.unpackSequence(frame.getlocal(0), 2);
            frame.setlocal(2, t$0$PyObject__[0]);
            frame.setlocal(3, t$0$PyObject__[1]);
            try {
                frame.setlocal(1, frame.getglobal("sre_parse").__getattr__("parse_template").__call__(frame.getlocal(2), frame.getlocal(3)));
            }
            catch (Throwable x$0) {
                t$0$PyException = Py.setException(x$0, frame);
                if (Py.matchException(t$0$PyException, frame.getglobal("error"))) {
                    frame.setlocal(4, t$0$PyException.value);
                    throw Py.makeException(frame.getglobal("error"), frame.getlocal(4));
                }
                else throw t$0$PyException;
            }
            if (frame.getglobal("len").__call__(frame.getglobal("_cache_repl"))._ge(frame.getglobal("_MAXCACHE")).__nonzero__()) {
                frame.getglobal("_cache_repl").invoke("clear");
            }
            frame.getglobal("_cache_repl").__setitem__(frame.getlocal(0), frame.getlocal(1));
            return frame.getlocal(1);
        }
        
        private static PyObject _expand$14(PyFrame frame) {
            frame.setlocal(2, frame.getglobal("sre_parse").__getattr__("parse_template").__call__(frame.getlocal(2), frame.getlocal(0)));
            return frame.getglobal("sre_parse").__getattr__("expand_template").__call__(frame.getlocal(2), frame.getlocal(1));
        }
        
        private static PyObject _sub$15(PyFrame frame) {
            return frame.getglobal("_subn").__call__(new PyObject[] {frame.getlocal(0), frame.getlocal(1), frame.getlocal(2), frame.getlocal(3)}).__getitem__(i$25);
        }
        
        private static PyObject filter$16(PyFrame frame) {
            return frame.getglobal("sre_parse").__getattr__("expand_template").__call__(frame.getlocal(1), frame.getlocal(0));
        }
        
        private static PyObject _subn$17(PyFrame frame) {
            // Temporary Variables
            PyObject[] t$0$PyObject__;
            PyObject t$0$PyObject;
            
            // Code
            if (frame.getglobal("callable").__call__(frame.getlocal(1)).__nonzero__()) {
                frame.setlocal(4, frame.getlocal(1));
            }
            else {
                frame.setlocal(1, frame.getglobal("_compile_repl").__call__(frame.getlocal(1), frame.getlocal(0)));
                frame.setlocal(4, new PyFunction(frame.f_globals, new PyObject[] {frame.getlocal(1)}, c$15_filter));
            }
            t$0$PyObject = i$25;
            frame.setlocal(6, t$0$PyObject);
            frame.setlocal(8, t$0$PyObject);
            frame.setlocal(12, new PyList(new PyObject[] {}));
            frame.setlocal(5, frame.getlocal(12).__getattr__("append"));
            frame.setlocal(10, frame.getlocal(0).invoke("scanner", frame.getlocal(2)));
            while (((t$0$PyObject = frame.getlocal(3).__not__()).__nonzero__() ? t$0$PyObject : frame.getlocal(6)._lt(frame.getlocal(3))).__nonzero__()) {
                frame.setlocal(7, frame.getlocal(10).invoke("search"));
                if (frame.getlocal(7).__not__().__nonzero__()) {
                    break;
                }
                t$0$PyObject__ = org.python.core.Py.unpackSequence(frame.getlocal(7).invoke("span"), 2);
                frame.setlocal(11, t$0$PyObject__[0]);
                frame.setlocal(9, t$0$PyObject__[1]);
                if (frame.getlocal(8)._lt(frame.getlocal(11)).__nonzero__()) {
                    frame.getlocal(5).__call__(frame.getlocal(2).__getslice__(frame.getlocal(8), frame.getlocal(11), null));
                }
                frame.getlocal(5).__call__(frame.getlocal(4).__call__(frame.getlocal(7)));
                frame.setlocal(8, frame.getlocal(9));
                frame.setlocal(6, frame.getlocal(6)._add(i$45));
            }
            frame.getlocal(5).__call__(frame.getlocal(2).__getslice__(frame.getlocal(8), null, null));
            return new PyTuple(new PyObject[] {frame.getglobal("_join").__call__(frame.getlocal(12), frame.getlocal(2).__getslice__(null, i$25, null)), frame.getlocal(6)});
        }
        
        private static PyObject _split$18(PyFrame frame) {
            // Temporary Variables
            PyObject[] t$0$PyObject__;
            PyObject t$0$PyObject;
            
            // Code
            t$0$PyObject = i$25;
            frame.setlocal(4, t$0$PyObject);
            frame.setlocal(6, t$0$PyObject);
            frame.setlocal(12, new PyList(new PyObject[] {}));
            frame.setlocal(3, frame.getlocal(12).__getattr__("append"));
            frame.setlocal(9, frame.getlocal(12).__getattr__("extend"));
            frame.setlocal(10, frame.getlocal(0).invoke("scanner", frame.getlocal(1)));
            frame.setlocal(7, frame.getlocal(0).__getattr__("groups"));
            while (((t$0$PyObject = frame.getlocal(2).__not__()).__nonzero__() ? t$0$PyObject : frame.getlocal(4)._lt(frame.getlocal(2))).__nonzero__()) {
                frame.setlocal(5, frame.getlocal(10).invoke("search"));
                if (frame.getlocal(5).__not__().__nonzero__()) {
                    break;
                }
                t$0$PyObject__ = org.python.core.Py.unpackSequence(frame.getlocal(5).invoke("span"), 2);
                frame.setlocal(11, t$0$PyObject__[0]);
                frame.setlocal(8, t$0$PyObject__[1]);
                if (frame.getlocal(11)._eq(frame.getlocal(8)).__nonzero__()) {
                    if (frame.getlocal(6)._ge(frame.getglobal("len").__call__(frame.getlocal(1))).__nonzero__()) {
                        break;
                    }
                    continue;
                }
                frame.getlocal(3).__call__(frame.getlocal(1).__getslice__(frame.getlocal(6), frame.getlocal(11), null));
                if (((t$0$PyObject = frame.getlocal(7)).__nonzero__() ? frame.getlocal(11)._ne(frame.getlocal(8)) : t$0$PyObject).__nonzero__()) {
                    frame.getlocal(9).__call__(frame.getglobal("list").__call__(frame.getlocal(5).invoke("groups")));
                }
                frame.setlocal(6, frame.getlocal(8));
                frame.setlocal(4, frame.getlocal(4)._add(i$45));
            }
            frame.getlocal(3).__call__(frame.getlocal(1).__getslice__(frame.getlocal(6), null, null));
            return frame.getlocal(12);
        }
        
        private static PyObject _pickle$19(PyFrame frame) {
            return new PyTuple(new PyObject[] {frame.getglobal("_compile"), new PyTuple(new PyObject[] {frame.getlocal(0).__getattr__("pattern"), frame.getlocal(0).__getattr__("flags")})});
        }
        
        private static PyObject __init__$20(PyFrame frame) {
            PyObject[] imp_accu;
            // Temporary Variables
            int t$0$int;
            PyObject[] t$0$PyObject__;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            imp_accu = org.python.core.imp.importFrom("sre_constants", new String[] {"BRANCH", "SUBPATTERN"}, frame);
            frame.setlocal(6, imp_accu[0]);
            frame.setlocal(3, imp_accu[1]);
            imp_accu = null;
            frame.getlocal(0).__setattr__("lexicon", frame.getlocal(1));
            frame.setlocal(2, new PyList(new PyObject[] {}));
            frame.setlocal(7, frame.getglobal("sre_parse").__getattr__("Pattern").__call__());
            t$0$int = 0;
            t$1$PyObject = frame.getlocal(1);
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                t$0$PyObject__ = org.python.core.Py.unpackSequence(t$0$PyObject, 2);
                frame.setlocal(4, t$0$PyObject__[0]);
                frame.setlocal(5, t$0$PyObject__[1]);
                frame.getlocal(2).invoke("append", frame.getglobal("sre_parse").__getattr__("SubPattern").__call__(frame.getlocal(7), new PyList(new PyObject[] {new PyTuple(new PyObject[] {frame.getlocal(3), new PyTuple(new PyObject[] {frame.getglobal("len").__call__(frame.getlocal(2)), frame.getglobal("sre_parse").__getattr__("parse").__call__(frame.getlocal(4))})})})));
            }
            frame.setlocal(2, frame.getglobal("sre_parse").__getattr__("SubPattern").__call__(frame.getlocal(7), new PyList(new PyObject[] {new PyTuple(new PyObject[] {frame.getlocal(6), new PyTuple(new PyObject[] {frame.getglobal("None"), frame.getlocal(2)})})})));
            frame.getlocal(7).__setattr__("groups", frame.getglobal("len").__call__(frame.getlocal(2)));
            frame.getlocal(0).__setattr__("scanner", frame.getglobal("sre_compile").__getattr__("compile").__call__(frame.getlocal(2)));
            return Py.None;
        }
        
        private static PyObject scan$21(PyFrame frame) {
            frame.setlocal(8, new PyList(new PyObject[] {}));
            frame.setlocal(2, frame.getlocal(8).__getattr__("append"));
            frame.setlocal(7, frame.getlocal(0).__getattr__("scanner").__getattr__("match"));
            frame.setlocal(6, i$25);
            while (i$45.__nonzero__()) {
                frame.setlocal(3, frame.getlocal(7).__call__(frame.getlocal(1), frame.getlocal(6)));
                if (frame.getlocal(3).__not__().__nonzero__()) {
                    break;
                }
                frame.setlocal(5, frame.getlocal(3).invoke("end"));
                if (frame.getlocal(6)._eq(frame.getlocal(5)).__nonzero__()) {
                    break;
                }
                frame.setlocal(4, frame.getlocal(0).__getattr__("lexicon").__getitem__(frame.getlocal(3).__getattr__("lastindex")).__getitem__(i$45));
                if (frame.getglobal("callable").__call__(frame.getlocal(4)).__nonzero__()) {
                    frame.getlocal(0).__setattr__("match", frame.getlocal(3));
                    frame.setlocal(4, frame.getlocal(4).__call__(frame.getlocal(0), frame.getlocal(3).invoke("group")));
                }
                if (frame.getlocal(4)._isnot(frame.getglobal("None")).__nonzero__()) {
                    frame.getlocal(2).__call__(frame.getlocal(4));
                }
                frame.setlocal(6, frame.getlocal(5));
            }
            return new PyTuple(new PyObject[] {frame.getlocal(8), frame.getlocal(1).__getslice__(frame.getlocal(6), null, null)});
        }
        
        private static PyObject Scanner$22(PyFrame frame) {
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {}, c$19___init__));
            frame.setlocal("scan", new PyFunction(frame.f_globals, new PyObject[] {}, c$20_scan));
            return frame.getf_locals();
        }
        
        private static PyObject main$23(PyFrame frame) {
            frame.setglobal("__file__", s$47);
            
            // Temporary Variables
            PyObject t$0$PyObject;
            
            // Code
            frame.setlocal("sre_compile", org.python.core.imp.importOne("sre_compile", frame));
            frame.setlocal("sre_parse", org.python.core.imp.importOne("sre_parse", frame));
            frame.setlocal("__all__", new PyList(new PyObject[] {s$0, s$1, s$2, s$3, s$4, s$5, s$6, s$7, s$8, s$9, s$10, s$11, s$12, s$13, s$14, s$15, s$16, s$17, s$18, s$19, s$20, s$21, s$22}));
            frame.setlocal("__version__", s$23);
            frame.setlocal("string", org.python.core.imp.importOne("string", frame));
            t$0$PyObject = frame.getname("sre_compile").__getattr__("SRE_FLAG_IGNORECASE");
            frame.setlocal("I", t$0$PyObject);
            frame.setlocal("IGNORECASE", t$0$PyObject);
            t$0$PyObject = frame.getname("sre_compile").__getattr__("SRE_FLAG_LOCALE");
            frame.setlocal("L", t$0$PyObject);
            frame.setlocal("LOCALE", t$0$PyObject);
            t$0$PyObject = frame.getname("sre_compile").__getattr__("SRE_FLAG_UNICODE");
            frame.setlocal("U", t$0$PyObject);
            frame.setlocal("UNICODE", t$0$PyObject);
            t$0$PyObject = frame.getname("sre_compile").__getattr__("SRE_FLAG_MULTILINE");
            frame.setlocal("M", t$0$PyObject);
            frame.setlocal("MULTILINE", t$0$PyObject);
            t$0$PyObject = frame.getname("sre_compile").__getattr__("SRE_FLAG_DOTALL");
            frame.setlocal("S", t$0$PyObject);
            frame.setlocal("DOTALL", t$0$PyObject);
            t$0$PyObject = frame.getname("sre_compile").__getattr__("SRE_FLAG_VERBOSE");
            frame.setlocal("X", t$0$PyObject);
            frame.setlocal("VERBOSE", t$0$PyObject);
            t$0$PyObject = frame.getname("sre_compile").__getattr__("SRE_FLAG_TEMPLATE");
            frame.setlocal("T", t$0$PyObject);
            frame.setlocal("TEMPLATE", t$0$PyObject);
            frame.setlocal("DEBUG", frame.getname("sre_compile").__getattr__("SRE_FLAG_DEBUG"));
            frame.setlocal("error", frame.getname("sre_compile").__getattr__("error"));
            frame.setlocal("match", new PyFunction(frame.f_globals, new PyObject[] {i$25}, c$0_match));
            frame.setlocal("search", new PyFunction(frame.f_globals, new PyObject[] {i$25}, c$1_search));
            frame.setlocal("sub", new PyFunction(frame.f_globals, new PyObject[] {i$25}, c$2_sub));
            frame.setlocal("subn", new PyFunction(frame.f_globals, new PyObject[] {i$25}, c$3_subn));
            frame.setlocal("split", new PyFunction(frame.f_globals, new PyObject[] {i$25}, c$4_split));
            frame.setlocal("findall", new PyFunction(frame.f_globals, new PyObject[] {i$25}, c$5_findall));
            frame.setlocal("compile", new PyFunction(frame.f_globals, new PyObject[] {i$25}, c$6_compile));
            frame.setlocal("purge", new PyFunction(frame.f_globals, new PyObject[] {}, c$7_purge));
            frame.setlocal("template", new PyFunction(frame.f_globals, new PyObject[] {i$25}, c$8_template));
            frame.setlocal("escape", new PyFunction(frame.f_globals, new PyObject[] {}, c$9_escape));
            frame.setlocal("_cache", new PyDictionary(new PyObject[] {}));
            frame.setlocal("_cache_repl", new PyDictionary(new PyObject[] {}));
            frame.setlocal("_MAXCACHE", i$44);
            frame.setlocal("_join", new PyFunction(frame.f_globals, new PyObject[] {}, c$10__join));
            frame.setlocal("_compile", new PyFunction(frame.f_globals, new PyObject[] {}, c$11__compile));
            frame.setlocal("_compile_repl", new PyFunction(frame.f_globals, new PyObject[] {}, c$12__compile_repl));
            frame.setlocal("_expand", new PyFunction(frame.f_globals, new PyObject[] {}, c$13__expand));
            frame.setlocal("_sub", new PyFunction(frame.f_globals, new PyObject[] {i$25}, c$14__sub));
            frame.setlocal("_subn", new PyFunction(frame.f_globals, new PyObject[] {i$25}, c$16__subn));
            frame.setlocal("_split", new PyFunction(frame.f_globals, new PyObject[] {i$25}, c$17__split));
            frame.setlocal("copy_reg", org.python.core.imp.importOne("copy_reg", frame));
            frame.setlocal("_pickle", new PyFunction(frame.f_globals, new PyObject[] {}, c$18__pickle));
            frame.getname("copy_reg").__getattr__("pickle").__call__(frame.getname("type").__call__(frame.getname("_compile").__call__(s$46, i$25)), frame.getname("_pickle"), frame.getname("_compile"));
            frame.setlocal("Scanner", Py.makeClass("Scanner", new PyObject[] {}, c$21_Scanner, null));
            return Py.None;
        }
        
    }
    public static void moduleDictInit(PyObject dict) {
        dict.__setitem__("__name__", new PyString("sre"));
        Py.runCode(new _PyInner().getMain(), dict, dict);
    }
    
    public static void main(String[] args) throws java.lang.Exception {
        String[] newargs = new String[args.length+1];
        newargs[0] = "sre";
        System.arraycopy(args, 0, newargs, 1, args.length);
        Py.runMain(sre._PyInner.class, newargs, sre.jpy$packages, sre.jpy$mainProperties, "", new String[] {"string", "random", "util", "traceback", "sre_compile", "atexit", "sre", "sre_constants", "StringIO", "javaos", "socket", "yapm", "calendar", "repr", "copy_reg", "SocketServer", "server", "re", "linecache", "javapath", "UserDict", "copy", "threading", "stat", "PathVFS", "sre_parse"});
    }
    
}
