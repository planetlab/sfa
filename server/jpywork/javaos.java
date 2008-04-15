import org.python.core.*;

public class javaos extends java.lang.Object {
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
        private static PyObject i$13;
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
        private static PyObject f$25;
        private static PyObject s$26;
        private static PyObject i$27;
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
        private static PyObject s$44;
        private static PyObject s$45;
        private static PyObject s$46;
        private static PyObject s$47;
        private static PyObject s$48;
        private static PyObject s$49;
        private static PyObject s$50;
        private static PyObject s$51;
        private static PyObject s$52;
        private static PyObject s$53;
        private static PyObject s$54;
        private static PyObject s$55;
        private static PyObject s$56;
        private static PyObject s$57;
        private static PyObject s$58;
        private static PyObject s$59;
        private static PyObject s$60;
        private static PyObject s$61;
        private static PyObject s$62;
        private static PyObject s$63;
        private static PyObject s$64;
        private static PyObject s$65;
        private static PyObject s$66;
        private static PyObject s$67;
        private static PyObject s$68;
        private static PyObject s$69;
        private static PyObject s$70;
        private static PyObject s$71;
        private static PyObject s$72;
        private static PyObject s$73;
        private static PyObject s$74;
        private static PyObject s$75;
        private static PyObject s$76;
        private static PyObject s$77;
        private static PyObject s$78;
        private static PyObject s$79;
        private static PyObject s$80;
        private static PyObject s$81;
        private static PyObject s$82;
        private static PyObject s$83;
        private static PyObject s$84;
        private static PyObject s$85;
        private static PyObject s$86;
        private static PyObject s$87;
        private static PyObject s$88;
        private static PyObject s$89;
        private static PyObject s$90;
        private static PyObject s$91;
        private static PyObject s$92;
        private static PyObject s$93;
        private static PyObject s$94;
        private static PyObject s$95;
        private static PyObject s$96;
        private static PyObject s$97;
        private static PyObject s$98;
        private static PyObject s$99;
        private static PyObject s$100;
        private static PyObject s$101;
        private static PyObject s$102;
        private static PyObject s$103;
        private static PyObject s$104;
        private static PyObject s$105;
        private static PyObject s$106;
        private static PyObject s$107;
        private static PyObject s$108;
        private static PyObject s$109;
        private static PyFunctionTable funcTable;
        private static PyCode c$0__exit;
        private static PyCode c$1_getcwd;
        private static PyCode c$2_chdir;
        private static PyCode c$3_listdir;
        private static PyCode c$4_mkdir;
        private static PyCode c$5_makedirs;
        private static PyCode c$6_remove;
        private static PyCode c$7_rename;
        private static PyCode c$8_rmdir;
        private static PyCode c$9_stat;
        private static PyCode c$10_utime;
        private static PyCode c$11_lambda;
        private static PyCode c$12_lambda;
        private static PyCode c$13___init__;
        private static PyCode c$14__LazyDict__populate;
        private static PyCode c$15___repr__;
        private static PyCode c$16___cmp__;
        private static PyCode c$17___len__;
        private static PyCode c$18___getitem__;
        private static PyCode c$19___setitem__;
        private static PyCode c$20___delitem__;
        private static PyCode c$21_clear;
        private static PyCode c$22_copy;
        private static PyCode c$23_keys;
        private static PyCode c$24_items;
        private static PyCode c$25_values;
        private static PyCode c$26_has_key;
        private static PyCode c$27_update;
        private static PyCode c$28_get;
        private static PyCode c$29_setdefault;
        private static PyCode c$30_popitem;
        private static PyCode c$31_LazyDict;
        private static PyCode c$32___init__;
        private static PyCode c$33_println;
        private static PyCode c$34_printlnStdErr;
        private static PyCode c$35_system;
        private static PyCode c$36_execute;
        private static PyCode c$37__readLines;
        private static PyCode c$38__formatCmd;
        private static PyCode c$39__formatEnvironment;
        private static PyCode c$40__getEnvironment;
        private static PyCode c$41__ShellEnv;
        private static PyCode c$42__getOsType;
        private static PyCode c$43__getShellEnv;
        private static PyCode c$44__testGetOsType;
        private static PyCode c$45__testCmds;
        private static PyCode c$46__testSystem;
        private static PyCode c$47__testBadShell;
        private static PyCode c$48__testBadGetEnv;
        private static PyCode c$49__test;
        private static PyCode c$50_main;
        private static void initConstants() {
            s$0 = Py.newString("OS routines for Java, with some attempts to support DOS, NT, and\012Posix functionality.\012\012This exports:\012  - all functions from posix, nt, dos, os2, mac, or ce, e.g. unlink, stat, etc.\012  - os.path is one of the modules posixpath, ntpath, macpath, or dospath\012  - os.name is 'posix', 'nt', 'dos', 'os2', 'mac', 'ce' or 'riscos'\012  - os.curdir is a string representing the current directory ('.' or ':')\012  - os.pardir is a string representing the parent directory ('..' or '::')\012  - os.sep is the (or a most common) pathname separator ('/' or ':' or '\\\\')\012  - os.altsep is the alternate pathname separator (None or '/')\012  - os.pathsep is the component separator used in $PATH etc\012  - os.linesep is the line separator in text files ('\\r' or '\\n' or '\\r\\n')\012  - os.defpath is the default search path for executables\012\012Programs that import and use 'os' stand a better chance of being\012portable between different platforms.  Of course, they must then\012only use functions that are defined by all platforms (e.g., unlink\012and opendir), and leave all pathname manipulation to os.path\012(e.g., split and join).\012");
            s$1 = Py.newString("altsep");
            s$2 = Py.newString("curdir");
            s$3 = Py.newString("pardir");
            s$4 = Py.newString("sep");
            s$5 = Py.newString("pathsep");
            s$6 = Py.newString("linesep");
            s$7 = Py.newString("defpath");
            s$8 = Py.newString("name");
            s$9 = Py.newString("java");
            s$10 = Py.newString(".");
            s$11 = Py.newString("..");
            s$12 = Py.newString("line.separator");
            i$13 = Py.newInteger(0);
            s$14 = Py.newString("foo");
            s$15 = Py.newString("chdir not supported in Java");
            s$16 = Py.newString("No such directory");
            s$17 = Py.newString("couldn't make directory");
            s$18 = Py.newString("ignored");
            s$19 = Py.newString("couldn't make directories");
            s$20 = Py.newString("couldn't delete file");
            s$21 = Py.newString("couldn't rename file");
            s$22 = Py.newString("couldn't delete directory");
            s$23 = Py.newString("The Java stat implementation only returns a small subset of\012    the standard fields");
            s$24 = Py.newString("No such file or directory");
            f$25 = Py.newFloat(1000.0);
            s$26 = Py.newString("setLastModified");
            i$27 = Py.newInteger(1);
            s$28 = Py.newString("A lazy-populating User Dictionary.\012    Lazy initialization is not thread-safe.\012    ");
            s$29 = Py.newString("dict: starting dictionary of values\012        populate: function that returns the populated dictionary\012        keyTransform: function to normalize the keys (e.g., toupper/None)\012        ");
            s$30 = Py.newString("Provide environment derived by spawning a subshell and parsing its\012    environment.  Also supports system functions and provides empty\012    environment support for platforms with unknown shell\012    functionality.\012    ");
            s$31 = Py.newString("cmd: list of exec() arguments to run command in subshell, or None\012        getEnv: shell command to list environment variables, or None\012        keyTransform: normalization function for environment keys, or None\012        ");
            s$32 = Py.newString("Imitate the standard library 'system' call.\012        Execute 'cmd' in a shell, and send output to stdout & stderr.\012        ");
            s$33 = Py.newString("\012");
            s$34 = Py.newString("Execute cmd in a shell, and return the process instance");
            s$35 = Py.newString("Failed to execute command (%s): %s");
            s$36 = Py.newString("Read lines of stream, and either append them to return\012        array of lines, or call func on each line.\012        ");
            s$37 = Py.newString("Format a command for execution in a shell.");
            s$38 = Py.newString("Unable to execute commands in subshell because shell functionality not implemented for OS %s with shell setting %s. Failed command=%s");
            s$39 = Py.newString("Format enviroment in lines suitable for Runtime.exec");
            s$40 = Py.newString("%s=%s");
            s$41 = Py.newString("Get the environment variables by spawning a subshell.\012        This allows multi-line variables as long as subsequent lines do\012        not have '=' signs.\012        ");
            s$42 = Py.newString("=");
            s$43 = Py.newString("getEnv command (%s) did not print environment.\012Output=%s");
            s$44 = Py.newString("%s\012%s");
            s$45 = Py.newString("Failed to get environment, environ will be empty:");
            s$46 = Py.newString("Select the OS behavior based on os argument, 'python.os' registry\012    setting and 'os.name' Java property.\012    os: explicitly select desired OS. os=None to autodetect, os='None' to\012    disable \012    ");
            s$47 = Py.newString("python.os");
            s$48 = Py.newString("os.name");
            s$49 = Py.newString("nt");
            s$50 = Py.newString("(nt)|(Windows NT)|(Windows NT 4.0)|(WindowsNT)|(Windows 2000)|(Windows XP)|(Windows CE)");
            s$51 = Py.newString("dos");
            s$52 = Py.newString("(dos)|(Windows 95)|(Windows 98)|(Windows ME)");
            s$53 = Py.newString("mac");
            s$54 = Py.newString("(mac)|(MacOS.*)|(Darwin)");
            s$55 = Py.newString("None");
            s$56 = Py.newString("(None)");
            s$57 = Py.newString("posix");
            s$58 = Py.newString("(.*)");
            s$59 = Py.newString("Create the desired environment type.\012    envType: 'shell' or None\012    ");
            s$60 = Py.newString("shell");
            s$61 = Py.newString("python.environment");
            s$62 = Py.newString("cmd");
            s$63 = Py.newString("/c");
            s$64 = Py.newString("set");
            s$65 = Py.newString("command.com");
            s$66 = Py.newString("sh");
            s$67 = Py.newString("-c");
            s$68 = Py.newString("env");
            s$69 = Py.newString(":");
            s$70 = Py.newString("::");
            s$71 = Py.newString("Windows NT");
            s$72 = Py.newString("Windows 95");
            s$73 = Py.newString("MacOS");
            s$74 = Py.newString("Solaris");
            s$75 = Py.newString("Linux");
            s$76 = Py.newString("_getOsType( '%s' ) should return '%s', not '%s'");
            s$77 = Py.newString("\012Executing '%s' with %s environment");
            s$78 = Py.newString("%s failed with %s environment");
            s$79 = Py.newString("expected match for %s, got %s");
            s$80 = Py.newString("testKey");
            s$81 = Py.newString("testValue");
            s$82 = Py.newString("echo hello there");
            s$83 = Py.newString("hello there");
            s$84 = Py.newString("echo PATH=%PATH%");
            s$85 = Py.newString("(PATH=.*;.*)|(PATH=%PATH%)");
            s$86 = Py.newString("echo %s=%%%s%%");
            s$87 = Py.newString("(%s=)");
            s$88 = Py.newString("echo PATH=$PATH");
            s$89 = Py.newString("PATH=.*");
            s$90 = Py.newString("echo %s=$%s");
            s$91 = Py.newString("(%s=$%s)|(%s=)|(%s=%s)");
            s$92 = Py.newString("echo \"hello there\"");
            s$93 = Py.newString("\"?hello there\"?");
            s$94 = Py.newString("jython -c \"import sys;sys.stdout.write( 'why\\n' )\"");
            s$95 = Py.newString("why");
            s$96 = Py.newString("jython -c \"import sys;sys.stderr.write('why\\n');print \" ");
            s$97 = Py.newString("");
            s$98 = Py.newString("before population, environ._populated should be false");
            s$99 = Py.newString("default");
            s$100 = Py.newString("after population, environ._populated should be true");
            s$101 = Py.newString("expected stub to have %s set");
            s$102 = Py.newString("expected real environment to have %s set");
            s$103 = Py.newString("initialized");
            s$104 = Py.newString("PATH");
            s$105 = Py.newString("expected environment to have PATH attribute (this may not apply to all platforms!)");
            s$106 = Py.newString("badshell");
            s$107 = Py.newString("environment should be empty");
            s$108 = Py.newString("echo This command does not print environment");
            s$109 = Py.newString("/usr/share/jython/Lib/javaos.py");
            funcTable = new _PyInner();
            c$0__exit = Py.newCode(1, new String[] {"n"}, "/usr/share/jython/Lib/javaos.py", "_exit", false, false, funcTable, 0, null, null, 0, 1);
            c$1_getcwd = Py.newCode(0, new String[] {"foo"}, "/usr/share/jython/Lib/javaos.py", "getcwd", false, false, funcTable, 1, null, null, 0, 1);
            c$2_chdir = Py.newCode(1, new String[] {"path"}, "/usr/share/jython/Lib/javaos.py", "chdir", false, false, funcTable, 2, null, null, 0, 1);
            c$3_listdir = Py.newCode(1, new String[] {"path", "l"}, "/usr/share/jython/Lib/javaos.py", "listdir", false, false, funcTable, 3, null, null, 0, 1);
            c$4_mkdir = Py.newCode(2, new String[] {"path", "mode"}, "/usr/share/jython/Lib/javaos.py", "mkdir", false, false, funcTable, 4, null, null, 0, 1);
            c$5_makedirs = Py.newCode(2, new String[] {"path", "mode"}, "/usr/share/jython/Lib/javaos.py", "makedirs", false, false, funcTable, 5, null, null, 0, 1);
            c$6_remove = Py.newCode(1, new String[] {"path"}, "/usr/share/jython/Lib/javaos.py", "remove", false, false, funcTable, 6, null, null, 0, 1);
            c$7_rename = Py.newCode(2, new String[] {"path", "newpath"}, "/usr/share/jython/Lib/javaos.py", "rename", false, false, funcTable, 7, null, null, 0, 1);
            c$8_rmdir = Py.newCode(1, new String[] {"path"}, "/usr/share/jython/Lib/javaos.py", "rmdir", false, false, funcTable, 8, null, null, 0, 1);
            c$9_stat = Py.newCode(1, new String[] {"path", "mtime", "size", "f"}, "/usr/share/jython/Lib/javaos.py", "stat", false, false, funcTable, 9, null, null, 0, 1);
            c$10_utime = Py.newCode(2, new String[] {"path", "times"}, "/usr/share/jython/Lib/javaos.py", "utime", false, false, funcTable, 10, null, null, 0, 1);
            c$11_lambda = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib/javaos.py", "<lambda>", false, false, funcTable, 11, null, null, 0, 1);
            c$12_lambda = Py.newCode(1, new String[] {"key"}, "/usr/share/jython/Lib/javaos.py", "<lambda>", false, false, funcTable, 12, null, null, 0, 1);
            c$13___init__ = Py.newCode(4, new String[] {"self", "dict", "populate", "keyTransform"}, "/usr/share/jython/Lib/javaos.py", "__init__", false, false, funcTable, 13, null, null, 0, 1);
            c$14__LazyDict__populate = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib/javaos.py", "_LazyDict__populate", false, false, funcTable, 14, null, null, 0, 1);
            c$15___repr__ = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib/javaos.py", "__repr__", false, false, funcTable, 15, null, null, 0, 1);
            c$16___cmp__ = Py.newCode(2, new String[] {"self", "dict"}, "/usr/share/jython/Lib/javaos.py", "__cmp__", false, false, funcTable, 16, null, null, 0, 1);
            c$17___len__ = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib/javaos.py", "__len__", false, false, funcTable, 17, null, null, 0, 1);
            c$18___getitem__ = Py.newCode(2, new String[] {"self", "key"}, "/usr/share/jython/Lib/javaos.py", "__getitem__", false, false, funcTable, 18, null, null, 0, 1);
            c$19___setitem__ = Py.newCode(3, new String[] {"self", "key", "item"}, "/usr/share/jython/Lib/javaos.py", "__setitem__", false, false, funcTable, 19, null, null, 0, 1);
            c$20___delitem__ = Py.newCode(2, new String[] {"self", "key"}, "/usr/share/jython/Lib/javaos.py", "__delitem__", false, false, funcTable, 20, null, null, 0, 1);
            c$21_clear = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib/javaos.py", "clear", false, false, funcTable, 21, null, null, 0, 1);
            c$22_copy = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib/javaos.py", "copy", false, false, funcTable, 22, null, null, 0, 1);
            c$23_keys = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib/javaos.py", "keys", false, false, funcTable, 23, null, null, 0, 1);
            c$24_items = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib/javaos.py", "items", false, false, funcTable, 24, null, null, 0, 1);
            c$25_values = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib/javaos.py", "values", false, false, funcTable, 25, null, null, 0, 1);
            c$26_has_key = Py.newCode(2, new String[] {"self", "key"}, "/usr/share/jython/Lib/javaos.py", "has_key", false, false, funcTable, 26, null, null, 0, 1);
            c$27_update = Py.newCode(2, new String[] {"self", "dict"}, "/usr/share/jython/Lib/javaos.py", "update", false, false, funcTable, 27, null, null, 0, 1);
            c$28_get = Py.newCode(3, new String[] {"self", "key", "failobj"}, "/usr/share/jython/Lib/javaos.py", "get", false, false, funcTable, 28, null, null, 0, 1);
            c$29_setdefault = Py.newCode(3, new String[] {"self", "key", "failobj"}, "/usr/share/jython/Lib/javaos.py", "setdefault", false, false, funcTable, 29, null, null, 0, 1);
            c$30_popitem = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib/javaos.py", "popitem", false, false, funcTable, 30, null, null, 0, 1);
            c$31_LazyDict = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib/javaos.py", "LazyDict", false, false, funcTable, 31, null, null, 0, 0);
            c$32___init__ = Py.newCode(4, new String[] {"self", "cmd", "getEnv", "keyTransform"}, "/usr/share/jython/Lib/javaos.py", "__init__", false, false, funcTable, 32, null, null, 0, 1);
            c$33_println = Py.newCode(2, new String[] {"arg", "write"}, "/usr/share/jython/Lib/javaos.py", "println", false, false, funcTable, 33, null, null, 0, 1);
            c$34_printlnStdErr = Py.newCode(2, new String[] {"arg", "write"}, "/usr/share/jython/Lib/javaos.py", "printlnStdErr", false, false, funcTable, 34, null, null, 0, 1);
            c$35_system = Py.newCode(2, new String[] {"self", "cmd", "println", "printlnStdErr", "p"}, "/usr/share/jython/Lib/javaos.py", "system", false, false, funcTable, 35, null, null, 0, 1);
            c$36_execute = Py.newCode(2, new String[] {"self", "cmd", "p", "shellCmd", "env", "ex"}, "/usr/share/jython/Lib/javaos.py", "execute", false, false, funcTable, 36, null, null, 0, 1);
            c$37__readLines = Py.newCode(3, new String[] {"self", "stream", "func", "bufStream", "lines", "line"}, "/usr/share/jython/Lib/javaos.py", "_readLines", false, false, funcTable, 37, null, null, 0, 1);
            c$38__formatCmd = Py.newCode(2, new String[] {"self", "cmd", "msgFmt"}, "/usr/share/jython/Lib/javaos.py", "_formatCmd", false, false, funcTable, 38, null, null, 0, 1);
            c$39__formatEnvironment = Py.newCode(2, new String[] {"self", "env", "lines", "keyValue"}, "/usr/share/jython/Lib/javaos.py", "_formatEnvironment", false, false, funcTable, 39, null, null, 0, 1);
            c$40__getEnvironment = Py.newCode(1, new String[] {"self", "p", "i", "env", "ex", "value", "key", "lines", "line"}, "/usr/share/jython/Lib/javaos.py", "_getEnvironment", false, false, funcTable, 40, null, null, 0, 1);
            c$41__ShellEnv = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib/javaos.py", "_ShellEnv", false, false, funcTable, 41, null, null, 0, 0);
            c$42__getOsType = Py.newCode(1, new String[] {"os", "osType", "pattern", "_osTypeMap"}, "/usr/share/jython/Lib/javaos.py", "_getOsType", false, false, funcTable, 42, null, null, 0, 1);
            c$43__getShellEnv = Py.newCode(4, new String[] {"envType", "shellCmd", "envCmd", "envTransform"}, "/usr/share/jython/Lib/javaos.py", "_getShellEnv", false, false, funcTable, 43, null, null, 0, 1);
            c$44__testGetOsType = Py.newCode(0, new String[] {"got", "key", "testVals", "msgFmt", "val"}, "/usr/share/jython/Lib/javaos.py", "_testGetOsType", false, false, funcTable, 44, null, null, 0, 1);
            c$45__testCmds = Py.newCode(3, new String[] {"_shellEnv", "testCmds", "whichEnv", "line", "pattern", "cmd"}, "/usr/share/jython/Lib/javaos.py", "_testCmds", false, false, funcTable, 45, null, null, 0, 1);
            c$46__testSystem = Py.newCode(1, new String[] {"shellEnv", "testCmds", "value", "key", "org"}, "/usr/share/jython/Lib/javaos.py", "_testSystem", false, false, funcTable, 46, null, null, 0, 1);
            c$47__testBadShell = Py.newCode(0, new String[] {"se2"}, "/usr/share/jython/Lib/javaos.py", "_testBadShell", false, false, funcTable, 47, null, null, 0, 1);
            c$48__testBadGetEnv = Py.newCode(0, new String[] {"se2"}, "/usr/share/jython/Lib/javaos.py", "_testBadGetEnv", false, false, funcTable, 48, null, null, 0, 1);
            c$49__test = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib/javaos.py", "_test", false, false, funcTable, 49, null, null, 0, 1);
            c$50_main = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib/javaos.py", "main", false, false, funcTable, 50, null, null, 0, 0);
        }
        
        
        public PyCode getMain() {
            if (c$50_main == null) _PyInner.initConstants();
            return c$50_main;
        }
        
        public PyObject call_function(int index, PyFrame frame) {
            switch (index){
                case 0:
                return _PyInner._exit$1(frame);
                case 1:
                return _PyInner.getcwd$2(frame);
                case 2:
                return _PyInner.chdir$3(frame);
                case 3:
                return _PyInner.listdir$4(frame);
                case 4:
                return _PyInner.mkdir$5(frame);
                case 5:
                return _PyInner.makedirs$6(frame);
                case 6:
                return _PyInner.remove$7(frame);
                case 7:
                return _PyInner.rename$8(frame);
                case 8:
                return _PyInner.rmdir$9(frame);
                case 9:
                return _PyInner.stat$10(frame);
                case 10:
                return _PyInner.utime$11(frame);
                case 11:
                return _PyInner.lambda$12(frame);
                case 12:
                return _PyInner.lambda$13(frame);
                case 13:
                return _PyInner.__init__$14(frame);
                case 14:
                return _PyInner._LazyDict__populate$15(frame);
                case 15:
                return _PyInner.__repr__$16(frame);
                case 16:
                return _PyInner.__cmp__$17(frame);
                case 17:
                return _PyInner.__len__$18(frame);
                case 18:
                return _PyInner.__getitem__$19(frame);
                case 19:
                return _PyInner.__setitem__$20(frame);
                case 20:
                return _PyInner.__delitem__$21(frame);
                case 21:
                return _PyInner.clear$22(frame);
                case 22:
                return _PyInner.copy$23(frame);
                case 23:
                return _PyInner.keys$24(frame);
                case 24:
                return _PyInner.items$25(frame);
                case 25:
                return _PyInner.values$26(frame);
                case 26:
                return _PyInner.has_key$27(frame);
                case 27:
                return _PyInner.update$28(frame);
                case 28:
                return _PyInner.get$29(frame);
                case 29:
                return _PyInner.setdefault$30(frame);
                case 30:
                return _PyInner.popitem$31(frame);
                case 31:
                return _PyInner.LazyDict$32(frame);
                case 32:
                return _PyInner.__init__$33(frame);
                case 33:
                return _PyInner.println$34(frame);
                case 34:
                return _PyInner.printlnStdErr$35(frame);
                case 35:
                return _PyInner.system$36(frame);
                case 36:
                return _PyInner.execute$37(frame);
                case 37:
                return _PyInner._readLines$38(frame);
                case 38:
                return _PyInner._formatCmd$39(frame);
                case 39:
                return _PyInner._formatEnvironment$40(frame);
                case 40:
                return _PyInner._getEnvironment$41(frame);
                case 41:
                return _PyInner._ShellEnv$42(frame);
                case 42:
                return _PyInner._getOsType$43(frame);
                case 43:
                return _PyInner._getShellEnv$44(frame);
                case 44:
                return _PyInner._testGetOsType$45(frame);
                case 45:
                return _PyInner._testCmds$46(frame);
                case 46:
                return _PyInner._testSystem$47(frame);
                case 47:
                return _PyInner._testBadShell$48(frame);
                case 48:
                return _PyInner._testBadGetEnv$49(frame);
                case 49:
                return _PyInner._test$50(frame);
                case 50:
                return _PyInner.main$51(frame);
                default:
                return null;
            }
        }
        
        private static PyObject _exit$1(PyFrame frame) {
            frame.getglobal("java").__getattr__("lang").__getattr__("System").__getattr__("exit").__call__(frame.getlocal(0));
            return Py.None;
        }
        
        private static PyObject getcwd$2(PyFrame frame) {
            frame.setlocal(0, frame.getglobal("File").__call__(frame.getglobal("File").__call__(s$14).invoke("getAbsolutePath")));
            return frame.getlocal(0).invoke("getParent");
        }
        
        private static PyObject chdir$3(PyFrame frame) {
            throw Py.makeException(frame.getglobal("OSError").__call__(i$13, s$15, frame.getlocal(0)));
        }
        
        private static PyObject listdir$4(PyFrame frame) {
            frame.setlocal(1, frame.getglobal("File").__call__(frame.getlocal(0)).invoke("list"));
            if (frame.getlocal(1)._is(frame.getglobal("None")).__nonzero__()) {
                throw Py.makeException(frame.getglobal("OSError").__call__(i$13, s$16, frame.getlocal(0)));
            }
            return frame.getglobal("list").__call__(frame.getlocal(1));
        }
        
        private static PyObject mkdir$5(PyFrame frame) {
            if (frame.getglobal("File").__call__(frame.getlocal(0)).invoke("mkdir").__not__().__nonzero__()) {
                throw Py.makeException(frame.getglobal("OSError").__call__(i$13, s$17, frame.getlocal(0)));
            }
            return Py.None;
        }
        
        private static PyObject makedirs$6(PyFrame frame) {
            if (frame.getglobal("File").__call__(frame.getlocal(0)).invoke("mkdirs").__not__().__nonzero__()) {
                throw Py.makeException(frame.getglobal("OSError").__call__(i$13, s$19, frame.getlocal(0)));
            }
            return Py.None;
        }
        
        private static PyObject remove$7(PyFrame frame) {
            if (frame.getglobal("File").__call__(frame.getlocal(0)).invoke("delete").__not__().__nonzero__()) {
                throw Py.makeException(frame.getglobal("OSError").__call__(i$13, s$20, frame.getlocal(0)));
            }
            return Py.None;
        }
        
        private static PyObject rename$8(PyFrame frame) {
            if (frame.getglobal("File").__call__(frame.getlocal(0)).invoke("renameTo", frame.getglobal("File").__call__(frame.getlocal(1))).__not__().__nonzero__()) {
                throw Py.makeException(frame.getglobal("OSError").__call__(i$13, s$21, frame.getlocal(0)));
            }
            return Py.None;
        }
        
        private static PyObject rmdir$9(PyFrame frame) {
            if (frame.getglobal("File").__call__(frame.getlocal(0)).invoke("delete").__not__().__nonzero__()) {
                throw Py.makeException(frame.getglobal("OSError").__call__(i$13, s$22, frame.getlocal(0)));
            }
            return Py.None;
        }
        
        private static PyObject stat$10(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject;
            
            // Code
            /* The Java stat implementation only returns a small subset of
                the standard fields */
            frame.setlocal(3, frame.getglobal("File").__call__(frame.getlocal(0)));
            frame.setlocal(2, frame.getlocal(3).invoke("length"));
            if (((t$0$PyObject = frame.getlocal(2)._eq(i$13)).__nonzero__() ? frame.getlocal(3).invoke("exists").__not__() : t$0$PyObject).__nonzero__()) {
                throw Py.makeException(frame.getglobal("OSError").__call__(i$13, s$24, frame.getlocal(0)));
            }
            frame.setlocal(1, frame.getlocal(3).invoke("lastModified")._div(f$25));
            return new PyTuple(new PyObject[] {i$13, i$13, i$13, i$13, i$13, i$13, frame.getlocal(2), frame.getlocal(1), frame.getlocal(1), i$13});
        }
        
        private static PyObject utime$11(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject;
            
            // Code
            if (((t$0$PyObject = frame.getlocal(1)).__nonzero__() ? frame.getglobal("hasattr").__call__(frame.getglobal("File"), s$26) : t$0$PyObject).__nonzero__()) {
                frame.getglobal("File").__call__(frame.getlocal(0)).invoke("setLastModified", frame.getglobal("long").__call__(frame.getlocal(1).__getitem__(i$27)._mul(f$25)));
            }
            return Py.None;
        }
        
        private static PyObject lambda$12(PyFrame frame) {
            return new PyDictionary(new PyObject[] {});
        }
        
        private static PyObject lambda$13(PyFrame frame) {
            return frame.getlocal(0);
        }
        
        private static PyObject __init__$14(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject;
            
            // Code
            /* dict: starting dictionary of values
                    populate: function that returns the populated dictionary
                    keyTransform: function to normalize the keys (e.g., toupper/None)
                     */
            frame.getglobal("UserDict").__getattr__("__init__").__call__(frame.getlocal(0), frame.getlocal(1));
            frame.getlocal(0).__setattr__("_populated", i$13);
            frame.getlocal(0).__setattr__("_LazyDict__populateFunc", (t$0$PyObject = frame.getlocal(2)).__nonzero__() ? t$0$PyObject : new PyFunction(frame.f_globals, new PyObject[] {}, c$11_lambda));
            frame.getlocal(0).__setattr__("_keyTransform", (t$0$PyObject = frame.getlocal(3)).__nonzero__() ? t$0$PyObject : new PyFunction(frame.f_globals, new PyObject[] {}, c$12_lambda));
            return Py.None;
        }
        
        private static PyObject _LazyDict__populate$15(PyFrame frame) {
            if (frame.getlocal(0).__getattr__("_populated").__not__().__nonzero__()) {
                frame.getlocal(0).__setattr__("data", frame.getlocal(0).invoke("_LazyDict__populateFunc"));
                frame.getlocal(0).__setattr__("_populated", i$27);
            }
            return Py.None;
        }
        
        private static PyObject __repr__$16(PyFrame frame) {
            frame.getlocal(0).invoke("_LazyDict__populate");
            return frame.getglobal("UserDict").__getattr__("__repr__").__call__(frame.getlocal(0));
        }
        
        private static PyObject __cmp__$17(PyFrame frame) {
            frame.getlocal(0).invoke("_LazyDict__populate");
            return frame.getglobal("UserDict").__getattr__("__cmp__").__call__(frame.getlocal(0), frame.getlocal(1));
        }
        
        private static PyObject __len__$18(PyFrame frame) {
            frame.getlocal(0).invoke("_LazyDict__populate");
            return frame.getglobal("UserDict").__getattr__("__len__").__call__(frame.getlocal(0));
        }
        
        private static PyObject __getitem__$19(PyFrame frame) {
            frame.getlocal(0).invoke("_LazyDict__populate");
            return frame.getglobal("UserDict").__getattr__("__getitem__").__call__(frame.getlocal(0), frame.getlocal(0).invoke("_keyTransform", frame.getlocal(1)));
        }
        
        private static PyObject __setitem__$20(PyFrame frame) {
            frame.getlocal(0).invoke("_LazyDict__populate");
            frame.getglobal("UserDict").__getattr__("__setitem__").__call__(frame.getlocal(0), frame.getlocal(0).invoke("_keyTransform", frame.getlocal(1)), frame.getlocal(2));
            return Py.None;
        }
        
        private static PyObject __delitem__$21(PyFrame frame) {
            frame.getlocal(0).invoke("_LazyDict__populate");
            frame.getglobal("UserDict").__getattr__("__delitem__").__call__(frame.getlocal(0), frame.getlocal(0).invoke("_keyTransform", frame.getlocal(1)));
            return Py.None;
        }
        
        private static PyObject clear$22(PyFrame frame) {
            frame.getlocal(0).invoke("_LazyDict__populate");
            frame.getglobal("UserDict").__getattr__("clear").__call__(frame.getlocal(0));
            return Py.None;
        }
        
        private static PyObject copy$23(PyFrame frame) {
            frame.getlocal(0).invoke("_LazyDict__populate");
            return frame.getglobal("UserDict").__getattr__("copy").__call__(frame.getlocal(0));
        }
        
        private static PyObject keys$24(PyFrame frame) {
            frame.getlocal(0).invoke("_LazyDict__populate");
            return frame.getglobal("UserDict").__getattr__("keys").__call__(frame.getlocal(0));
        }
        
        private static PyObject items$25(PyFrame frame) {
            frame.getlocal(0).invoke("_LazyDict__populate");
            return frame.getglobal("UserDict").__getattr__("items").__call__(frame.getlocal(0));
        }
        
        private static PyObject values$26(PyFrame frame) {
            frame.getlocal(0).invoke("_LazyDict__populate");
            return frame.getglobal("UserDict").__getattr__("values").__call__(frame.getlocal(0));
        }
        
        private static PyObject has_key$27(PyFrame frame) {
            frame.getlocal(0).invoke("_LazyDict__populate");
            return frame.getglobal("UserDict").__getattr__("has_key").__call__(frame.getlocal(0), frame.getlocal(0).invoke("_keyTransform", frame.getlocal(1)));
        }
        
        private static PyObject update$28(PyFrame frame) {
            frame.getlocal(0).invoke("_LazyDict__populate");
            frame.getglobal("UserDict").__getattr__("update").__call__(frame.getlocal(0), frame.getlocal(1));
            return Py.None;
        }
        
        private static PyObject get$29(PyFrame frame) {
            frame.getlocal(0).invoke("_LazyDict__populate");
            return frame.getglobal("UserDict").__getattr__("get").__call__(frame.getlocal(0), frame.getlocal(0).invoke("_keyTransform", frame.getlocal(1)), frame.getlocal(2));
        }
        
        private static PyObject setdefault$30(PyFrame frame) {
            frame.getlocal(0).invoke("_LazyDict__populate");
            return frame.getglobal("UserDict").__getattr__("setdefault").__call__(frame.getlocal(0), frame.getlocal(0).invoke("_keyTransform", frame.getlocal(1)), frame.getlocal(2));
        }
        
        private static PyObject popitem$31(PyFrame frame) {
            frame.getlocal(0).invoke("_LazyDict__populate");
            return frame.getglobal("UserDict").__getattr__("popitem").__call__(frame.getlocal(0));
        }
        
        private static PyObject LazyDict$32(PyFrame frame) {
            /* A lazy-populating User Dictionary.
                Lazy initialization is not thread-safe.
                 */
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None"), frame.getname("None"), frame.getname("None")}, c$13___init__));
            frame.setlocal("_LazyDict__populate", new PyFunction(frame.f_globals, new PyObject[] {}, c$14__LazyDict__populate));
            frame.setlocal("__repr__", new PyFunction(frame.f_globals, new PyObject[] {}, c$15___repr__));
            frame.setlocal("__cmp__", new PyFunction(frame.f_globals, new PyObject[] {}, c$16___cmp__));
            frame.setlocal("__len__", new PyFunction(frame.f_globals, new PyObject[] {}, c$17___len__));
            frame.setlocal("__getitem__", new PyFunction(frame.f_globals, new PyObject[] {}, c$18___getitem__));
            frame.setlocal("__setitem__", new PyFunction(frame.f_globals, new PyObject[] {}, c$19___setitem__));
            frame.setlocal("__delitem__", new PyFunction(frame.f_globals, new PyObject[] {}, c$20___delitem__));
            frame.setlocal("clear", new PyFunction(frame.f_globals, new PyObject[] {}, c$21_clear));
            frame.setlocal("copy", new PyFunction(frame.f_globals, new PyObject[] {}, c$22_copy));
            frame.setlocal("keys", new PyFunction(frame.f_globals, new PyObject[] {}, c$23_keys));
            frame.setlocal("items", new PyFunction(frame.f_globals, new PyObject[] {}, c$24_items));
            frame.setlocal("values", new PyFunction(frame.f_globals, new PyObject[] {}, c$25_values));
            frame.setlocal("has_key", new PyFunction(frame.f_globals, new PyObject[] {}, c$26_has_key));
            frame.setlocal("update", new PyFunction(frame.f_globals, new PyObject[] {}, c$27_update));
            frame.setlocal("get", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$28_get));
            frame.setlocal("setdefault", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$29_setdefault));
            frame.setlocal("popitem", new PyFunction(frame.f_globals, new PyObject[] {}, c$30_popitem));
            return frame.getf_locals();
        }
        
        private static PyObject __init__$33(PyFrame frame) {
            /* cmd: list of exec() arguments to run command in subshell, or None
                    getEnv: shell command to list environment variables, or None
                    keyTransform: normalization function for environment keys, or None
                     */
            frame.getlocal(0).__setattr__("cmd", frame.getlocal(1));
            frame.getlocal(0).__setattr__("getEnv", frame.getlocal(2));
            frame.getlocal(0).__setattr__("environment", frame.getglobal("LazyDict").__call__(new PyObject[] {frame.getlocal(0).__getattr__("_getEnvironment"), frame.getlocal(3)}, new String[] {"populate", "keyTransform"}));
            frame.getlocal(0).__setattr__("_keyTransform", frame.getlocal(0).__getattr__("environment").__getattr__("_keyTransform"));
            return Py.None;
        }
        
        private static PyObject println$34(PyFrame frame) {
            frame.getlocal(1).__call__(frame.getlocal(0)._add(s$33));
            return Py.None;
        }
        
        private static PyObject printlnStdErr$35(PyFrame frame) {
            frame.getlocal(1).__call__(frame.getlocal(0)._add(s$33));
            return Py.None;
        }
        
        private static PyObject system$36(PyFrame frame) {
            /* Imitate the standard library 'system' call.
                    Execute 'cmd' in a shell, and send output to stdout & stderr.
                     */
            frame.setlocal(4, frame.getlocal(0).invoke("execute", frame.getlocal(1)));
            frame.setlocal(2, new PyFunction(frame.f_globals, new PyObject[] {frame.getglobal("sys").__getattr__("stdout").__getattr__("write")}, c$33_println));
            frame.setlocal(3, new PyFunction(frame.f_globals, new PyObject[] {frame.getglobal("sys").__getattr__("stderr").__getattr__("write")}, c$34_printlnStdErr));
            frame.getglobal("thread").__getattr__("start_new_thread").__call__(frame.getlocal(0).__getattr__("_readLines"), new PyTuple(new PyObject[] {frame.getlocal(4).invoke("getErrorStream"), frame.getlocal(3)}));
            frame.getlocal(0).invoke("_readLines", frame.getlocal(4).invoke("getInputStream"), frame.getlocal(2));
            return frame.getlocal(4).invoke("waitFor");
        }
        
        private static PyObject execute$37(PyFrame frame) {
            // Temporary Variables
            PyException t$0$PyException;
            
            // Code
            /* Execute cmd in a shell, and return the process instance */
            frame.setlocal(3, frame.getlocal(0).invoke("_formatCmd", frame.getlocal(1)));
            if (frame.getlocal(0).__getattr__("environment").__getattr__("_populated").__nonzero__()) {
                frame.setlocal(4, frame.getlocal(0).invoke("_formatEnvironment", frame.getlocal(0).__getattr__("environment")));
            }
            else {
                frame.setlocal(4, frame.getglobal("None"));
            }
            try {
                frame.setlocal(2, frame.getglobal("java").__getattr__("lang").__getattr__("Runtime").__getattr__("getRuntime").__call__().invoke("exec", frame.getlocal(3), frame.getlocal(4)));
                return frame.getlocal(2);
            }
            catch (Throwable x$0) {
                t$0$PyException = Py.setException(x$0, frame);
                if (Py.matchException(t$0$PyException, frame.getglobal("IOException"))) {
                    frame.setlocal(5, t$0$PyException.value);
                    throw Py.makeException(frame.getglobal("OSError").__call__(i$13, s$35._mod(new PyTuple(new PyObject[] {frame.getlocal(3), frame.getlocal(5)}))));
                }
                else throw t$0$PyException;
            }
        }
        
        private static PyObject _readLines$38(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject;
            
            // Code
            /* Read lines of stream, and either append them to return
                    array of lines, or call func on each line.
                     */
            frame.setlocal(4, new PyList(new PyObject[] {}));
            frame.setlocal(2, (t$0$PyObject = frame.getlocal(2)).__nonzero__() ? t$0$PyObject : frame.getlocal(4).__getattr__("append"));
            frame.setlocal(3, frame.getglobal("BufferedReader").__call__(frame.getglobal("InputStreamReader").__call__(frame.getlocal(1))));
            while (i$27.__nonzero__()) {
                frame.setlocal(5, frame.getlocal(3).invoke("readLine"));
                if (frame.getlocal(5)._is(frame.getglobal("None")).__nonzero__()) {
                    break;
                }
                frame.getlocal(2).__call__(frame.getlocal(5));
            }
            return (t$0$PyObject = frame.getlocal(4)).__nonzero__() ? t$0$PyObject : frame.getglobal("None");
        }
        
        private static PyObject _formatCmd$39(PyFrame frame) {
            /* Format a command for execution in a shell. */
            if (frame.getlocal(0).__getattr__("cmd")._is(frame.getglobal("None")).__nonzero__()) {
                frame.setlocal(2, s$38);
                throw Py.makeException(frame.getglobal("OSError").__call__(i$13, frame.getlocal(2)._mod(new PyTuple(new PyObject[] {frame.getglobal("_osType"), frame.getglobal("_envType"), frame.getlocal(1)}))));
            }
            return frame.getlocal(0).__getattr__("cmd")._add(new PyList(new PyObject[] {frame.getlocal(1)}));
        }
        
        private static PyObject _formatEnvironment$40(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            /* Format enviroment in lines suitable for Runtime.exec */
            frame.setlocal(2, new PyList(new PyObject[] {}));
            t$0$int = 0;
            t$1$PyObject = frame.getlocal(1).invoke("items");
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                frame.setlocal(3, t$0$PyObject);
                frame.getlocal(2).invoke("append", s$40._mod(frame.getlocal(3)));
            }
            return frame.getlocal(2);
        }
        
        private static PyObject _getEnvironment$41(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyException t$0$PyException;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            /* Get the environment variables by spawning a subshell.
                    This allows multi-line variables as long as subsequent lines do
                    not have '=' signs.
                     */
            frame.setlocal(3, new PyDictionary(new PyObject[] {}));
            if (frame.getlocal(0).__getattr__("getEnv").__nonzero__()) {
                try {
                    frame.setlocal(1, frame.getlocal(0).invoke("execute", frame.getlocal(0).__getattr__("getEnv")));
                    frame.setlocal(7, frame.getlocal(0).invoke("_readLines", frame.getlocal(1).invoke("getInputStream")));
                    if (s$42._notin(frame.getlocal(7).__getitem__(i$13)).__nonzero__()) {
                        Py.println(s$43._mod(new PyTuple(new PyObject[] {frame.getlocal(0).__getattr__("getEnv"), s$33.invoke("join", frame.getlocal(7))})));
                        return frame.getlocal(3);
                    }
                    t$0$int = 0;
                    t$1$PyObject = frame.getlocal(7);
                    while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                        frame.setlocal(8, t$0$PyObject);
                        try {
                            frame.setlocal(2, frame.getlocal(8).invoke("index", s$42));
                            frame.setlocal(6, frame.getlocal(0).invoke("_keyTransform", frame.getlocal(8).__getslice__(null, frame.getlocal(2), null)));
                            frame.setlocal(5, frame.getlocal(8).__getslice__(frame.getlocal(2)._add(i$27), null, null));
                        }
                        catch (Throwable x$0) {
                            t$0$PyException = Py.setException(x$0, frame);
                            if (Py.matchException(t$0$PyException, frame.getglobal("ValueError"))) {
                                frame.setlocal(5, s$44._mod(new PyTuple(new PyObject[] {frame.getlocal(5), frame.getlocal(8)})));
                            }
                            else throw t$0$PyException;
                        }
                        frame.getlocal(3).__setitem__(frame.getlocal(6), frame.getlocal(5));
                    }
                }
                catch (Throwable x$1) {
                    t$0$PyException = Py.setException(x$1, frame);
                    if (Py.matchException(t$0$PyException, frame.getglobal("OSError"))) {
                        frame.setlocal(4, t$0$PyException.value);
                        Py.printComma(s$45);
                        Py.println(frame.getlocal(4));
                    }
                    else throw t$0$PyException;
                }
            }
            return frame.getlocal(3);
        }
        
        private static PyObject _ShellEnv$42(PyFrame frame) {
            /* Provide environment derived by spawning a subshell and parsing its
                environment.  Also supports system functions and provides empty
                environment support for platforms with unknown shell
                functionality.
                 */
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None"), frame.getname("None"), frame.getname("None")}, c$32___init__));
            frame.setlocal("system", new PyFunction(frame.f_globals, new PyObject[] {}, c$35_system));
            frame.setlocal("execute", new PyFunction(frame.f_globals, new PyObject[] {}, c$36_execute));
            frame.setlocal("_readLines", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$37__readLines));
            frame.setlocal("_formatCmd", new PyFunction(frame.f_globals, new PyObject[] {}, c$38__formatCmd));
            frame.setlocal("_formatEnvironment", new PyFunction(frame.f_globals, new PyObject[] {}, c$39__formatEnvironment));
            frame.setlocal("_getEnvironment", new PyFunction(frame.f_globals, new PyObject[] {}, c$40__getEnvironment));
            return frame.getf_locals();
        }
        
        private static PyObject _getOsType$43(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyObject[] t$0$PyObject__;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            /* Select the OS behavior based on os argument, 'python.os' registry
                setting and 'os.name' Java property.
                os: explicitly select desired OS. os=None to autodetect, os='None' to
                disable 
                 */
            frame.setlocal(0, (t$0$PyObject = ((t$1$PyObject = frame.getlocal(0)).__nonzero__() ? t$1$PyObject : frame.getglobal("sys").__getattr__("registry").__getattr__("getProperty").__call__(s$47))).__nonzero__() ? t$0$PyObject : frame.getglobal("java").__getattr__("lang").__getattr__("System").__getattr__("getProperty").__call__(s$48));
            frame.setlocal(3, new PyTuple(new PyObject[] {new PyTuple(new PyObject[] {s$49, s$50}), new PyTuple(new PyObject[] {s$51, s$52}), new PyTuple(new PyObject[] {s$53, s$54}), new PyTuple(new PyObject[] {s$55, s$56}), new PyTuple(new PyObject[] {s$57, s$58})}));
            t$0$int = 0;
            t$1$PyObject = frame.getlocal(3);
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                t$0$PyObject__ = org.python.core.Py.unpackSequence(t$0$PyObject, 2);
                frame.setlocal(1, t$0$PyObject__[0]);
                frame.setlocal(2, t$0$PyObject__[1]);
                if (frame.getglobal("re").__getattr__("match").__call__(frame.getlocal(2), frame.getlocal(0)).__nonzero__()) {
                    break;
                }
            }
            return frame.getlocal(1);
        }
        
        private static PyObject _getShellEnv$44(PyFrame frame) {
            /* Create the desired environment type.
                envType: 'shell' or None
                 */
            if (frame.getlocal(0)._eq(s$60).__nonzero__()) {
                return frame.getglobal("_ShellEnv").__call__(frame.getlocal(1), frame.getlocal(2), frame.getlocal(3));
            }
            else {
                return frame.getglobal("_ShellEnv").__call__();
            }
        }
        
        private static PyObject _testGetOsType$45(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyObject[] t$0$PyObject__;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            frame.setlocal(2, new PyDictionary(new PyObject[] {s$71, s$49, s$72, s$51, s$73, s$53, s$74, s$57, s$75, s$57, s$55, s$55}));
            frame.setlocal(3, s$76);
            t$0$int = 0;
            t$1$PyObject = frame.getlocal(2).invoke("items");
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                t$0$PyObject__ = org.python.core.Py.unpackSequence(t$0$PyObject, 2);
                frame.setlocal(1, t$0$PyObject__[0]);
                frame.setlocal(4, t$0$PyObject__[1]);
                frame.setlocal(0, frame.getglobal("_getOsType").__call__(frame.getlocal(1)));
                if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0)._eq(frame.getlocal(4)), frame.getlocal(3)._mod(new PyTuple(new PyObject[] {frame.getlocal(1), frame.getlocal(4), frame.getlocal(0)})));
            }
            return Py.None;
        }
        
        private static PyObject _testCmds$46(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyObject[] t$0$PyObject__;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            t$0$int = 0;
            t$1$PyObject = frame.getlocal(1);
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                t$0$PyObject__ = org.python.core.Py.unpackSequence(t$0$PyObject, 2);
                frame.setlocal(5, t$0$PyObject__[0]);
                frame.setlocal(4, t$0$PyObject__[1]);
                Py.println(s$77._mod(new PyTuple(new PyObject[] {frame.getlocal(5), frame.getlocal(2)})));
                if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).invoke("system", frame.getlocal(5)).__not__(), s$78._mod(new PyTuple(new PyObject[] {frame.getlocal(5), frame.getlocal(2)})));
                frame.setlocal(3, frame.getlocal(0).invoke("_readLines", frame.getlocal(0).invoke("execute", frame.getlocal(5)).invoke("getInputStream")).__getitem__(i$13));
                if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getglobal("re").__getattr__("match").__call__(frame.getlocal(4), frame.getlocal(3)), s$79._mod(new PyTuple(new PyObject[] {frame.getlocal(4), frame.getlocal(3)})));
            }
            return Py.None;
        }
        
        private static PyObject _testSystem$47(PyFrame frame) {
            // Temporary Variables
            PyObject[] t$0$PyObject__;
            
            // Code
            t$0$PyObject__ = org.python.core.Py.unpackSequence(new PyTuple(new PyObject[] {s$80, s$81}), 2);
            frame.setlocal(3, t$0$PyObject__[0]);
            frame.setlocal(2, t$0$PyObject__[1]);
            frame.setlocal(4, frame.getglobal("environ"));
            frame.setlocal(1, new PyList(new PyObject[] {new PyTuple(new PyObject[] {s$82, s$83}), new PyTuple(new PyObject[] {s$84, s$85}), new PyTuple(new PyObject[] {s$86._mod(new PyTuple(new PyObject[] {frame.getlocal(3), frame.getlocal(3)})), s$87._mod(new PyTuple(new PyObject[] {frame.getlocal(3)}))}), new PyTuple(new PyObject[] {s$88, s$89}), new PyTuple(new PyObject[] {s$90._mod(new PyTuple(new PyObject[] {frame.getlocal(3), frame.getlocal(3)})), s$91._mod(new PyTuple(new PyObject[] {frame.getlocal(3), frame.getlocal(3), frame.getlocal(3), frame.getlocal(3), frame.getlocal(2)}))}), new PyTuple(new PyObject[] {s$92, s$93}), new PyTuple(new PyObject[] {s$94, s$95}), new PyTuple(new PyObject[] {s$96, s$97})}));
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getglobal("environ").__getattr__("_populated").__not__(), s$98);
            frame.getglobal("_testCmds").__call__(frame.getglobal("_shellEnv"), frame.getlocal(1), s$99);
            frame.getglobal("environ").__setitem__(frame.getlocal(3), frame.getlocal(2));
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getglobal("environ").__getattr__("_populated"), s$100);
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(4).invoke("get", frame.getlocal(3), frame.getglobal("None"))._eq(frame.getlocal(2)), s$101._mod(frame.getlocal(3)));
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getglobal("environ").invoke("get", frame.getlocal(3), frame.getglobal("None"))._eq(frame.getlocal(2)), s$102._mod(frame.getlocal(3)));
            frame.getglobal("_testCmds").__call__(frame.getglobal("_shellEnv"), frame.getlocal(1), s$103);
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getglobal("environ").invoke("has_key", s$104), s$105);
            return Py.None;
        }
        
        private static PyObject _testBadShell$48(PyFrame frame) {
            frame.setlocal(0, frame.getglobal("_ShellEnv").__call__(new PyList(new PyObject[] {s$106, s$67}), s$64));
            frame.getglobal("str").__call__(frame.getlocal(0).__getattr__("environment"));
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("environment").invoke("items").__not__(), s$107);
            return Py.None;
        }
        
        private static PyObject _testBadGetEnv$49(PyFrame frame) {
            frame.setlocal(0, frame.getglobal("_getShellEnv").__call__(new PyObject[] {s$60, frame.getglobal("_shellCmd"), frame.getglobal("_envCmd"), frame.getglobal("_envTransform")}));
            frame.getlocal(0).__setattr__("getEnv", s$108);
            frame.getglobal("str").__call__(frame.getlocal(0).__getattr__("environment"));
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("environment").invoke("items").__not__(), s$107);
            return Py.None;
        }
        
        private static PyObject _test$50(PyFrame frame) {
            frame.getglobal("_testGetOsType").__call__();
            frame.getglobal("_testBadShell").__call__();
            frame.getglobal("_testBadGetEnv").__call__();
            frame.getglobal("_testSystem").__call__();
            return Py.None;
        }
        
        private static PyObject main$51(PyFrame frame) {
            frame.setglobal("__file__", s$109);
            
            PyObject[] imp_accu;
            // Code
            /* OS routines for Java, with some attempts to support DOS, NT, and
            Posix functionality.
            
            This exports:
              - all functions from posix, nt, dos, os2, mac, or ce, e.g. unlink, stat, etc.
              - os.path is one of the modules posixpath, ntpath, macpath, or dospath
              - os.name is 'posix', 'nt', 'dos', 'os2', 'mac', 'ce' or 'riscos'
              - os.curdir is a string representing the current directory ('.' or ':')
              - os.pardir is a string representing the parent directory ('..' or '::')
              - os.sep is the (or a most common) pathname separator ('/' or ':' or '\\')
              - os.altsep is the alternate pathname separator (None or '/')
              - os.pathsep is the component separator used in $PATH etc
              - os.linesep is the line separator in text files ('\r' or '\n' or '\r\n')
              - os.defpath is the default search path for executables
            
            Programs that import and use 'os' stand a better chance of being
            portable between different platforms.  Of course, they must then
            only use functions that are defined by all platforms (e.g., unlink
            and opendir), and leave all pathname manipulation to os.path
            (e.g., split and join).
             */
            frame.setlocal("__all__", new PyList(new PyObject[] {s$1, s$2, s$3, s$4, s$5, s$6, s$7, s$8}));
            frame.setlocal("java", org.python.core.imp.importOne("java", frame));
            imp_accu = org.python.core.imp.importFrom("java.io", new String[] {"File", "BufferedReader", "InputStreamReader", "IOException"}, frame);
            frame.setlocal("File", imp_accu[0]);
            frame.setlocal("BufferedReader", imp_accu[1]);
            frame.setlocal("InputStreamReader", imp_accu[2]);
            frame.setlocal("IOException", imp_accu[3]);
            imp_accu = null;
            frame.setlocal("path", org.python.core.imp.importOneAs("javapath", frame));
            imp_accu = org.python.core.imp.importFrom("UserDict", new String[] {"UserDict"}, frame);
            frame.setlocal("UserDict", imp_accu[0]);
            imp_accu = null;
            frame.setlocal("string", org.python.core.imp.importOne("string", frame));
            frame.setlocal("exceptions", org.python.core.imp.importOne("exceptions", frame));
            frame.setlocal("re", org.python.core.imp.importOne("re", frame));
            frame.setlocal("sys", org.python.core.imp.importOne("sys", frame));
            frame.setlocal("thread", org.python.core.imp.importOne("thread", frame));
            frame.setlocal("error", frame.getname("OSError"));
            frame.setlocal("name", s$9);
            frame.setlocal("curdir", s$10);
            frame.setlocal("pardir", s$11);
            frame.setlocal("sep", frame.getname("java").__getattr__("io").__getattr__("File").__getattr__("separator"));
            frame.setlocal("altsep", frame.getname("None"));
            frame.setlocal("pathsep", frame.getname("java").__getattr__("io").__getattr__("File").__getattr__("pathSeparator"));
            frame.setlocal("defpath", s$10);
            frame.setlocal("linesep", frame.getname("java").__getattr__("lang").__getattr__("System").__getattr__("getProperty").__call__(s$12));
            frame.setlocal("_exit", new PyFunction(frame.f_globals, new PyObject[] {i$13}, c$0__exit));
            frame.setlocal("getcwd", new PyFunction(frame.f_globals, new PyObject[] {}, c$1_getcwd));
            frame.setlocal("chdir", new PyFunction(frame.f_globals, new PyObject[] {}, c$2_chdir));
            frame.setlocal("listdir", new PyFunction(frame.f_globals, new PyObject[] {}, c$3_listdir));
            frame.setlocal("mkdir", new PyFunction(frame.f_globals, new PyObject[] {s$18}, c$4_mkdir));
            frame.setlocal("makedirs", new PyFunction(frame.f_globals, new PyObject[] {s$18}, c$5_makedirs));
            frame.setlocal("remove", new PyFunction(frame.f_globals, new PyObject[] {}, c$6_remove));
            frame.setlocal("rename", new PyFunction(frame.f_globals, new PyObject[] {}, c$7_rename));
            frame.setlocal("rmdir", new PyFunction(frame.f_globals, new PyObject[] {}, c$8_rmdir));
            frame.setlocal("unlink", frame.getname("remove"));
            frame.setlocal("stat", new PyFunction(frame.f_globals, new PyObject[] {}, c$9_stat));
            frame.setlocal("utime", new PyFunction(frame.f_globals, new PyObject[] {}, c$10_utime));
            frame.setlocal("LazyDict", Py.makeClass("LazyDict", new PyObject[] {frame.getname("UserDict")}, c$31_LazyDict, null));
            frame.setlocal("_ShellEnv", Py.makeClass("_ShellEnv", new PyObject[] {}, c$41__ShellEnv, null));
            frame.setlocal("_getOsType", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$42__getOsType));
            frame.setlocal("_getShellEnv", new PyFunction(frame.f_globals, new PyObject[] {}, c$43__getShellEnv));
            frame.setlocal("_osType", frame.getname("_getOsType").__call__());
            frame.setlocal("_envType", frame.getname("sys").__getattr__("registry").__getattr__("getProperty").__call__(s$61, s$60));
            frame.setlocal("_shellCmd", frame.getname("None"));
            frame.setlocal("_envCmd", frame.getname("None"));
            frame.setlocal("_envTransform", frame.getname("None"));
            if (frame.getname("_osType")._eq(s$49).__nonzero__()) {
                frame.setlocal("_shellCmd", new PyList(new PyObject[] {s$62, s$63}));
                frame.setlocal("_envCmd", s$64);
                frame.setlocal("_envTransform", frame.getname("string").__getattr__("upper"));
            }
            else if (frame.getname("_osType")._eq(s$51).__nonzero__()) {
                frame.setlocal("_shellCmd", new PyList(new PyObject[] {s$65, s$63}));
                frame.setlocal("_envCmd", s$64);
                frame.setlocal("_envTransform", frame.getname("string").__getattr__("upper"));
            }
            else if (frame.getname("_osType")._eq(s$57).__nonzero__()) {
                frame.setlocal("_shellCmd", new PyList(new PyObject[] {s$66, s$67}));
                frame.setlocal("_envCmd", s$68);
            }
            else if (frame.getname("_osType")._eq(s$53).__nonzero__()) {
                frame.setlocal("curdir", s$69);
                frame.setlocal("pardir", s$70);
            }
            else if (frame.getname("_osType")._eq(s$55).__nonzero__()) {
                // pass
            }
            frame.setlocal("_shellEnv", frame.getname("_getShellEnv").__call__(new PyObject[] {frame.getname("_envType"), frame.getname("_shellCmd"), frame.getname("_envCmd"), frame.getname("_envTransform")}));
            frame.setlocal("environ", frame.getname("_shellEnv").__getattr__("environment"));
            frame.setlocal("putenv", frame.getname("environ").__getattr__("__setitem__"));
            frame.setlocal("getenv", frame.getname("environ").__getattr__("__getitem__"));
            frame.setlocal("system", frame.getname("_shellEnv").__getattr__("system"));
            frame.setlocal("_testGetOsType", new PyFunction(frame.f_globals, new PyObject[] {}, c$44__testGetOsType));
            frame.setlocal("_testCmds", new PyFunction(frame.f_globals, new PyObject[] {}, c$45__testCmds));
            frame.setlocal("_testSystem", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("_shellEnv")}, c$46__testSystem));
            frame.setlocal("_testBadShell", new PyFunction(frame.f_globals, new PyObject[] {}, c$47__testBadShell));
            frame.setlocal("_testBadGetEnv", new PyFunction(frame.f_globals, new PyObject[] {}, c$48__testBadGetEnv));
            frame.setlocal("_test", new PyFunction(frame.f_globals, new PyObject[] {}, c$49__test));
            return Py.None;
        }
        
    }
    public static void moduleDictInit(PyObject dict) {
        dict.__setitem__("__name__", new PyString("javaos"));
        Py.runCode(new _PyInner().getMain(), dict, dict);
    }
    
    public static void main(String[] args) throws java.lang.Exception {
        String[] newargs = new String[args.length+1];
        newargs[0] = "javaos";
        System.arraycopy(args, 0, newargs, 1, args.length);
        Py.runMain(javaos._PyInner.class, newargs, javaos.jpy$packages, javaos.jpy$mainProperties, "", new String[] {"string", "random", "util", "traceback", "sre_compile", "atexit", "sre", "sre_constants", "StringIO", "javaos", "socket", "yapm", "calendar", "repr", "copy_reg", "SocketServer", "server", "re", "linecache", "javapath", "UserDict", "copy", "threading", "stat", "PathVFS", "sre_parse"});
    }
    
}
