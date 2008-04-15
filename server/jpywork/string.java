import org.python.core.*;

public class string extends java.lang.Object {
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
        private static PyObject i$9;
        private static PyObject s$10;
        private static PyObject s$11;
        private static PyObject s$12;
        private static PyObject s$13;
        private static PyObject s$14;
        private static PyObject s$15;
        private static PyObject s$16;
        private static PyObject i$17;
        private static PyObject s$18;
        private static PyObject s$19;
        private static PyObject s$20;
        private static PyObject s$21;
        private static PyObject s$22;
        private static PyObject s$23;
        private static PyObject s$24;
        private static PyObject s$25;
        private static PyObject s$26;
        private static PyObject s$27;
        private static PyObject i$28;
        private static PyObject s$29;
        private static PyObject s$30;
        private static PyObject s$31;
        private static PyObject s$32;
        private static PyObject s$33;
        private static PyObject i$34;
        private static PyObject s$35;
        private static PyObject s$36;
        private static PyObject s$37;
        private static PyObject s$38;
        private static PyObject s$39;
        private static PyObject s$40;
        private static PyObject s$41;
        private static PyObject i$42;
        private static PyObject s$43;
        private static PyObject s$44;
        private static PyObject s$45;
        private static PyObject s$46;
        private static PyObject s$47;
        private static PyObject s$48;
        private static PyObject s$49;
        private static PyFunctionTable funcTable;
        private static PyCode c$0_lower;
        private static PyCode c$1_upper;
        private static PyCode c$2_swapcase;
        private static PyCode c$3_strip;
        private static PyCode c$4_lstrip;
        private static PyCode c$5_rstrip;
        private static PyCode c$6_split;
        private static PyCode c$7_join;
        private static PyCode c$8_index;
        private static PyCode c$9_rindex;
        private static PyCode c$10_count;
        private static PyCode c$11_find;
        private static PyCode c$12_rfind;
        private static PyCode c$13_atof;
        private static PyCode c$14_atoi;
        private static PyCode c$15_atol;
        private static PyCode c$16_ljust;
        private static PyCode c$17_rjust;
        private static PyCode c$18_center;
        private static PyCode c$19_zfill;
        private static PyCode c$20_expandtabs;
        private static PyCode c$21_translate;
        private static PyCode c$22_capitalize;
        private static PyCode c$23_capwords;
        private static PyCode c$24_maketrans;
        private static PyCode c$25_replace;
        private static PyCode c$26_main;
        private static void initConstants() {
            s$0 = Py.newString("Common string manipulations.\012\012Public module variables:\012\012whitespace -- a string containing all characters considered whitespace\012lowercase -- a string containing all characters considered lowercase letters\012uppercase -- a string containing all characters considered uppercase letters\012letters -- a string containing all characters considered letters\012digits -- a string containing all characters considered decimal digits\012hexdigits -- a string containing all characters considered hexadecimal digits\012octdigits -- a string containing all characters considered octal digits\012\012");
            s$1 = Py.newString(" \011\012\015\013\014");
            s$2 = Py.newString("abcdefghijklmnopqrstuvwxyz");
            s$3 = Py.newString("ABCDEFGHIJKLMNOPQRSTUVWXYZ");
            s$4 = Py.newString("0123456789");
            s$5 = Py.newString("abcdef");
            s$6 = Py.newString("ABCDEF");
            s$7 = Py.newString("01234567");
            s$8 = Py.newString("");
            i$9 = Py.newInteger(256);
            s$10 = Py.newString("lower(s) -> string\012\012    Return a copy of the string s converted to lowercase.\012\012    ");
            s$11 = Py.newString("upper(s) -> string\012\012    Return a copy of the string s converted to uppercase.\012\012    ");
            s$12 = Py.newString("swapcase(s) -> string\012\012    Return a copy of the string s with upper case characters\012    converted to lowercase and vice versa.\012\012    ");
            s$13 = Py.newString("strip(s) -> string\012\012    Return a copy of the string s with leading and trailing\012    whitespace removed.\012\012    ");
            s$14 = Py.newString("lstrip(s) -> string\012\012    Return a copy of the string s with leading whitespace removed.\012\012    ");
            s$15 = Py.newString("rstrip(s) -> string\012\012    Return a copy of the string s with trailing whitespace\012    removed.\012\012    ");
            s$16 = Py.newString("split(str [,sep [,maxsplit]]) -> list of strings\012\012    Return a list of the words in the string s, using sep as the\012    delimiter string.  If maxsplit is nonzero, splits into at most\012    maxsplit words If sep is not specified, any whitespace string\012    is a separator.  Maxsplit defaults to -1.\012\012    (split and splitfields are synonymous)\012\012    ");
            i$17 = Py.newInteger(1);
            s$18 = Py.newString("join(list [,sep]) -> string\012\012    Return a string composed of the words in list, with\012    intervening occurences of sep.  The default separator is a\012    single space.\012\012    (joinfields and join are synonymous)\012\012    ");
            s$19 = Py.newString(" ");
            s$20 = Py.newString("index(s, sub [,start [,end]]) -> int\012\012    Like find but raises ValueError when the substring is not found.\012\012    ");
            s$21 = Py.newString("rindex(s, sub [,start [,end]]) -> int\012\012    Like rfind but raises ValueError when the substring is not found.\012\012    ");
            s$22 = Py.newString("count(s, sub[, start[,end]]) -> int\012\012    Return the number of occurrences of substring sub in string\012    s[start:end].  Optional arguments start and end are\012    interpreted as in slice notation.\012\012    ");
            s$23 = Py.newString("find(s, sub [,start [,end]]) -> in\012\012    Return the lowest index in s where substring sub is found,\012    such that sub is contained within s[start,end].  Optional\012    arguments start and end are interpreted as in slice notation.\012\012    Return -1 on failure.\012\012    ");
            s$24 = Py.newString("rfind(s, sub [,start [,end]]) -> int\012\012    Return the highest index in s where substring sub is found,\012    such that sub is contained within s[start,end].  Optional\012    arguments start and end are interpreted as in slice notation.\012\012    Return -1 on failure.\012\012    ");
            s$25 = Py.newString("atof(s) -> float\012\012    Return the floating point number represented by the string s.\012\012    ");
            s$26 = Py.newString("argument 1: expected string, %s found");
            s$27 = Py.newString("atoi(s [,base]) -> int\012\012    Return the integer represented by the string s in the given\012    base, which defaults to 10.  The string s must consist of one\012    or more digits, possibly preceded by a sign.  If base is 0, it\012    is chosen from the leading characters of s, 0 for octal, 0x or\012    0X for hexadecimal.  If base is 16, a preceding 0x or 0X is\012    accepted.\012\012    ");
            i$28 = Py.newInteger(0);
            s$29 = Py.newString("function requires at least 1 argument: %d given");
            s$30 = Py.newString("atol(s [,base]) -> long\012\012    Return the long integer represented by the string s in the\012    given base, which defaults to 10.  The string s must consist\012    of one or more digits, possibly preceded by a sign.  If base\012    is 0, it is chosen from the leading characters of s, 0 for\012    octal, 0x or 0X for hexadecimal.  If base is 16, a preceding\012    0x or 0X is accepted.  A trailing L or l is not accepted,\012    unless base is 0.\012\012    ");
            s$31 = Py.newString("ljust(s, width) -> string\012\012    Return a left-justified version of s, in a field of the\012    specified width, padded with spaces as needed.  The string is\012    never truncated.\012\012    ");
            s$32 = Py.newString("rjust(s, width) -> string\012\012    Return a right-justified version of s, in a field of the\012    specified width, padded with spaces as needed.  The string is\012    never truncated.\012\012    ");
            s$33 = Py.newString("center(s, width) -> string\012\012    Return a center version of s, in a field of the specified\012    width. padded with spaces as needed.  The string is never\012    truncated.\012\012    ");
            i$34 = Py.newInteger(2);
            s$35 = Py.newString("zfill(x, width) -> string\012\012    Pad a numeric string x with zeros on the left, to fill a field\012    of the specified width.  The string x is never truncated.\012\012    ");
            s$36 = Py.newString("-");
            s$37 = Py.newString("+");
            s$38 = Py.newString("0");
            s$39 = Py.newString("expandtabs(s [,tabsize]) -> string\012\012    Return a copy of the string s with all tab characters replaced\012    by the appropriate number of spaces, depending on the current\012    column, and the tabsize (default 8).\012\012    ");
            s$40 = Py.newString("\011");
            s$41 = Py.newString("\012");
            i$42 = Py.newInteger(8);
            s$43 = Py.newString("translate(s,table [,deletechars]) -> string\012\012    Return a copy of the string s, where all characters occurring\012    in the optional argument deletechars are removed, and the\012    remaining characters have been mapped through the given\012    translation table, which must be a string of length 256.\012\012    ");
            s$44 = Py.newString("capitalize(s) -> string\012\012    Return a copy of the string s with only its first character\012    capitalized.\012\012    ");
            s$45 = Py.newString("capwords(s, [sep]) -> string\012\012    Split the argument into words using split, capitalize each\012    word using capitalize, and join the capitalized words using\012    join. Note that this replaces runs of whitespace characters by\012    a single space.\012\012    ");
            s$46 = Py.newString("maketrans(frm, to) -> string\012\012    Return a translation table (a string of 256 bytes long)\012    suitable for use in string.translate.  The strings frm and to\012    must be of the same length.\012\012    ");
            s$47 = Py.newString("maketrans arguments must have same length");
            s$48 = Py.newString("replace (str, old, new[, maxsplit]) -> string\012\012    Return a copy of string str with all occurrences of substring\012    old replaced by new. If the optional argument maxsplit is\012    given, only the first maxsplit occurrences are replaced.\012\012    ");
            s$49 = Py.newString("/usr/share/jython/Lib/string.py");
            funcTable = new _PyInner();
            c$0_lower = Py.newCode(1, new String[] {"s"}, "/usr/share/jython/Lib/string.py", "lower", false, false, funcTable, 0, null, null, 0, 1);
            c$1_upper = Py.newCode(1, new String[] {"s"}, "/usr/share/jython/Lib/string.py", "upper", false, false, funcTable, 1, null, null, 0, 1);
            c$2_swapcase = Py.newCode(1, new String[] {"s"}, "/usr/share/jython/Lib/string.py", "swapcase", false, false, funcTable, 2, null, null, 0, 1);
            c$3_strip = Py.newCode(1, new String[] {"s"}, "/usr/share/jython/Lib/string.py", "strip", false, false, funcTable, 3, null, null, 0, 1);
            c$4_lstrip = Py.newCode(1, new String[] {"s"}, "/usr/share/jython/Lib/string.py", "lstrip", false, false, funcTable, 4, null, null, 0, 1);
            c$5_rstrip = Py.newCode(1, new String[] {"s"}, "/usr/share/jython/Lib/string.py", "rstrip", false, false, funcTable, 5, null, null, 0, 1);
            c$6_split = Py.newCode(3, new String[] {"s", "sep", "maxsplit"}, "/usr/share/jython/Lib/string.py", "split", false, false, funcTable, 6, null, null, 0, 1);
            c$7_join = Py.newCode(2, new String[] {"words", "sep"}, "/usr/share/jython/Lib/string.py", "join", false, false, funcTable, 7, null, null, 0, 1);
            c$8_index = Py.newCode(2, new String[] {"s", "args"}, "/usr/share/jython/Lib/string.py", "index", true, false, funcTable, 8, null, null, 0, 1);
            c$9_rindex = Py.newCode(2, new String[] {"s", "args"}, "/usr/share/jython/Lib/string.py", "rindex", true, false, funcTable, 9, null, null, 0, 1);
            c$10_count = Py.newCode(2, new String[] {"s", "args"}, "/usr/share/jython/Lib/string.py", "count", true, false, funcTable, 10, null, null, 0, 1);
            c$11_find = Py.newCode(2, new String[] {"s", "args"}, "/usr/share/jython/Lib/string.py", "find", true, false, funcTable, 11, null, null, 0, 1);
            c$12_rfind = Py.newCode(2, new String[] {"s", "args"}, "/usr/share/jython/Lib/string.py", "rfind", true, false, funcTable, 12, null, null, 0, 1);
            c$13_atof = Py.newCode(1, new String[] {"s"}, "/usr/share/jython/Lib/string.py", "atof", false, false, funcTable, 13, null, null, 0, 1);
            c$14_atoi = Py.newCode(1, new String[] {"args", "s"}, "/usr/share/jython/Lib/string.py", "atoi", true, false, funcTable, 14, null, null, 0, 1);
            c$15_atol = Py.newCode(1, new String[] {"args", "s"}, "/usr/share/jython/Lib/string.py", "atol", true, false, funcTable, 15, null, null, 0, 1);
            c$16_ljust = Py.newCode(2, new String[] {"s", "width", "n"}, "/usr/share/jython/Lib/string.py", "ljust", false, false, funcTable, 16, null, null, 0, 1);
            c$17_rjust = Py.newCode(2, new String[] {"s", "width", "n"}, "/usr/share/jython/Lib/string.py", "rjust", false, false, funcTable, 17, null, null, 0, 1);
            c$18_center = Py.newCode(2, new String[] {"s", "width", "half", "n"}, "/usr/share/jython/Lib/string.py", "center", false, false, funcTable, 18, null, null, 0, 1);
            c$19_zfill = Py.newCode(2, new String[] {"x", "width", "sign", "s", "n"}, "/usr/share/jython/Lib/string.py", "zfill", false, false, funcTable, 19, null, null, 0, 1);
            c$20_expandtabs = Py.newCode(2, new String[] {"s", "tabsize", "line", "res", "c"}, "/usr/share/jython/Lib/string.py", "expandtabs", false, false, funcTable, 20, null, null, 0, 1);
            c$21_translate = Py.newCode(3, new String[] {"s", "table", "deletions"}, "/usr/share/jython/Lib/string.py", "translate", false, false, funcTable, 21, null, null, 0, 1);
            c$22_capitalize = Py.newCode(1, new String[] {"s"}, "/usr/share/jython/Lib/string.py", "capitalize", false, false, funcTable, 22, null, null, 0, 1);
            c$23_capwords = Py.newCode(2, new String[] {"s", "sep"}, "/usr/share/jython/Lib/string.py", "capwords", false, false, funcTable, 23, null, null, 0, 1);
            c$24_maketrans = Py.newCode(2, new String[] {"fromstr", "tostr", "i", "L"}, "/usr/share/jython/Lib/string.py", "maketrans", false, false, funcTable, 24, null, null, 0, 1);
            c$25_replace = Py.newCode(4, new String[] {"s", "old", "new", "maxsplit"}, "/usr/share/jython/Lib/string.py", "replace", false, false, funcTable, 25, null, null, 0, 1);
            c$26_main = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib/string.py", "main", false, false, funcTable, 26, null, null, 0, 0);
        }
        
        
        public PyCode getMain() {
            if (c$26_main == null) _PyInner.initConstants();
            return c$26_main;
        }
        
        public PyObject call_function(int index, PyFrame frame) {
            switch (index){
                case 0:
                return _PyInner.lower$1(frame);
                case 1:
                return _PyInner.upper$2(frame);
                case 2:
                return _PyInner.swapcase$3(frame);
                case 3:
                return _PyInner.strip$4(frame);
                case 4:
                return _PyInner.lstrip$5(frame);
                case 5:
                return _PyInner.rstrip$6(frame);
                case 6:
                return _PyInner.split$7(frame);
                case 7:
                return _PyInner.join$8(frame);
                case 8:
                return _PyInner.index$9(frame);
                case 9:
                return _PyInner.rindex$10(frame);
                case 10:
                return _PyInner.count$11(frame);
                case 11:
                return _PyInner.find$12(frame);
                case 12:
                return _PyInner.rfind$13(frame);
                case 13:
                return _PyInner.atof$14(frame);
                case 14:
                return _PyInner.atoi$15(frame);
                case 15:
                return _PyInner.atol$16(frame);
                case 16:
                return _PyInner.ljust$17(frame);
                case 17:
                return _PyInner.rjust$18(frame);
                case 18:
                return _PyInner.center$19(frame);
                case 19:
                return _PyInner.zfill$20(frame);
                case 20:
                return _PyInner.expandtabs$21(frame);
                case 21:
                return _PyInner.translate$22(frame);
                case 22:
                return _PyInner.capitalize$23(frame);
                case 23:
                return _PyInner.capwords$24(frame);
                case 24:
                return _PyInner.maketrans$25(frame);
                case 25:
                return _PyInner.replace$26(frame);
                case 26:
                return _PyInner.main$27(frame);
                default:
                return null;
            }
        }
        
        private static PyObject lower$1(PyFrame frame) {
            /* lower(s) -> string
            
                Return a copy of the string s converted to lowercase.
            
                 */
            return frame.getlocal(0).invoke("lower");
        }
        
        private static PyObject upper$2(PyFrame frame) {
            /* upper(s) -> string
            
                Return a copy of the string s converted to uppercase.
            
                 */
            return frame.getlocal(0).invoke("upper");
        }
        
        private static PyObject swapcase$3(PyFrame frame) {
            /* swapcase(s) -> string
            
                Return a copy of the string s with upper case characters
                converted to lowercase and vice versa.
            
                 */
            return frame.getlocal(0).invoke("swapcase");
        }
        
        private static PyObject strip$4(PyFrame frame) {
            /* strip(s) -> string
            
                Return a copy of the string s with leading and trailing
                whitespace removed.
            
                 */
            return frame.getlocal(0).invoke("strip");
        }
        
        private static PyObject lstrip$5(PyFrame frame) {
            /* lstrip(s) -> string
            
                Return a copy of the string s with leading whitespace removed.
            
                 */
            return frame.getlocal(0).invoke("lstrip");
        }
        
        private static PyObject rstrip$6(PyFrame frame) {
            /* rstrip(s) -> string
            
                Return a copy of the string s with trailing whitespace
                removed.
            
                 */
            return frame.getlocal(0).invoke("rstrip");
        }
        
        private static PyObject split$7(PyFrame frame) {
            /* split(str [,sep [,maxsplit]]) -> list of strings
            
                Return a list of the words in the string s, using sep as the
                delimiter string.  If maxsplit is nonzero, splits into at most
                maxsplit words If sep is not specified, any whitespace string
                is a separator.  Maxsplit defaults to -1.
            
                (split and splitfields are synonymous)
            
                 */
            return frame.getlocal(0).invoke("split", frame.getlocal(1), frame.getlocal(2));
        }
        
        private static PyObject join$8(PyFrame frame) {
            /* join(list [,sep]) -> string
            
                Return a string composed of the words in list, with
                intervening occurences of sep.  The default separator is a
                single space.
            
                (joinfields and join are synonymous)
            
                 */
            return frame.getlocal(1).invoke("join", frame.getlocal(0));
        }
        
        private static PyObject index$9(PyFrame frame) {
            /* index(s, sub [,start [,end]]) -> int
            
                Like find but raises ValueError when the substring is not found.
            
                 */
            return frame.getglobal("_apply").__call__(frame.getlocal(0).__getattr__("index"), frame.getlocal(1));
        }
        
        private static PyObject rindex$10(PyFrame frame) {
            /* rindex(s, sub [,start [,end]]) -> int
            
                Like rfind but raises ValueError when the substring is not found.
            
                 */
            return frame.getglobal("_apply").__call__(frame.getlocal(0).__getattr__("rindex"), frame.getlocal(1));
        }
        
        private static PyObject count$11(PyFrame frame) {
            /* count(s, sub[, start[,end]]) -> int
            
                Return the number of occurrences of substring sub in string
                s[start:end].  Optional arguments start and end are
                interpreted as in slice notation.
            
                 */
            return frame.getglobal("_apply").__call__(frame.getlocal(0).__getattr__("count"), frame.getlocal(1));
        }
        
        private static PyObject find$12(PyFrame frame) {
            /* find(s, sub [,start [,end]]) -> in
            
                Return the lowest index in s where substring sub is found,
                such that sub is contained within s[start,end].  Optional
                arguments start and end are interpreted as in slice notation.
            
                Return -1 on failure.
            
                 */
            return frame.getglobal("_apply").__call__(frame.getlocal(0).__getattr__("find"), frame.getlocal(1));
        }
        
        private static PyObject rfind$13(PyFrame frame) {
            /* rfind(s, sub [,start [,end]]) -> int
            
                Return the highest index in s where substring sub is found,
                such that sub is contained within s[start,end].  Optional
                arguments start and end are interpreted as in slice notation.
            
                Return -1 on failure.
            
                 */
            return frame.getglobal("_apply").__call__(frame.getlocal(0).__getattr__("rfind"), frame.getlocal(1));
        }
        
        private static PyObject atof$14(PyFrame frame) {
            /* atof(s) -> float
            
                Return the floating point number represented by the string s.
            
                 */
            if (frame.getglobal("type").__call__(frame.getlocal(0))._eq(frame.getglobal("_StringType")).__nonzero__()) {
                return frame.getglobal("_float").__call__(frame.getlocal(0));
            }
            else {
                throw Py.makeException(frame.getglobal("TypeError").__call__(s$26._mod(frame.getglobal("type").__call__(frame.getlocal(0)).__getattr__("__name__"))));
            }
        }
        
        private static PyObject atoi$15(PyFrame frame) {
            // Temporary Variables
            PyException t$0$PyException;
            
            // Code
            /* atoi(s [,base]) -> int
            
                Return the integer represented by the string s in the given
                base, which defaults to 10.  The string s must consist of one
                or more digits, possibly preceded by a sign.  If base is 0, it
                is chosen from the leading characters of s, 0 for octal, 0x or
                0X for hexadecimal.  If base is 16, a preceding 0x or 0X is
                accepted.
            
                 */
            try {
                frame.setlocal(1, frame.getlocal(0).__getitem__(i$28));
            }
            catch (Throwable x$0) {
                t$0$PyException = Py.setException(x$0, frame);
                if (Py.matchException(t$0$PyException, frame.getglobal("IndexError"))) {
                    throw Py.makeException(frame.getglobal("TypeError").__call__(s$29._mod(frame.getglobal("len").__call__(frame.getlocal(0)))));
                }
                else throw t$0$PyException;
            }
            if (frame.getglobal("type").__call__(frame.getlocal(1))._eq(frame.getglobal("_StringType")).__nonzero__()) {
                return frame.getglobal("_apply").__call__(frame.getglobal("_int"), frame.getlocal(0));
            }
            else {
                throw Py.makeException(frame.getglobal("TypeError").__call__(s$26._mod(frame.getglobal("type").__call__(frame.getlocal(1)).__getattr__("__name__"))));
            }
        }
        
        private static PyObject atol$16(PyFrame frame) {
            // Temporary Variables
            PyException t$0$PyException;
            
            // Code
            /* atol(s [,base]) -> long
            
                Return the long integer represented by the string s in the
                given base, which defaults to 10.  The string s must consist
                of one or more digits, possibly preceded by a sign.  If base
                is 0, it is chosen from the leading characters of s, 0 for
                octal, 0x or 0X for hexadecimal.  If base is 16, a preceding
                0x or 0X is accepted.  A trailing L or l is not accepted,
                unless base is 0.
            
                 */
            try {
                frame.setlocal(1, frame.getlocal(0).__getitem__(i$28));
            }
            catch (Throwable x$0) {
                t$0$PyException = Py.setException(x$0, frame);
                if (Py.matchException(t$0$PyException, frame.getglobal("IndexError"))) {
                    throw Py.makeException(frame.getglobal("TypeError").__call__(s$29._mod(frame.getglobal("len").__call__(frame.getlocal(0)))));
                }
                else throw t$0$PyException;
            }
            if (frame.getglobal("type").__call__(frame.getlocal(1))._eq(frame.getglobal("_StringType")).__nonzero__()) {
                return frame.getglobal("_apply").__call__(frame.getglobal("_long"), frame.getlocal(0));
            }
            else {
                throw Py.makeException(frame.getglobal("TypeError").__call__(s$26._mod(frame.getglobal("type").__call__(frame.getlocal(1)).__getattr__("__name__"))));
            }
        }
        
        private static PyObject ljust$17(PyFrame frame) {
            /* ljust(s, width) -> string
            
                Return a left-justified version of s, in a field of the
                specified width, padded with spaces as needed.  The string is
                never truncated.
            
                 */
            frame.setlocal(2, frame.getlocal(1)._sub(frame.getglobal("len").__call__(frame.getlocal(0))));
            if (frame.getlocal(2)._le(i$28).__nonzero__()) {
                return frame.getlocal(0);
            }
            return frame.getlocal(0)._add(s$19._mul(frame.getlocal(2)));
        }
        
        private static PyObject rjust$18(PyFrame frame) {
            /* rjust(s, width) -> string
            
                Return a right-justified version of s, in a field of the
                specified width, padded with spaces as needed.  The string is
                never truncated.
            
                 */
            frame.setlocal(2, frame.getlocal(1)._sub(frame.getglobal("len").__call__(frame.getlocal(0))));
            if (frame.getlocal(2)._le(i$28).__nonzero__()) {
                return frame.getlocal(0);
            }
            return s$19._mul(frame.getlocal(2))._add(frame.getlocal(0));
        }
        
        private static PyObject center$19(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject;
            
            // Code
            /* center(s, width) -> string
            
                Return a center version of s, in a field of the specified
                width. padded with spaces as needed.  The string is never
                truncated.
            
                 */
            frame.setlocal(3, frame.getlocal(1)._sub(frame.getglobal("len").__call__(frame.getlocal(0))));
            if (frame.getlocal(3)._le(i$28).__nonzero__()) {
                return frame.getlocal(0);
            }
            frame.setlocal(2, frame.getlocal(3)._div(i$34));
            if (((t$0$PyObject = frame.getlocal(3)._mod(i$34)).__nonzero__() ? frame.getlocal(1)._mod(i$34) : t$0$PyObject).__nonzero__()) {
                frame.setlocal(2, frame.getlocal(2)._add(i$17));
            }
            return s$19._mul(frame.getlocal(2))._add(frame.getlocal(0))._add(s$19._mul(frame.getlocal(3)._sub(frame.getlocal(2))));
        }
        
        private static PyObject zfill$20(PyFrame frame) {
            // Temporary Variables
            PyObject[] t$0$PyObject__;
            
            // Code
            /* zfill(x, width) -> string
            
                Pad a numeric string x with zeros on the left, to fill a field
                of the specified width.  The string x is never truncated.
            
                 */
            if (frame.getglobal("type").__call__(frame.getlocal(0))._eq(frame.getglobal("type").__call__(s$8)).__nonzero__()) {
                frame.setlocal(3, frame.getlocal(0));
            }
            else {
                frame.setlocal(3, frame.getlocal(0).__repr__());
            }
            frame.setlocal(4, frame.getglobal("len").__call__(frame.getlocal(3)));
            if (frame.getlocal(4)._ge(frame.getlocal(1)).__nonzero__()) {
                return frame.getlocal(3);
            }
            frame.setlocal(2, s$8);
            if (frame.getlocal(3).__getitem__(i$28)._in(new PyTuple(new PyObject[] {s$36, s$37})).__nonzero__()) {
                t$0$PyObject__ = org.python.core.Py.unpackSequence(new PyTuple(new PyObject[] {frame.getlocal(3).__getitem__(i$28), frame.getlocal(3).__getslice__(i$17, null, null)}), 2);
                frame.setlocal(2, t$0$PyObject__[0]);
                frame.setlocal(3, t$0$PyObject__[1]);
            }
            return frame.getlocal(2)._add(s$38._mul(frame.getlocal(1)._sub(frame.getlocal(4))))._add(frame.getlocal(3));
        }
        
        private static PyObject expandtabs$21(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            /* expandtabs(s [,tabsize]) -> string
            
                Return a copy of the string s with all tab characters replaced
                by the appropriate number of spaces, depending on the current
                column, and the tabsize (default 8).
            
                 */
            t$0$PyObject = s$8;
            frame.setlocal(3, t$0$PyObject);
            frame.setlocal(2, t$0$PyObject);
            t$0$int = 0;
            t$1$PyObject = frame.getlocal(0);
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                frame.setlocal(4, t$0$PyObject);
                if (frame.getlocal(4)._eq(s$40).__nonzero__()) {
                    frame.setlocal(4, s$19._mul(frame.getlocal(1)._sub(frame.getglobal("len").__call__(frame.getlocal(2))._mod(frame.getlocal(1)))));
                }
                frame.setlocal(2, frame.getlocal(2)._add(frame.getlocal(4)));
                if (frame.getlocal(4)._eq(s$41).__nonzero__()) {
                    frame.setlocal(3, frame.getlocal(3)._add(frame.getlocal(2)));
                    frame.setlocal(2, s$8);
                }
            }
            return frame.getlocal(3)._add(frame.getlocal(2));
        }
        
        private static PyObject translate$22(PyFrame frame) {
            /* translate(s,table [,deletechars]) -> string
            
                Return a copy of the string s, where all characters occurring
                in the optional argument deletechars are removed, and the
                remaining characters have been mapped through the given
                translation table, which must be a string of length 256.
            
                 */
            return frame.getlocal(0).invoke("translate", frame.getlocal(1), frame.getlocal(2));
        }
        
        private static PyObject capitalize$23(PyFrame frame) {
            /* capitalize(s) -> string
            
                Return a copy of the string s with only its first character
                capitalized.
            
                 */
            return frame.getlocal(0).invoke("capitalize");
        }
        
        private static PyObject capwords$24(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject;
            
            // Code
            /* capwords(s, [sep]) -> string
            
                Split the argument into words using split, capitalize each
                word using capitalize, and join the capitalized words using
                join. Note that this replaces runs of whitespace characters by
                a single space.
            
                 */
            return frame.getglobal("join").__call__(frame.getglobal("map").__call__(frame.getglobal("capitalize"), frame.getlocal(0).invoke("split", frame.getlocal(1))), (t$0$PyObject = frame.getlocal(1)).__nonzero__() ? t$0$PyObject : s$19);
        }
        
        private static PyObject maketrans$25(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            /* maketrans(frm, to) -> string
            
                Return a translation table (a string of 256 bytes long)
                suitable for use in string.translate.  The strings frm and to
                must be of the same length.
            
                 */
            if (frame.getglobal("len").__call__(frame.getlocal(0))._ne(frame.getglobal("len").__call__(frame.getlocal(1))).__nonzero__()) {
                throw Py.makeException(frame.getglobal("ValueError"), s$47);
            }
            // global _idmapL
            if (frame.getglobal("_idmapL").__not__().__nonzero__()) {
                frame.setglobal("_idmapL", frame.getglobal("map").__call__(frame.getglobal("None"), frame.getglobal("_idmap")));
            }
            frame.setlocal(3, frame.getglobal("_idmapL").__getslice__(null, null, null));
            frame.setlocal(0, frame.getglobal("map").__call__(frame.getglobal("ord"), frame.getlocal(0)));
            t$0$int = 0;
            t$1$PyObject = frame.getglobal("range").__call__(frame.getglobal("len").__call__(frame.getlocal(0)));
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                frame.setlocal(2, t$0$PyObject);
                frame.getlocal(3).__setitem__(frame.getlocal(0).__getitem__(frame.getlocal(2)), frame.getlocal(1).__getitem__(frame.getlocal(2)));
            }
            return frame.getglobal("joinfields").__call__(frame.getlocal(3), s$8);
        }
        
        private static PyObject replace$26(PyFrame frame) {
            /* replace (str, old, new[, maxsplit]) -> string
            
                Return a copy of string str with all occurrences of substring
                old replaced by new. If the optional argument maxsplit is
                given, only the first maxsplit occurrences are replaced.
            
                 */
            return frame.getlocal(0).invoke("replace", new PyObject[] {frame.getlocal(1), frame.getlocal(2), frame.getlocal(3)});
        }
        
        private static PyObject main$27(PyFrame frame) {
            frame.setglobal("__file__", s$49);
            
            PyObject[] imp_accu;
            // Temporary Variables
            int t$0$int;
            PyException t$0$PyException;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            /* Common string manipulations.
            
            Public module variables:
            
            whitespace -- a string containing all characters considered whitespace
            lowercase -- a string containing all characters considered lowercase letters
            uppercase -- a string containing all characters considered uppercase letters
            letters -- a string containing all characters considered letters
            digits -- a string containing all characters considered decimal digits
            hexdigits -- a string containing all characters considered hexadecimal digits
            octdigits -- a string containing all characters considered octal digits
            
             */
            frame.setlocal("whitespace", s$1);
            frame.setlocal("lowercase", s$2);
            frame.setlocal("uppercase", s$3);
            frame.setlocal("letters", frame.getname("lowercase")._add(frame.getname("uppercase")));
            frame.setlocal("digits", s$4);
            frame.setlocal("hexdigits", frame.getname("digits")._add(s$5)._add(s$6));
            frame.setlocal("octdigits", s$7);
            frame.setlocal("_idmap", s$8);
            t$0$int = 0;
            t$1$PyObject = frame.getname("range").__call__(i$9);
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                frame.setlocal("i", t$0$PyObject);
                frame.setlocal("_idmap", frame.getname("_idmap")._add(frame.getname("chr").__call__(frame.getname("i"))));
            }
            frame.dellocal("i");
            frame.setlocal("index_error", frame.getname("ValueError"));
            frame.setlocal("atoi_error", frame.getname("ValueError"));
            frame.setlocal("atof_error", frame.getname("ValueError"));
            frame.setlocal("atol_error", frame.getname("ValueError"));
            frame.setlocal("lower", new PyFunction(frame.f_globals, new PyObject[] {}, c$0_lower));
            frame.setlocal("upper", new PyFunction(frame.f_globals, new PyObject[] {}, c$1_upper));
            frame.setlocal("swapcase", new PyFunction(frame.f_globals, new PyObject[] {}, c$2_swapcase));
            frame.setlocal("strip", new PyFunction(frame.f_globals, new PyObject[] {}, c$3_strip));
            frame.setlocal("lstrip", new PyFunction(frame.f_globals, new PyObject[] {}, c$4_lstrip));
            frame.setlocal("rstrip", new PyFunction(frame.f_globals, new PyObject[] {}, c$5_rstrip));
            frame.setlocal("split", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None"), i$17.__neg__()}, c$6_split));
            frame.setlocal("splitfields", frame.getname("split"));
            frame.setlocal("join", new PyFunction(frame.f_globals, new PyObject[] {s$19}, c$7_join));
            frame.setlocal("joinfields", frame.getname("join"));
            frame.setlocal("_apply", frame.getname("apply"));
            frame.setlocal("index", new PyFunction(frame.f_globals, new PyObject[] {}, c$8_index));
            frame.setlocal("rindex", new PyFunction(frame.f_globals, new PyObject[] {}, c$9_rindex));
            frame.setlocal("count", new PyFunction(frame.f_globals, new PyObject[] {}, c$10_count));
            frame.setlocal("find", new PyFunction(frame.f_globals, new PyObject[] {}, c$11_find));
            frame.setlocal("rfind", new PyFunction(frame.f_globals, new PyObject[] {}, c$12_rfind));
            frame.setlocal("_float", frame.getname("float"));
            frame.setlocal("_int", frame.getname("int"));
            frame.setlocal("_long", frame.getname("long"));
            frame.setlocal("_StringType", frame.getname("type").__call__(s$8));
            frame.setlocal("atof", new PyFunction(frame.f_globals, new PyObject[] {}, c$13_atof));
            frame.setlocal("atoi", new PyFunction(frame.f_globals, new PyObject[] {}, c$14_atoi));
            frame.setlocal("atol", new PyFunction(frame.f_globals, new PyObject[] {}, c$15_atol));
            frame.setlocal("ljust", new PyFunction(frame.f_globals, new PyObject[] {}, c$16_ljust));
            frame.setlocal("rjust", new PyFunction(frame.f_globals, new PyObject[] {}, c$17_rjust));
            frame.setlocal("center", new PyFunction(frame.f_globals, new PyObject[] {}, c$18_center));
            frame.setlocal("zfill", new PyFunction(frame.f_globals, new PyObject[] {}, c$19_zfill));
            frame.setlocal("expandtabs", new PyFunction(frame.f_globals, new PyObject[] {i$42}, c$20_expandtabs));
            frame.setlocal("translate", new PyFunction(frame.f_globals, new PyObject[] {s$8}, c$21_translate));
            frame.setlocal("capitalize", new PyFunction(frame.f_globals, new PyObject[] {}, c$22_capitalize));
            frame.setlocal("capwords", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$23_capwords));
            frame.setlocal("_idmapL", frame.getname("None"));
            frame.setlocal("maketrans", new PyFunction(frame.f_globals, new PyObject[] {}, c$24_maketrans));
            frame.setlocal("replace", new PyFunction(frame.f_globals, new PyObject[] {i$17.__neg__()}, c$25_replace));
            try {
                imp_accu = org.python.core.imp.importFrom("strop", new String[] {"maketrans", "lowercase", "uppercase", "whitespace"}, frame);
                frame.setlocal("maketrans", imp_accu[0]);
                frame.setlocal("lowercase", imp_accu[1]);
                frame.setlocal("uppercase", imp_accu[2]);
                frame.setlocal("whitespace", imp_accu[3]);
                imp_accu = null;
                frame.setlocal("letters", frame.getname("lowercase")._add(frame.getname("uppercase")));
            }
            catch (Throwable x$0) {
                t$0$PyException = Py.setException(x$0, frame);
                if (Py.matchException(t$0$PyException, frame.getname("ImportError"))) {
                    // pass
                }
                else throw t$0$PyException;
            }
            return Py.None;
        }
        
    }
    public static void moduleDictInit(PyObject dict) {
        dict.__setitem__("__name__", new PyString("string"));
        Py.runCode(new _PyInner().getMain(), dict, dict);
    }
    
    public static void main(String[] args) throws java.lang.Exception {
        String[] newargs = new String[args.length+1];
        newargs[0] = "string";
        System.arraycopy(args, 0, newargs, 1, args.length);
        Py.runMain(string._PyInner.class, newargs, string.jpy$packages, string.jpy$mainProperties, "", new String[] {"string", "random", "util", "traceback", "sre_compile", "atexit", "sre", "sre_constants", "StringIO", "javaos", "socket", "yapm", "calendar", "repr", "copy_reg", "SocketServer", "server", "re", "linecache", "javapath", "UserDict", "copy", "threading", "stat", "PathVFS", "sre_parse"});
    }
    
}
