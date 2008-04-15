import org.python.core.*;

public class socket extends java.lang.Object {
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
        private static PyObject i$14;
        private static PyObject i$15;
        private static PyObject i$16;
        private static PyObject i$17;
        private static PyObject i$18;
        private static PyObject i$19;
        private static PyObject s$20;
        private static PyObject s$21;
        private static PyObject i$22;
        private static PyObject s$23;
        private static PyObject s$24;
        private static PyObject s$25;
        private static PyObject i$26;
        private static PyObject s$27;
        private static PyObject s$28;
        private static PyObject s$29;
        private static PyObject s$30;
        private static PyObject s$31;
        private static PyObject i$32;
        private static PyObject s$33;
        private static PyObject i$34;
        private static PyObject s$35;
        private static PyObject s$36;
        private static PyFunctionTable funcTable;
        private static PyCode c$0__gethostbyaddr;
        private static PyCode c$1_getfqdn;
        private static PyCode c$2_gethostname;
        private static PyCode c$3_gethostbyname;
        private static PyCode c$4_gethostbyaddr;
        private static PyCode c$5_socket;
        private static PyCode c$6_bind;
        private static PyCode c$7_listen;
        private static PyCode c$8_accept;
        private static PyCode c$9_connect;
        private static PyCode c$10__setup;
        private static PyCode c$11_recv;
        private static PyCode c$12_send;
        private static PyCode c$13_getsockname;
        private static PyCode c$14_getpeername;
        private static PyCode c$15_setsockopt;
        private static PyCode c$16_getsockopt;
        private static PyCode c$17_makefile;
        private static PyCode c$18___init__;
        private static PyCode c$19_close;
        private static PyCode c$20_FileWrapper;
        private static PyCode c$21_shutdown;
        private static PyCode c$22_close;
        private static PyCode c$23__tcpsocket;
        private static PyCode c$24___init__;
        private static PyCode c$25_bind;
        private static PyCode c$26_connect;
        private static PyCode c$27_sendto;
        private static PyCode c$28_send;
        private static PyCode c$29_recvfrom;
        private static PyCode c$30_recv;
        private static PyCode c$31_getsockname;
        private static PyCode c$32_getpeername;
        private static PyCode c$33___del__;
        private static PyCode c$34_close;
        private static PyCode c$35__udpsocket;
        private static PyCode c$36_test;
        private static PyCode c$37_main;
        private static void initConstants() {
            s$0 = Py.newString("Preliminary socket module.\012\012XXX Restrictions:\012\012- Only INET sockets\012- No asynchronous behavior\012- No socket options\012- Can't do a very good gethostbyaddr() right...\012\012");
            s$1 = Py.newString("AF_INET");
            s$2 = Py.newString("SOCK_DGRAM");
            s$3 = Py.newString("SOCK_RAW");
            s$4 = Py.newString("SOCK_RDM");
            s$5 = Py.newString("SOCK_SEQPACKET");
            s$6 = Py.newString("SOCK_STREAM");
            s$7 = Py.newString("SocketType");
            s$8 = Py.newString("error");
            s$9 = Py.newString("getfqdn");
            s$10 = Py.newString("gethostbyaddr");
            s$11 = Py.newString("gethostbyname");
            s$12 = Py.newString("gethostname");
            s$13 = Py.newString("socket");
            i$14 = Py.newInteger(2);
            i$15 = Py.newInteger(1);
            i$16 = Py.newInteger(3);
            i$17 = Py.newInteger(4);
            i$18 = Py.newInteger(5);
            i$19 = Py.newInteger(65535);
            s$20 = Py.newString("\012    Return a fully qualified domain name for name. If name is omitted or empty\012    it is interpreted as the local host.  To find the fully qualified name,\012    the hostname returned by gethostbyaddr() is checked, then aliases for the\012    host, if available. The first name which includes a period is selected.\012    In case no fully qualified domain name is available, the hostname is retur\012    New in version 2.0.\012    ");
            s$21 = Py.newString(".");
            i$22 = Py.newInteger(0);
            s$23 = Py.newString("This signifies a server socket");
            s$24 = Py.newString("");
            s$25 = Py.newString("setReuseAddress");
            i$26 = Py.newInteger(50);
            s$27 = Py.newString("This signifies a client socket");
            s$28 = Py.newString("b");
            s$29 = Py.newString("<socket>");
            s$30 = Py.newString("both istream and ostream have been shut down");
            s$31 = Py.newString("r");
            i$32 = Py.newInteger(80);
            s$33 = Py.newString("GET / HTTP/1.0\015\012\015\012");
            i$34 = Py.newInteger(2000);
            s$35 = Py.newString("__main__");
            s$36 = Py.newString("/usr/share/jython/Lib/socket.py");
            funcTable = new _PyInner();
            c$0__gethostbyaddr = Py.newCode(1, new String[] {"name", "addrs", "names", "addresses", "addr"}, "/usr/share/jython/Lib/socket.py", "_gethostbyaddr", false, false, funcTable, 0, null, null, 0, 1);
            c$1_getfqdn = Py.newCode(1, new String[] {"name", "a", "addrs", "names"}, "/usr/share/jython/Lib/socket.py", "getfqdn", false, false, funcTable, 1, null, null, 0, 1);
            c$2_gethostname = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib/socket.py", "gethostname", false, false, funcTable, 2, null, null, 0, 1);
            c$3_gethostbyname = Py.newCode(1, new String[] {"name"}, "/usr/share/jython/Lib/socket.py", "gethostbyname", false, false, funcTable, 3, null, null, 0, 1);
            c$4_gethostbyaddr = Py.newCode(1, new String[] {"name", "addrs", "names"}, "/usr/share/jython/Lib/socket.py", "gethostbyaddr", false, false, funcTable, 4, null, null, 0, 1);
            c$5_socket = Py.newCode(3, new String[] {"family", "type", "flags"}, "/usr/share/jython/Lib/socket.py", "socket", false, false, funcTable, 5, null, null, 0, 1);
            c$6_bind = Py.newCode(3, new String[] {"self", "addr", "port", "host"}, "/usr/share/jython/Lib/socket.py", "bind", false, false, funcTable, 6, null, null, 0, 1);
            c$7_listen = Py.newCode(2, new String[] {"self", "backlog", "a", "port", "host"}, "/usr/share/jython/Lib/socket.py", "listen", false, false, funcTable, 7, null, null, 0, 1);
            c$8_accept = Py.newCode(1, new String[] {"self", "port", "sock", "conn", "host"}, "/usr/share/jython/Lib/socket.py", "accept", false, false, funcTable, 8, null, null, 0, 1);
            c$9_connect = Py.newCode(3, new String[] {"self", "addr", "port", "host"}, "/usr/share/jython/Lib/socket.py", "connect", false, false, funcTable, 9, null, null, 0, 1);
            c$10__setup = Py.newCode(2, new String[] {"self", "sock"}, "/usr/share/jython/Lib/socket.py", "_setup", false, false, funcTable, 10, null, null, 0, 1);
            c$11_recv = Py.newCode(2, new String[] {"self", "n", "m", "data"}, "/usr/share/jython/Lib/socket.py", "recv", false, false, funcTable, 11, null, null, 0, 1);
            c$12_send = Py.newCode(2, new String[] {"self", "s", "n"}, "/usr/share/jython/Lib/socket.py", "send", false, false, funcTable, 12, null, null, 0, 1);
            c$13_getsockname = Py.newCode(1, new String[] {"self", "port", "host"}, "/usr/share/jython/Lib/socket.py", "getsockname", false, false, funcTable, 13, null, null, 0, 1);
            c$14_getpeername = Py.newCode(1, new String[] {"self", "port", "host"}, "/usr/share/jython/Lib/socket.py", "getpeername", false, false, funcTable, 14, null, null, 0, 1);
            c$15_setsockopt = Py.newCode(4, new String[] {"self", "level", "optname", "value"}, "/usr/share/jython/Lib/socket.py", "setsockopt", false, false, funcTable, 15, null, null, 0, 1);
            c$16_getsockopt = Py.newCode(3, new String[] {"self", "level", "optname"}, "/usr/share/jython/Lib/socket.py", "getsockopt", false, false, funcTable, 16, null, null, 0, 1);
            c$17_makefile = Py.newCode(3, new String[] {"self", "mode", "bufsize", "file"}, "/usr/share/jython/Lib/socket.py", "makefile", false, false, funcTable, 17, null, null, 0, 1);
            c$18___init__ = Py.newCode(3, new String[] {"self", "socket", "file"}, "/usr/share/jython/Lib/socket.py", "__init__", false, false, funcTable, 18, null, null, 0, 1);
            c$19_close = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib/socket.py", "close", false, false, funcTable, 19, null, null, 0, 1);
            c$20_FileWrapper = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib/socket.py", "FileWrapper", false, false, funcTable, 20, null, null, 0, 0);
            c$21_shutdown = Py.newCode(2, new String[] {"self", "how"}, "/usr/share/jython/Lib/socket.py", "shutdown", false, false, funcTable, 21, null, null, 0, 1);
            c$22_close = Py.newCode(1, new String[] {"self", "ostream", "sock", "istream"}, "/usr/share/jython/Lib/socket.py", "close", false, false, funcTable, 22, null, null, 0, 1);
            c$23__tcpsocket = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib/socket.py", "_tcpsocket", false, false, funcTable, 23, null, null, 0, 0);
            c$24___init__ = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib/socket.py", "__init__", false, false, funcTable, 24, null, null, 0, 1);
            c$25_bind = Py.newCode(3, new String[] {"self", "addr", "port", "a", "host"}, "/usr/share/jython/Lib/socket.py", "bind", false, false, funcTable, 25, null, null, 0, 1);
            c$26_connect = Py.newCode(3, new String[] {"self", "addr", "port", "host"}, "/usr/share/jython/Lib/socket.py", "connect", false, false, funcTable, 26, null, null, 0, 1);
            c$27_sendto = Py.newCode(3, new String[] {"self", "data", "addr", "packet", "n", "port", "a", "host", "bytes"}, "/usr/share/jython/Lib/socket.py", "sendto", false, false, funcTable, 27, null, null, 0, 1);
            c$28_send = Py.newCode(2, new String[] {"self", "data"}, "/usr/share/jython/Lib/socket.py", "send", false, false, funcTable, 28, null, null, 0, 1);
            c$29_recvfrom = Py.newCode(2, new String[] {"self", "n", "packet", "port", "m", "host", "bytes"}, "/usr/share/jython/Lib/socket.py", "recvfrom", false, false, funcTable, 29, null, null, 0, 1);
            c$30_recv = Py.newCode(2, new String[] {"self", "n", "m", "bytes", "packet"}, "/usr/share/jython/Lib/socket.py", "recv", false, false, funcTable, 30, null, null, 0, 1);
            c$31_getsockname = Py.newCode(1, new String[] {"self", "port", "host"}, "/usr/share/jython/Lib/socket.py", "getsockname", false, false, funcTable, 31, null, null, 0, 1);
            c$32_getpeername = Py.newCode(1, new String[] {"self", "port", "host"}, "/usr/share/jython/Lib/socket.py", "getpeername", false, false, funcTable, 32, null, null, 0, 1);
            c$33___del__ = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib/socket.py", "__del__", false, false, funcTable, 33, null, null, 0, 1);
            c$34_close = Py.newCode(1, new String[] {"self", "sock"}, "/usr/share/jython/Lib/socket.py", "close", false, false, funcTable, 34, null, null, 0, 1);
            c$35__udpsocket = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib/socket.py", "_udpsocket", false, false, funcTable, 35, null, null, 0, 0);
            c$36_test = Py.newCode(0, new String[] {"s", "data"}, "/usr/share/jython/Lib/socket.py", "test", false, false, funcTable, 36, null, null, 0, 1);
            c$37_main = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib/socket.py", "main", false, false, funcTable, 37, null, null, 0, 0);
        }
        
        
        public PyCode getMain() {
            if (c$37_main == null) _PyInner.initConstants();
            return c$37_main;
        }
        
        public PyObject call_function(int index, PyFrame frame) {
            switch (index){
                case 0:
                return _PyInner._gethostbyaddr$1(frame);
                case 1:
                return _PyInner.getfqdn$2(frame);
                case 2:
                return _PyInner.gethostname$3(frame);
                case 3:
                return _PyInner.gethostbyname$4(frame);
                case 4:
                return _PyInner.gethostbyaddr$5(frame);
                case 5:
                return _PyInner.socket$6(frame);
                case 6:
                return _PyInner.bind$7(frame);
                case 7:
                return _PyInner.listen$8(frame);
                case 8:
                return _PyInner.accept$9(frame);
                case 9:
                return _PyInner.connect$10(frame);
                case 10:
                return _PyInner._setup$11(frame);
                case 11:
                return _PyInner.recv$12(frame);
                case 12:
                return _PyInner.send$13(frame);
                case 13:
                return _PyInner.getsockname$14(frame);
                case 14:
                return _PyInner.getpeername$15(frame);
                case 15:
                return _PyInner.setsockopt$16(frame);
                case 16:
                return _PyInner.getsockopt$17(frame);
                case 17:
                return _PyInner.makefile$18(frame);
                case 18:
                return _PyInner.__init__$19(frame);
                case 19:
                return _PyInner.close$20(frame);
                case 20:
                return _PyInner.FileWrapper$21(frame);
                case 21:
                return _PyInner.shutdown$22(frame);
                case 22:
                return _PyInner.close$23(frame);
                case 23:
                return _PyInner._tcpsocket$24(frame);
                case 24:
                return _PyInner.__init__$25(frame);
                case 25:
                return _PyInner.bind$26(frame);
                case 26:
                return _PyInner.connect$27(frame);
                case 27:
                return _PyInner.sendto$28(frame);
                case 28:
                return _PyInner.send$29(frame);
                case 29:
                return _PyInner.recvfrom$30(frame);
                case 30:
                return _PyInner.recv$31(frame);
                case 31:
                return _PyInner.getsockname$32(frame);
                case 32:
                return _PyInner.getpeername$33(frame);
                case 33:
                return _PyInner.__del__$34(frame);
                case 34:
                return _PyInner.close$35(frame);
                case 35:
                return _PyInner._udpsocket$36(frame);
                case 36:
                return _PyInner.test$37(frame);
                case 37:
                return _PyInner.main$38(frame);
                default:
                return null;
            }
        }
        
        private static PyObject _gethostbyaddr$1(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            frame.setlocal(3, frame.getglobal("java").__getattr__("net").__getattr__("InetAddress").__getattr__("getAllByName").__call__(frame.getglobal("gethostbyname").__call__(frame.getlocal(0))));
            frame.setlocal(2, new PyList(new PyObject[] {}));
            frame.setlocal(1, new PyList(new PyObject[] {}));
            t$0$int = 0;
            t$1$PyObject = frame.getlocal(3);
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                frame.setlocal(4, t$0$PyObject);
                frame.getlocal(2).invoke("append", frame.getlocal(4).invoke("getHostName"));
                frame.getlocal(1).invoke("append", frame.getlocal(4).invoke("getHostAddress"));
            }
            return new PyTuple(new PyObject[] {frame.getlocal(2), frame.getlocal(1)});
        }
        
        private static PyObject getfqdn$2(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyObject[] t$0$PyObject__;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            /* 
                Return a fully qualified domain name for name. If name is omitted or empty
                it is interpreted as the local host.  To find the fully qualified name,
                the hostname returned by gethostbyaddr() is checked, then aliases for the
                host, if available. The first name which includes a period is selected.
                In case no fully qualified domain name is available, the hostname is retur
                New in version 2.0.
                 */
            if (frame.getlocal(0).__not__().__nonzero__()) {
                frame.setlocal(0, frame.getglobal("gethostname").__call__());
            }
            t$0$PyObject__ = org.python.core.Py.unpackSequence(frame.getglobal("_gethostbyaddr").__call__(frame.getlocal(0)), 2);
            frame.setlocal(3, t$0$PyObject__[0]);
            frame.setlocal(2, t$0$PyObject__[1]);
            t$0$int = 0;
            t$1$PyObject = frame.getlocal(3);
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                frame.setlocal(1, t$0$PyObject);
                if (frame.getlocal(1).invoke("find", s$21)._ge(i$22).__nonzero__()) {
                    return frame.getlocal(1);
                }
            }
            return frame.getlocal(0);
        }
        
        private static PyObject gethostname$3(PyFrame frame) {
            return frame.getglobal("java").__getattr__("net").__getattr__("InetAddress").__getattr__("getLocalHost").__call__().invoke("getHostName");
        }
        
        private static PyObject gethostbyname$4(PyFrame frame) {
            return frame.getglobal("java").__getattr__("net").__getattr__("InetAddress").__getattr__("getByName").__call__(frame.getlocal(0)).invoke("getHostAddress");
        }
        
        private static PyObject gethostbyaddr$5(PyFrame frame) {
            // Temporary Variables
            PyObject[] t$0$PyObject__;
            
            // Code
            t$0$PyObject__ = org.python.core.Py.unpackSequence(frame.getglobal("_gethostbyaddr").__call__(frame.getlocal(0)), 2);
            frame.setlocal(2, t$0$PyObject__[0]);
            frame.setlocal(1, t$0$PyObject__[1]);
            return new PyTuple(new PyObject[] {frame.getlocal(2).__getitem__(i$22), frame.getlocal(2), frame.getlocal(1)});
        }
        
        private static PyObject socket$6(PyFrame frame) {
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0)._eq(frame.getglobal("AF_INET")));
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(1)._in(new PyTuple(new PyObject[] {frame.getglobal("SOCK_DGRAM"), frame.getglobal("SOCK_STREAM")})));
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(2)._eq(i$22));
            if (frame.getlocal(1)._eq(frame.getglobal("SOCK_STREAM")).__nonzero__()) {
                return frame.getglobal("_tcpsocket").__call__();
            }
            else {
                return frame.getglobal("_udpsocket").__call__();
            }
        }
        
        private static PyObject bind$7(PyFrame frame) {
            // Temporary Variables
            PyObject[] t$0$PyObject__;
            
            // Code
            if (frame.getlocal(2)._isnot(frame.getglobal("None")).__nonzero__()) {
                frame.setlocal(1, new PyTuple(new PyObject[] {frame.getlocal(1), frame.getlocal(2)}));
            }
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("sock").__not__());
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("addr").__not__());
            t$0$PyObject__ = org.python.core.Py.unpackSequence(frame.getlocal(1), 2);
            frame.setlocal(3, t$0$PyObject__[0]);
            frame.setlocal(2, t$0$PyObject__[1]);
            frame.getlocal(0).__setattr__("addr", frame.getlocal(1));
            return Py.None;
        }
        
        private static PyObject listen$8(PyFrame frame) {
            // Temporary Variables
            PyObject[] t$0$PyObject__;
            
            // Code
            /* This signifies a server socket */
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("sock").__not__());
            frame.getlocal(0).__setattr__("server", i$15);
            if (frame.getlocal(0).__getattr__("addr").__nonzero__()) {
                t$0$PyObject__ = org.python.core.Py.unpackSequence(frame.getlocal(0).__getattr__("addr"), 2);
                frame.setlocal(4, t$0$PyObject__[0]);
                frame.setlocal(3, t$0$PyObject__[1]);
            }
            else {
                t$0$PyObject__ = org.python.core.Py.unpackSequence(new PyTuple(new PyObject[] {s$24, i$22}), 2);
                frame.setlocal(4, t$0$PyObject__[0]);
                frame.setlocal(3, t$0$PyObject__[1]);
            }
            if (frame.getlocal(4).__nonzero__()) {
                frame.setlocal(2, frame.getglobal("java").__getattr__("net").__getattr__("InetAddress").__getattr__("getByName").__call__(frame.getlocal(4)));
                frame.getlocal(0).__setattr__("sock", frame.getglobal("java").__getattr__("net").__getattr__("ServerSocket").__call__(frame.getlocal(3), frame.getlocal(1), frame.getlocal(2)));
            }
            else {
                frame.getlocal(0).__setattr__("sock", frame.getglobal("java").__getattr__("net").__getattr__("ServerSocket").__call__(frame.getlocal(3), frame.getlocal(1)));
            }
            if (frame.getglobal("hasattr").__call__(frame.getlocal(0).__getattr__("sock"), s$25).__nonzero__()) {
                frame.getlocal(0).__getattr__("sock").invoke("setReuseAddress", frame.getlocal(0).__getattr__("reuse_addr"));
            }
            return Py.None;
        }
        
        private static PyObject accept$9(PyFrame frame) {
            /* This signifies a server socket */
            if (frame.getlocal(0).__getattr__("sock").__not__().__nonzero__()) {
                frame.getlocal(0).invoke("listen");
            }
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("server"));
            frame.setlocal(2, frame.getlocal(0).__getattr__("sock").invoke("accept"));
            frame.setlocal(4, frame.getlocal(2).invoke("getInetAddress").invoke("getHostName"));
            frame.setlocal(1, frame.getlocal(2).invoke("getPort"));
            frame.setlocal(3, frame.getglobal("_tcpsocket").__call__());
            frame.getlocal(3).invoke("_setup", frame.getlocal(2));
            return new PyTuple(new PyObject[] {frame.getlocal(3), new PyTuple(new PyObject[] {frame.getlocal(4), frame.getlocal(1)})});
        }
        
        private static PyObject connect$10(PyFrame frame) {
            // Temporary Variables
            PyObject[] t$0$PyObject__;
            
            // Code
            /* This signifies a client socket */
            if (frame.getlocal(2)._isnot(frame.getglobal("None")).__nonzero__()) {
                frame.setlocal(1, new PyTuple(new PyObject[] {frame.getlocal(1), frame.getlocal(2)}));
            }
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("sock").__not__());
            t$0$PyObject__ = org.python.core.Py.unpackSequence(frame.getlocal(1), 2);
            frame.setlocal(3, t$0$PyObject__[0]);
            frame.setlocal(2, t$0$PyObject__[1]);
            if (frame.getlocal(3)._eq(s$24).__nonzero__()) {
                frame.setlocal(3, frame.getglobal("java").__getattr__("net").__getattr__("InetAddress").__getattr__("getLocalHost").__call__());
            }
            frame.getlocal(0).invoke("_setup", frame.getglobal("java").__getattr__("net").__getattr__("Socket").__call__(frame.getlocal(3), frame.getlocal(2)));
            return Py.None;
        }
        
        private static PyObject _setup$11(PyFrame frame) {
            frame.getlocal(0).__setattr__("sock", frame.getlocal(1));
            if (frame.getglobal("hasattr").__call__(frame.getlocal(0).__getattr__("sock"), s$25).__nonzero__()) {
                frame.getlocal(0).__getattr__("sock").invoke("setReuseAddress", frame.getlocal(0).__getattr__("reuse_addr"));
            }
            frame.getlocal(0).__setattr__("istream", frame.getlocal(1).invoke("getInputStream"));
            frame.getlocal(0).__setattr__("ostream", frame.getlocal(1).invoke("getOutputStream"));
            return Py.None;
        }
        
        private static PyObject recv$12(PyFrame frame) {
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("sock"));
            frame.setlocal(3, frame.getglobal("jarray").__getattr__("zeros").__call__(frame.getlocal(1), s$28));
            frame.setlocal(2, frame.getlocal(0).__getattr__("istream").invoke("read", frame.getlocal(3)));
            if (frame.getlocal(2)._le(i$22).__nonzero__()) {
                return s$24;
            }
            if (frame.getlocal(2)._lt(frame.getlocal(1)).__nonzero__()) {
                frame.setlocal(3, frame.getlocal(3).__getslice__(null, frame.getlocal(2), null));
            }
            return frame.getlocal(3).invoke("tostring");
        }
        
        private static PyObject send$13(PyFrame frame) {
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("sock"));
            frame.setlocal(2, frame.getglobal("len").__call__(frame.getlocal(1)));
            frame.getlocal(0).__getattr__("ostream").invoke("write", frame.getlocal(1));
            return frame.getlocal(2);
        }
        
        private static PyObject getsockname$14(PyFrame frame) {
            // Temporary Variables
            PyObject[] t$0$PyObject__;
            PyObject t$0$PyObject;
            
            // Code
            if (frame.getlocal(0).__getattr__("sock").__not__().__nonzero__()) {
                t$0$PyObject__ = org.python.core.Py.unpackSequence((t$0$PyObject = frame.getlocal(0).__getattr__("addr")).__nonzero__() ? t$0$PyObject : new PyTuple(new PyObject[] {s$24, i$22}), 2);
                frame.setlocal(2, t$0$PyObject__[0]);
                frame.setlocal(1, t$0$PyObject__[1]);
                frame.setlocal(2, frame.getglobal("java").__getattr__("net").__getattr__("InetAddress").__getattr__("getByName").__call__(frame.getlocal(2)).invoke("getHostAddress"));
            }
            else {
                if (frame.getlocal(0).__getattr__("server").__nonzero__()) {
                    frame.setlocal(2, frame.getlocal(0).__getattr__("sock").invoke("getInetAddress").invoke("getHostAddress"));
                }
                else {
                    frame.setlocal(2, frame.getlocal(0).__getattr__("sock").invoke("getLocalAddress").invoke("getHostAddress"));
                }
                frame.setlocal(1, frame.getlocal(0).__getattr__("sock").invoke("getLocalPort"));
            }
            return new PyTuple(new PyObject[] {frame.getlocal(2), frame.getlocal(1)});
        }
        
        private static PyObject getpeername$15(PyFrame frame) {
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("sock"));
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("server").__not__());
            frame.setlocal(2, frame.getlocal(0).__getattr__("sock").invoke("getInetAddress").invoke("getHostAddress"));
            frame.setlocal(1, frame.getlocal(0).__getattr__("sock").invoke("getPort"));
            return new PyTuple(new PyObject[] {frame.getlocal(2), frame.getlocal(1)});
        }
        
        private static PyObject setsockopt$16(PyFrame frame) {
            if (frame.getlocal(2)._eq(frame.getglobal("SO_REUSEADDR")).__nonzero__()) {
                frame.getlocal(0).__setattr__("reuse_addr", frame.getlocal(3));
            }
            return Py.None;
        }
        
        private static PyObject getsockopt$17(PyFrame frame) {
            if (frame.getlocal(2)._eq(frame.getglobal("SO_REUSEADDR")).__nonzero__()) {
                return frame.getlocal(0).__getattr__("reuse_addr");
            }
            return Py.None;
        }
        
        private static PyObject makefile$18(PyFrame frame) {
            frame.setlocal(3, frame.getglobal("None"));
            if (frame.getlocal(0).__getattr__("istream").__nonzero__()) {
                if (frame.getlocal(0).__getattr__("ostream").__nonzero__()) {
                    frame.setlocal(3, frame.getglobal("org").__getattr__("python").__getattr__("core").__getattr__("PyFile").__call__(new PyObject[] {frame.getlocal(0).__getattr__("istream"), frame.getlocal(0).__getattr__("ostream"), s$29, frame.getlocal(1)}));
                }
                else {
                    frame.setlocal(3, frame.getglobal("org").__getattr__("python").__getattr__("core").__getattr__("PyFile").__call__(frame.getlocal(0).__getattr__("istream"), s$29, frame.getlocal(1)));
                }
            }
            else if (frame.getlocal(0).__getattr__("ostream").__nonzero__()) {
                frame.setlocal(3, frame.getglobal("org").__getattr__("python").__getattr__("core").__getattr__("PyFile").__call__(frame.getlocal(0).__getattr__("ostream"), s$29, frame.getlocal(1)));
            }
            else {
                throw Py.makeException(frame.getglobal("IOError"), s$30);
            }
            if (frame.getlocal(3).__nonzero__()) {
                return frame.getglobal("_tcpsocket").invoke("FileWrapper", frame.getlocal(0), frame.getlocal(3));
            }
            return Py.None;
        }
        
        private static PyObject __init__$19(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject, t$1$PyObject, t$2$PyObject;
            
            // Code
            frame.getlocal(0).__setattr__("socket", frame.getlocal(1));
            frame.getlocal(0).__setattr__("sock", frame.getlocal(1).__getattr__("sock"));
            frame.getlocal(0).__setattr__("istream", frame.getlocal(1).__getattr__("istream"));
            frame.getlocal(0).__setattr__("ostream", frame.getlocal(1).__getattr__("ostream"));
            frame.getlocal(0).__setattr__("file", frame.getlocal(2));
            frame.getlocal(0).__setattr__("read", frame.getlocal(2).__getattr__("read"));
            frame.getlocal(0).__setattr__("readline", frame.getlocal(2).__getattr__("readline"));
            frame.getlocal(0).__setattr__("readlines", frame.getlocal(2).__getattr__("readlines"));
            frame.getlocal(0).__setattr__("write", frame.getlocal(2).__getattr__("write"));
            frame.getlocal(0).__setattr__("writelines", frame.getlocal(2).__getattr__("writelines"));
            frame.getlocal(0).__setattr__("flush", frame.getlocal(2).__getattr__("flush"));
            frame.getlocal(0).__setattr__("seek", frame.getlocal(2).__getattr__("seek"));
            frame.getlocal(0).__setattr__("tell", frame.getlocal(2).__getattr__("tell"));
            t$0$PyObject = i$15;
            t$1$PyObject = frame.getlocal(0);
            t$2$PyObject = t$1$PyObject.__getattr__("socket");
            t$2$PyObject.__setattr__("file_count", t$2$PyObject.__getattr__("file_count").__iadd__(t$0$PyObject));
            return Py.None;
        }
        
        private static PyObject close$20(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject, t$1$PyObject, t$2$PyObject;
            
            // Code
            if (frame.getlocal(0).__getattr__("file").__getattr__("closed").__nonzero__()) {
                return Py.None;
            }
            t$0$PyObject = i$15;
            t$1$PyObject = frame.getlocal(0);
            t$2$PyObject = t$1$PyObject.__getattr__("socket");
            t$2$PyObject.__setattr__("file_count", t$2$PyObject.__getattr__("file_count").__isub__(t$0$PyObject));
            frame.getlocal(0).__getattr__("file").invoke("close");
            if (((t$0$PyObject = frame.getlocal(0).__getattr__("socket").__getattr__("file_count")._eq(i$22)).__nonzero__() ? frame.getlocal(0).__getattr__("socket").__getattr__("sock")._eq(i$22) : t$0$PyObject).__nonzero__()) {
                if (frame.getlocal(0).__getattr__("sock").__nonzero__()) {
                    frame.getlocal(0).__getattr__("sock").invoke("close");
                }
                if (frame.getlocal(0).__getattr__("istream").__nonzero__()) {
                    frame.getlocal(0).__getattr__("istream").invoke("close");
                }
                if (frame.getlocal(0).__getattr__("ostream").__nonzero__()) {
                    frame.getlocal(0).__getattr__("ostream").invoke("close");
                }
            }
            return Py.None;
        }
        
        private static PyObject FileWrapper$21(PyFrame frame) {
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {}, c$18___init__));
            frame.setlocal("close", new PyFunction(frame.f_globals, new PyObject[] {}, c$19_close));
            return frame.getf_locals();
        }
        
        private static PyObject shutdown$22(PyFrame frame) {
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(1)._in(new PyTuple(new PyObject[] {i$22, i$15, i$14})));
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("sock"));
            if (frame.getlocal(1)._in(new PyTuple(new PyObject[] {i$22, i$14})).__nonzero__()) {
                frame.getlocal(0).__setattr__("istream", frame.getglobal("None"));
            }
            if (frame.getlocal(1)._in(new PyTuple(new PyObject[] {i$15, i$14})).__nonzero__()) {
                frame.getlocal(0).__setattr__("ostream", frame.getglobal("None"));
            }
            return Py.None;
        }
        
        private static PyObject close$23(PyFrame frame) {
            frame.setlocal(2, frame.getlocal(0).__getattr__("sock"));
            frame.setlocal(3, frame.getlocal(0).__getattr__("istream"));
            frame.setlocal(1, frame.getlocal(0).__getattr__("ostream"));
            frame.getlocal(0).__setattr__("sock", i$22);
            frame.getlocal(0).__setattr__("istream", i$22);
            frame.getlocal(0).__setattr__("ostream", i$22);
            if (frame.getlocal(0).__getattr__("file_count")._eq(i$22).__nonzero__()) {
                if (frame.getlocal(3).__nonzero__()) {
                    frame.getlocal(3).invoke("close");
                }
                if (frame.getlocal(1).__nonzero__()) {
                    frame.getlocal(1).invoke("close");
                }
                if (frame.getlocal(2).__nonzero__()) {
                    frame.getlocal(2).invoke("close");
                }
            }
            return Py.None;
        }
        
        private static PyObject _tcpsocket$24(PyFrame frame) {
            frame.setlocal("sock", frame.getname("None"));
            frame.setlocal("istream", frame.getname("None"));
            frame.setlocal("ostream", frame.getname("None"));
            frame.setlocal("addr", frame.getname("None"));
            frame.setlocal("server", i$22);
            frame.setlocal("file_count", i$22);
            frame.setlocal("reuse_addr", i$22);
            frame.setlocal("bind", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$6_bind));
            frame.setlocal("listen", new PyFunction(frame.f_globals, new PyObject[] {i$26}, c$7_listen));
            frame.setlocal("accept", new PyFunction(frame.f_globals, new PyObject[] {}, c$8_accept));
            frame.setlocal("connect", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$9_connect));
            frame.setlocal("_setup", new PyFunction(frame.f_globals, new PyObject[] {}, c$10__setup));
            frame.setlocal("recv", new PyFunction(frame.f_globals, new PyObject[] {}, c$11_recv));
            frame.setlocal("send", new PyFunction(frame.f_globals, new PyObject[] {}, c$12_send));
            frame.setlocal("getsockname", new PyFunction(frame.f_globals, new PyObject[] {}, c$13_getsockname));
            frame.setlocal("getpeername", new PyFunction(frame.f_globals, new PyObject[] {}, c$14_getpeername));
            frame.setlocal("setsockopt", new PyFunction(frame.f_globals, new PyObject[] {}, c$15_setsockopt));
            frame.setlocal("getsockopt", new PyFunction(frame.f_globals, new PyObject[] {}, c$16_getsockopt));
            frame.setlocal("makefile", new PyFunction(frame.f_globals, new PyObject[] {s$31, i$15.__neg__()}, c$17_makefile));
            frame.setlocal("FileWrapper", Py.makeClass("FileWrapper", new PyObject[] {}, c$20_FileWrapper, null));
            frame.setlocal("shutdown", new PyFunction(frame.f_globals, new PyObject[] {}, c$21_shutdown));
            frame.setlocal("close", new PyFunction(frame.f_globals, new PyObject[] {}, c$22_close));
            return frame.getf_locals();
        }
        
        private static PyObject __init__$25(PyFrame frame) {
            frame.getlocal(0).__setattr__("sock", frame.getglobal("None"));
            frame.getlocal(0).__setattr__("addr", frame.getglobal("None"));
            return Py.None;
        }
        
        private static PyObject bind$26(PyFrame frame) {
            // Temporary Variables
            PyObject[] t$0$PyObject__;
            
            // Code
            if (frame.getlocal(2)._isnot(frame.getglobal("None")).__nonzero__()) {
                frame.setlocal(1, new PyTuple(new PyObject[] {frame.getlocal(1), frame.getlocal(2)}));
            }
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("sock").__not__());
            t$0$PyObject__ = org.python.core.Py.unpackSequence(frame.getlocal(1), 2);
            frame.setlocal(4, t$0$PyObject__[0]);
            frame.setlocal(2, t$0$PyObject__[1]);
            if (frame.getlocal(4)._eq(s$24).__nonzero__()) {
                frame.getlocal(0).__setattr__("sock", frame.getglobal("java").__getattr__("net").__getattr__("DatagramSocket").__call__(frame.getlocal(2)));
            }
            else {
                frame.setlocal(3, frame.getglobal("java").__getattr__("net").__getattr__("InetAddress").__getattr__("getByName").__call__(frame.getlocal(4)));
                frame.getlocal(0).__setattr__("sock", frame.getglobal("java").__getattr__("net").__getattr__("DatagramSocket").__call__(frame.getlocal(2), frame.getlocal(3)));
            }
            return Py.None;
        }
        
        private static PyObject connect$27(PyFrame frame) {
            // Temporary Variables
            PyObject[] t$0$PyObject__;
            
            // Code
            if (frame.getlocal(2)._isnot(frame.getglobal("None")).__nonzero__()) {
                frame.setlocal(1, new PyTuple(new PyObject[] {frame.getlocal(1), frame.getlocal(2)}));
            }
            t$0$PyObject__ = org.python.core.Py.unpackSequence(frame.getlocal(1), 2);
            frame.setlocal(3, t$0$PyObject__[0]);
            frame.setlocal(2, t$0$PyObject__[1]);
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("addr").__not__());
            if (frame.getlocal(0).__getattr__("sock").__not__().__nonzero__()) {
                frame.getlocal(0).__setattr__("sock", frame.getglobal("java").__getattr__("net").__getattr__("DatagramSocket").__call__());
            }
            frame.getlocal(0).__setattr__("addr", frame.getlocal(1));
            return Py.None;
        }
        
        private static PyObject sendto$28(PyFrame frame) {
            // Temporary Variables
            PyObject[] t$0$PyObject__;
            
            // Code
            frame.setlocal(4, frame.getglobal("len").__call__(frame.getlocal(1)));
            if (frame.getlocal(0).__getattr__("sock").__not__().__nonzero__()) {
                frame.getlocal(0).__setattr__("sock", frame.getglobal("java").__getattr__("net").__getattr__("DatagramSocket").__call__());
            }
            t$0$PyObject__ = org.python.core.Py.unpackSequence(frame.getlocal(2), 2);
            frame.setlocal(7, t$0$PyObject__[0]);
            frame.setlocal(5, t$0$PyObject__[1]);
            frame.setlocal(8, frame.getglobal("jarray").__getattr__("array").__call__(frame.getglobal("map").__call__(frame.getglobal("ord"), frame.getlocal(1)), s$28));
            frame.setlocal(6, frame.getglobal("java").__getattr__("net").__getattr__("InetAddress").__getattr__("getByName").__call__(frame.getlocal(7)));
            frame.setlocal(3, frame.getglobal("java").__getattr__("net").__getattr__("DatagramPacket").__call__(new PyObject[] {frame.getlocal(8), frame.getlocal(4), frame.getlocal(6), frame.getlocal(5)}));
            frame.getlocal(0).__getattr__("sock").invoke("send", frame.getlocal(3));
            return frame.getlocal(4);
        }
        
        private static PyObject send$29(PyFrame frame) {
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("addr"));
            return frame.getlocal(0).invoke("sendto", frame.getlocal(0).__getattr__("addr"));
        }
        
        private static PyObject recvfrom$30(PyFrame frame) {
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("sock"));
            frame.setlocal(6, frame.getglobal("jarray").__getattr__("zeros").__call__(frame.getlocal(1), s$28));
            frame.setlocal(2, frame.getglobal("java").__getattr__("net").__getattr__("DatagramPacket").__call__(frame.getlocal(6), frame.getlocal(1)));
            frame.getlocal(0).__getattr__("sock").invoke("receive", frame.getlocal(2));
            frame.setlocal(5, frame.getlocal(2).invoke("getAddress").invoke("getHostName"));
            frame.setlocal(3, frame.getlocal(2).invoke("getPort"));
            frame.setlocal(4, frame.getlocal(2).invoke("getLength"));
            if (frame.getlocal(4)._lt(frame.getlocal(1)).__nonzero__()) {
                frame.setlocal(6, frame.getlocal(6).__getslice__(null, frame.getlocal(4), null));
            }
            return new PyTuple(new PyObject[] {frame.getlocal(6).invoke("tostring"), new PyTuple(new PyObject[] {frame.getlocal(5), frame.getlocal(3)})});
        }
        
        private static PyObject recv$31(PyFrame frame) {
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("sock"));
            frame.setlocal(3, frame.getglobal("jarray").__getattr__("zeros").__call__(frame.getlocal(1), s$28));
            frame.setlocal(4, frame.getglobal("java").__getattr__("net").__getattr__("DatagramPacket").__call__(frame.getlocal(3), frame.getlocal(1)));
            frame.getlocal(0).__getattr__("sock").invoke("receive", frame.getlocal(4));
            frame.setlocal(2, frame.getlocal(4).invoke("getLength"));
            if (frame.getlocal(2)._lt(frame.getlocal(1)).__nonzero__()) {
                frame.setlocal(3, frame.getlocal(3).__getslice__(null, frame.getlocal(2), null));
            }
            return frame.getlocal(3).invoke("tostring");
        }
        
        private static PyObject getsockname$32(PyFrame frame) {
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("sock"));
            frame.setlocal(2, frame.getlocal(0).__getattr__("sock").invoke("getLocalAddress").invoke("getHostName"));
            frame.setlocal(1, frame.getlocal(0).__getattr__("sock").invoke("getLocalPort"));
            return new PyTuple(new PyObject[] {frame.getlocal(2), frame.getlocal(1)});
        }
        
        private static PyObject getpeername$33(PyFrame frame) {
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("sock"));
            frame.setlocal(2, frame.getlocal(0).__getattr__("sock").invoke("getInetAddress").invoke("getHostName"));
            frame.setlocal(1, frame.getlocal(0).__getattr__("sock").invoke("getPort"));
            return new PyTuple(new PyObject[] {frame.getlocal(2), frame.getlocal(1)});
        }
        
        private static PyObject __del__$34(PyFrame frame) {
            frame.getlocal(0).invoke("close");
            return Py.None;
        }
        
        private static PyObject close$35(PyFrame frame) {
            frame.setlocal(1, frame.getlocal(0).__getattr__("sock"));
            frame.getlocal(0).__setattr__("sock", i$22);
            frame.getlocal(1).invoke("close");
            return Py.None;
        }
        
        private static PyObject _udpsocket$36(PyFrame frame) {
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {}, c$24___init__));
            frame.setlocal("bind", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$25_bind));
            frame.setlocal("connect", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$26_connect));
            frame.setlocal("sendto", new PyFunction(frame.f_globals, new PyObject[] {}, c$27_sendto));
            frame.setlocal("send", new PyFunction(frame.f_globals, new PyObject[] {}, c$28_send));
            frame.setlocal("recvfrom", new PyFunction(frame.f_globals, new PyObject[] {}, c$29_recvfrom));
            frame.setlocal("recv", new PyFunction(frame.f_globals, new PyObject[] {}, c$30_recv));
            frame.setlocal("getsockname", new PyFunction(frame.f_globals, new PyObject[] {}, c$31_getsockname));
            frame.setlocal("getpeername", new PyFunction(frame.f_globals, new PyObject[] {}, c$32_getpeername));
            frame.setlocal("__del__", new PyFunction(frame.f_globals, new PyObject[] {}, c$33___del__));
            frame.setlocal("close", new PyFunction(frame.f_globals, new PyObject[] {}, c$34_close));
            return frame.getf_locals();
        }
        
        private static PyObject test$37(PyFrame frame) {
            frame.setlocal(0, frame.getglobal("socket").__call__(frame.getglobal("AF_INET"), frame.getglobal("SOCK_STREAM")));
            frame.getlocal(0).invoke("connect", new PyTuple(new PyObject[] {s$24, i$32}));
            frame.getlocal(0).invoke("send", s$33);
            while (i$15.__nonzero__()) {
                frame.setlocal(1, frame.getlocal(0).invoke("recv", i$34));
                Py.println(frame.getlocal(1));
                if (frame.getlocal(1).__not__().__nonzero__()) {
                    break;
                }
            }
            return Py.None;
        }
        
        private static PyObject main$38(PyFrame frame) {
            frame.setglobal("__file__", s$36);
            
            /* Preliminary socket module.
            
            XXX Restrictions:
            
            - Only INET sockets
            - No asynchronous behavior
            - No socket options
            - Can't do a very good gethostbyaddr() right...
            
             */
            frame.setlocal("java", org.python.core.imp.importOne("java.net", frame));
            frame.setlocal("org", org.python.core.imp.importOne("org.python.core", frame));
            frame.setlocal("jarray", org.python.core.imp.importOne("jarray", frame));
            frame.setlocal("string", org.python.core.imp.importOne("string", frame));
            frame.setlocal("__all__", new PyList(new PyObject[] {s$1, s$2, s$3, s$4, s$5, s$6, s$7, s$8, s$9, s$10, s$11, s$12, s$13}));
            frame.setlocal("error", frame.getname("IOError"));
            frame.setlocal("AF_INET", i$14);
            frame.setlocal("SOCK_DGRAM", i$15);
            frame.setlocal("SOCK_STREAM", i$14);
            frame.setlocal("SOCK_RAW", i$16);
            frame.setlocal("SOCK_RDM", i$17);
            frame.setlocal("SOCK_SEQPACKET", i$18);
            frame.setlocal("SOL_SOCKET", i$19);
            frame.setlocal("SO_REUSEADDR", i$17);
            frame.setlocal("_gethostbyaddr", new PyFunction(frame.f_globals, new PyObject[] {}, c$0__gethostbyaddr));
            frame.setlocal("getfqdn", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$1_getfqdn));
            frame.setlocal("gethostname", new PyFunction(frame.f_globals, new PyObject[] {}, c$2_gethostname));
            frame.setlocal("gethostbyname", new PyFunction(frame.f_globals, new PyObject[] {}, c$3_gethostbyname));
            frame.setlocal("gethostbyaddr", new PyFunction(frame.f_globals, new PyObject[] {}, c$4_gethostbyaddr));
            frame.setlocal("socket", new PyFunction(frame.f_globals, new PyObject[] {i$22}, c$5_socket));
            frame.setlocal("_tcpsocket", Py.makeClass("_tcpsocket", new PyObject[] {}, c$23__tcpsocket, null));
            frame.setlocal("_udpsocket", Py.makeClass("_udpsocket", new PyObject[] {}, c$35__udpsocket, null));
            frame.setlocal("SocketType", frame.getname("_tcpsocket"));
            frame.setlocal("test", new PyFunction(frame.f_globals, new PyObject[] {}, c$36_test));
            if (frame.getname("__name__")._eq(s$35).__nonzero__()) {
                frame.getname("test").__call__();
            }
            return Py.None;
        }
        
    }
    public static void moduleDictInit(PyObject dict) {
        dict.__setitem__("__name__", new PyString("socket"));
        Py.runCode(new _PyInner().getMain(), dict, dict);
    }
    
    public static void main(String[] args) throws java.lang.Exception {
        String[] newargs = new String[args.length+1];
        newargs[0] = "socket";
        System.arraycopy(args, 0, newargs, 1, args.length);
        Py.runMain(socket._PyInner.class, newargs, socket.jpy$packages, socket.jpy$mainProperties, "", new String[] {"string", "random", "util", "traceback", "sre_compile", "atexit", "sre", "sre_constants", "StringIO", "javaos", "socket", "yapm", "calendar", "repr", "copy_reg", "SocketServer", "server", "re", "linecache", "javapath", "UserDict", "copy", "threading", "stat", "PathVFS", "sre_parse"});
    }
    
}
