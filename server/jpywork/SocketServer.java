import org.python.core.*;

public class SocketServer extends java.lang.Object {
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
        private static PyObject i$22;
        private static PyObject s$23;
        private static PyObject s$24;
        private static PyObject s$25;
        private static PyObject s$26;
        private static PyObject s$27;
        private static PyObject s$28;
        private static PyObject s$29;
        private static PyObject s$30;
        private static PyObject i$31;
        private static PyObject s$32;
        private static PyObject s$33;
        private static PyObject i$34;
        private static PyObject i$35;
        private static PyObject s$36;
        private static PyObject s$37;
        private static PyObject s$38;
        private static PyObject s$39;
        private static PyObject i$40;
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
        private static PyFunctionTable funcTable;
        private static PyCode c$0___init__;
        private static PyCode c$1_server_activate;
        private static PyCode c$2_serve_forever;
        private static PyCode c$3_handle_request;
        private static PyCode c$4_verify_request;
        private static PyCode c$5_process_request;
        private static PyCode c$6_server_close;
        private static PyCode c$7_finish_request;
        private static PyCode c$8_close_request;
        private static PyCode c$9_handle_error;
        private static PyCode c$10_BaseServer;
        private static PyCode c$11___init__;
        private static PyCode c$12_server_bind;
        private static PyCode c$13_server_activate;
        private static PyCode c$14_server_close;
        private static PyCode c$15_fileno;
        private static PyCode c$16_get_request;
        private static PyCode c$17_close_request;
        private static PyCode c$18_TCPServer;
        private static PyCode c$19_get_request;
        private static PyCode c$20_server_activate;
        private static PyCode c$21_close_request;
        private static PyCode c$22_UDPServer;
        private static PyCode c$23_collect_children;
        private static PyCode c$24_process_request;
        private static PyCode c$25_ForkingMixIn;
        private static PyCode c$26_process_request;
        private static PyCode c$27_ThreadingMixIn;
        private static PyCode c$28_ForkingUDPServer;
        private static PyCode c$29_ForkingTCPServer;
        private static PyCode c$30_ThreadingUDPServer;
        private static PyCode c$31_ThreadingTCPServer;
        private static PyCode c$32_UnixStreamServer;
        private static PyCode c$33_UnixDatagramServer;
        private static PyCode c$34_ThreadingUnixStreamServer;
        private static PyCode c$35_ThreadingUnixDatagramServer;
        private static PyCode c$36___init__;
        private static PyCode c$37_setup;
        private static PyCode c$38___del__;
        private static PyCode c$39_handle;
        private static PyCode c$40_finish;
        private static PyCode c$41_BaseRequestHandler;
        private static PyCode c$42_setup;
        private static PyCode c$43_finish;
        private static PyCode c$44_StreamRequestHandler;
        private static PyCode c$45_setup;
        private static PyCode c$46_finish;
        private static PyCode c$47_DatagramRequestHandler;
        private static PyCode c$48_main;
        private static void initConstants() {
            s$0 = Py.newString("Generic socket server classes.\012\012This module tries to capture the various aspects of defining a server:\012\012For socket-based servers:\012\012- address family:\012        - AF_INET: IP (Internet Protocol) sockets (default)\012        - AF_UNIX: Unix domain sockets\012        - others, e.g. AF_DECNET are conceivable (see <socket.h>\012- socket type:\012        - SOCK_STREAM (reliable stream, e.g. TCP)\012        - SOCK_DGRAM (datagrams, e.g. UDP)\012\012For request-based servers (including socket-based):\012\012- client address verification before further looking at the request\012        (This is actually a hook for any processing that needs to look\012         at the request before anything else, e.g. logging)\012- how to handle multiple requests:\012        - synchronous (one request is handled at a time)\012        - forking (each request is handled by a new process)\012        - threading (each request is handled by a new thread)\012\012The classes in this module favor the server type that is simplest to\012write: a synchronous TCP/IP server.  This is bad class design, but\012save some typing.  (There's also the issue that a deep class hierarchy\012slows down method lookups.)\012\012There are five classes in an inheritance diagram, four of which represent\012synchronous servers of four types:\012\012        +------------+\012        | BaseServer |\012        +------------+\012              |\012              v\012        +-----------+        +------------------+\012        | TCPServer |------->| UnixStreamServer |\012        +-----------+        +------------------+\012              |\012              v\012        +-----------+        +--------------------+\012        | UDPServer |------->| UnixDatagramServer |\012        +-----------+        +--------------------+\012\012Note that UnixDatagramServer derives from UDPServer, not from\012UnixStreamServer -- the only difference between an IP and a Unix\012stream server is the address family, which is simply repeated in both\012unix server classes.\012\012Forking and threading versions of each type of server can be created\012using the ForkingServer and ThreadingServer mix-in classes.  For\012instance, a threading UDP server class is created as follows:\012\012        class ThreadingUDPServer(ThreadingMixIn, UDPServer): pass\012\012The Mix-in class must come first, since it overrides a method defined\012in UDPServer!\012\012To implement a service, you must derive a class from\012BaseRequestHandler and redefine its handle() method.  You can then run\012various versions of the service by combining one of the server classes\012with your request handler class.\012\012The request handler class must be different for datagram or stream\012services.  This can be hidden by using the mix-in request handler\012classes StreamRequestHandler or DatagramRequestHandler.\012\012Of course, you still have to use your head!\012\012For instance, it makes no sense to use a forking server if the service\012contains state in memory that can be modified by requests (since the\012modifications in the child process would never reach the initial state\012kept in the parent process and passed to each child).  In this case,\012you can use a threading server, but you will probably have to use\012locks to avoid two requests that come in nearly simultaneous to apply\012conflicting changes to the server state.\012\012On the other hand, if you are building e.g. an HTTP server, where all\012data is stored externally (e.g. in the file system), a synchronous\012class will essentially render the service \"deaf\" while one request is\012being handled -- which may be for a very long time if a client is slow\012to reqd all the data it has requested.  Here a threading or forking\012server is appropriate.\012\012In some cases, it may be appropriate to process part of a request\012synchronously, but to finish processing in a forked child depending on\012the request data.  This can be implemented by using a synchronous\012server and doing an explicit fork in the request handler class\012handle() method.\012\012Another approach to handling multiple simultaneous requests in an\012environment that supports neither threads nor fork (or where these are\012too expensive or inappropriate for the service) is to maintain an\012explicit table of partially finished requests and to use select() to\012decide which request to work on next (or whether to handle a new\012incoming request).  This is particularly important for stream services\012where each client can potentially be connected for a long time (if\012threads or subprocesses cannot be used).\012\012Future work:\012- Standard classes for Sun RPC (which uses either UDP or TCP)\012- Standard mix-in classes to implement various authentication\012  and encryption schemes\012- Standard framework for select-based multiplexing\012\012XXX Open problems:\012- What to do with out-of-band data?\012\012BaseServer:\012- split generic \"request\" functionality out into BaseServer class.\012  Copyright (C) 2000  Luke Kenneth Casson Leighton <lkcl@samba.org>\012\012  example: read entries from a SQL database (requires overriding\012  get_request() to return a table entry from the database).\012  entry is processed by a RequestHandlerClass.\012\012");
            s$1 = Py.newString("0.4");
            s$2 = Py.newString("TCPServer");
            s$3 = Py.newString("UDPServer");
            s$4 = Py.newString("ForkingUDPServer");
            s$5 = Py.newString("ForkingTCPServer");
            s$6 = Py.newString("ThreadingUDPServer");
            s$7 = Py.newString("ThreadingTCPServer");
            s$8 = Py.newString("BaseRequestHandler");
            s$9 = Py.newString("StreamRequestHandler");
            s$10 = Py.newString("DatagramRequestHandler");
            s$11 = Py.newString("ThreadingMixIn");
            s$12 = Py.newString("ForkingMixIn");
            s$13 = Py.newString("AF_UNIX");
            s$14 = Py.newString("UnixStreamServer");
            s$15 = Py.newString("UnixDatagramServer");
            s$16 = Py.newString("ThreadingUnixStreamServer");
            s$17 = Py.newString("ThreadingUnixDatagramServer");
            s$18 = Py.newString("Base class for server classes.\012\012    Methods for the caller:\012\012    - __init__(server_address, RequestHandlerClass)\012    - serve_forever()\012    - handle_request()  # if you do not use serve_forever()\012    - fileno() -> int   # for select()\012\012    Methods that may be overridden:\012\012    - server_bind()\012    - server_activate()\012    - get_request() -> request, client_address\012    - verify_request(request, client_address)\012    - server_close()\012    - process_request(request, client_address)\012    - close_request(request)\012    - handle_error()\012\012    Methods for derived classes:\012\012    - finish_request(request, client_address)\012\012    Class variables that may be overridden by derived classes or\012    instances:\012\012    - address_family\012    - socket_type\012    - reuse_address\012\012    Instance variables:\012\012    - RequestHandlerClass\012    - socket\012\012    ");
            s$19 = Py.newString("Constructor.  May be extended, do not override.");
            s$20 = Py.newString("Called by constructor to activate the server.\012\012        May be overridden.\012\012        ");
            s$21 = Py.newString("Handle one request at a time until doomsday.");
            i$22 = Py.newInteger(1);
            s$23 = Py.newString("Handle one request, possibly blocking.");
            s$24 = Py.newString("Verify the request.  May be overridden.\012\012        Return true if we should proceed with this request.\012\012        ");
            s$25 = Py.newString("Call finish_request.\012\012        Overridden by ForkingMixIn and ThreadingMixIn.\012\012        ");
            s$26 = Py.newString("Called to clean-up the server.\012\012        May be overridden.\012\012        ");
            s$27 = Py.newString("Finish one request by instantiating RequestHandlerClass.");
            s$28 = Py.newString("Called to clean up an individual request.");
            s$29 = Py.newString("Handle an error gracefully.  May be overridden.\012\012        The default is to print a traceback and continue.\012\012        ");
            s$30 = Py.newString("-");
            i$31 = Py.newInteger(40);
            s$32 = Py.newString("Exception happened during processing of request from");
            s$33 = Py.newString("Base class for various socket-based server classes.\012\012    Defaults to synchronous IP stream (i.e., TCP).\012\012    Methods for the caller:\012\012    - __init__(server_address, RequestHandlerClass)\012    - serve_forever()\012    - handle_request()  # if you don't use serve_forever()\012    - fileno() -> int   # for select()\012\012    Methods that may be overridden:\012\012    - server_bind()\012    - server_activate()\012    - get_request() -> request, client_address\012    - verify_request(request, client_address)\012    - process_request(request, client_address)\012    - close_request(request)\012    - handle_error()\012\012    Methods for derived classes:\012\012    - finish_request(request, client_address)\012\012    Class variables that may be overridden by derived classes or\012    instances:\012\012    - address_family\012    - socket_type\012    - request_queue_size (only for stream sockets)\012    - reuse_address\012\012    Instance variables:\012\012    - server_address\012    - RequestHandlerClass\012    - socket\012\012    ");
            i$34 = Py.newInteger(5);
            i$35 = Py.newInteger(0);
            s$36 = Py.newString("Called by constructor to bind the socket.\012\012        May be overridden.\012\012        ");
            s$37 = Py.newString("Return socket file number.\012\012        Interface required by select().\012\012        ");
            s$38 = Py.newString("Get the request and client address from the socket.\012\012        May be overridden.\012\012        ");
            s$39 = Py.newString("UDP server class.");
            i$40 = Py.newInteger(8192);
            s$41 = Py.newString("Mix-in class to handle each request in a new process.");
            s$42 = Py.newString("Internal routine to wait for died children.");
            s$43 = Py.newString("Fork a new subprocess to process the request.");
            s$44 = Py.newString("Mix-in class to handle each request in a new thread.");
            s$45 = Py.newString("Start a new thread to process the request.");
            s$46 = Py.newString("Base class for request handler classes.\012\012    This class is instantiated for each request to be handled.  The\012    constructor sets the instance variables request, client_address\012    and server, and then calls the handle() method.  To implement a\012    specific service, all you need to do is to derive a class which\012    defines a handle() method.\012\012    The handle() method can find the request as self.request, the\012    client address as self.client_address, and the server (in case it\012    needs access to per-server information) as self.server.  Since a\012    separate instance is created for each request, the handle() method\012    can define arbitrary other instance variariables.\012\012    ");
            s$47 = Py.newString("Define self.rfile and self.wfile for stream sockets.");
            s$48 = Py.newString("rb");
            s$49 = Py.newString("wb");
            s$50 = Py.newString("Define self.rfile and self.wfile for datagram sockets.");
            s$51 = Py.newString("/usr/share/jython/Lib-cpython/SocketServer.py");
            funcTable = new _PyInner();
            c$0___init__ = Py.newCode(3, new String[] {"self", "server_address", "RequestHandlerClass"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "__init__", false, false, funcTable, 0, null, null, 0, 1);
            c$1_server_activate = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "server_activate", false, false, funcTable, 1, null, null, 0, 1);
            c$2_serve_forever = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "serve_forever", false, false, funcTable, 2, null, null, 0, 1);
            c$3_handle_request = Py.newCode(1, new String[] {"self", "client_address", "request"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "handle_request", false, false, funcTable, 3, null, null, 0, 1);
            c$4_verify_request = Py.newCode(3, new String[] {"self", "request", "client_address"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "verify_request", false, false, funcTable, 4, null, null, 0, 1);
            c$5_process_request = Py.newCode(3, new String[] {"self", "request", "client_address"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "process_request", false, false, funcTable, 5, null, null, 0, 1);
            c$6_server_close = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "server_close", false, false, funcTable, 6, null, null, 0, 1);
            c$7_finish_request = Py.newCode(3, new String[] {"self", "request", "client_address"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "finish_request", false, false, funcTable, 7, null, null, 0, 1);
            c$8_close_request = Py.newCode(2, new String[] {"self", "request"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "close_request", false, false, funcTable, 8, null, null, 0, 1);
            c$9_handle_error = Py.newCode(3, new String[] {"self", "request", "client_address", "traceback"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "handle_error", false, false, funcTable, 9, null, null, 0, 1);
            c$10_BaseServer = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/SocketServer.py", "BaseServer", false, false, funcTable, 10, null, null, 0, 0);
            c$11___init__ = Py.newCode(3, new String[] {"self", "server_address", "RequestHandlerClass"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "__init__", false, false, funcTable, 11, null, null, 0, 1);
            c$12_server_bind = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "server_bind", false, false, funcTable, 12, null, null, 0, 1);
            c$13_server_activate = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "server_activate", false, false, funcTable, 13, null, null, 0, 1);
            c$14_server_close = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "server_close", false, false, funcTable, 14, null, null, 0, 1);
            c$15_fileno = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "fileno", false, false, funcTable, 15, null, null, 0, 1);
            c$16_get_request = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "get_request", false, false, funcTable, 16, null, null, 0, 1);
            c$17_close_request = Py.newCode(2, new String[] {"self", "request"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "close_request", false, false, funcTable, 17, null, null, 0, 1);
            c$18_TCPServer = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/SocketServer.py", "TCPServer", false, false, funcTable, 18, null, null, 0, 0);
            c$19_get_request = Py.newCode(1, new String[] {"self", "client_addr", "data"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "get_request", false, false, funcTable, 19, null, null, 0, 1);
            c$20_server_activate = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "server_activate", false, false, funcTable, 20, null, null, 0, 1);
            c$21_close_request = Py.newCode(2, new String[] {"self", "request"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "close_request", false, false, funcTable, 21, null, null, 0, 1);
            c$22_UDPServer = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/SocketServer.py", "UDPServer", false, false, funcTable, 22, null, null, 0, 0);
            c$23_collect_children = Py.newCode(1, new String[] {"self", "status", "pid", "options"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "collect_children", false, false, funcTable, 23, null, null, 0, 1);
            c$24_process_request = Py.newCode(3, new String[] {"self", "request", "client_address", "pid"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "process_request", false, false, funcTable, 24, null, null, 0, 1);
            c$25_ForkingMixIn = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/SocketServer.py", "ForkingMixIn", false, false, funcTable, 25, null, null, 0, 0);
            c$26_process_request = Py.newCode(3, new String[] {"self", "request", "client_address", "t", "threading"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "process_request", false, false, funcTable, 26, null, null, 0, 1);
            c$27_ThreadingMixIn = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/SocketServer.py", "ThreadingMixIn", false, false, funcTable, 27, null, null, 0, 0);
            c$28_ForkingUDPServer = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/SocketServer.py", "ForkingUDPServer", false, false, funcTable, 28, null, null, 0, 0);
            c$29_ForkingTCPServer = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/SocketServer.py", "ForkingTCPServer", false, false, funcTable, 29, null, null, 0, 0);
            c$30_ThreadingUDPServer = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/SocketServer.py", "ThreadingUDPServer", false, false, funcTable, 30, null, null, 0, 0);
            c$31_ThreadingTCPServer = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/SocketServer.py", "ThreadingTCPServer", false, false, funcTable, 31, null, null, 0, 0);
            c$32_UnixStreamServer = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/SocketServer.py", "UnixStreamServer", false, false, funcTable, 32, null, null, 0, 0);
            c$33_UnixDatagramServer = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/SocketServer.py", "UnixDatagramServer", false, false, funcTable, 33, null, null, 0, 0);
            c$34_ThreadingUnixStreamServer = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/SocketServer.py", "ThreadingUnixStreamServer", false, false, funcTable, 34, null, null, 0, 0);
            c$35_ThreadingUnixDatagramServer = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/SocketServer.py", "ThreadingUnixDatagramServer", false, false, funcTable, 35, null, null, 0, 0);
            c$36___init__ = Py.newCode(4, new String[] {"self", "request", "client_address", "server"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "__init__", false, false, funcTable, 36, null, null, 0, 1);
            c$37_setup = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "setup", false, false, funcTable, 37, null, null, 0, 1);
            c$38___del__ = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "__del__", false, false, funcTable, 38, null, null, 0, 1);
            c$39_handle = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "handle", false, false, funcTable, 39, null, null, 0, 1);
            c$40_finish = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "finish", false, false, funcTable, 40, null, null, 0, 1);
            c$41_BaseRequestHandler = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/SocketServer.py", "BaseRequestHandler", false, false, funcTable, 41, null, null, 0, 0);
            c$42_setup = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "setup", false, false, funcTable, 42, null, null, 0, 1);
            c$43_finish = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "finish", false, false, funcTable, 43, null, null, 0, 1);
            c$44_StreamRequestHandler = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/SocketServer.py", "StreamRequestHandler", false, false, funcTable, 44, null, null, 0, 0);
            c$45_setup = Py.newCode(1, new String[] {"self", "StringIO"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "setup", false, false, funcTable, 45, null, null, 0, 1);
            c$46_finish = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/SocketServer.py", "finish", false, false, funcTable, 46, null, null, 0, 1);
            c$47_DatagramRequestHandler = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/SocketServer.py", "DatagramRequestHandler", false, false, funcTable, 47, null, null, 0, 0);
            c$48_main = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/SocketServer.py", "main", false, false, funcTable, 48, null, null, 0, 0);
        }
        
        
        public PyCode getMain() {
            if (c$48_main == null) _PyInner.initConstants();
            return c$48_main;
        }
        
        public PyObject call_function(int index, PyFrame frame) {
            switch (index){
                case 0:
                return _PyInner.__init__$1(frame);
                case 1:
                return _PyInner.server_activate$2(frame);
                case 2:
                return _PyInner.serve_forever$3(frame);
                case 3:
                return _PyInner.handle_request$4(frame);
                case 4:
                return _PyInner.verify_request$5(frame);
                case 5:
                return _PyInner.process_request$6(frame);
                case 6:
                return _PyInner.server_close$7(frame);
                case 7:
                return _PyInner.finish_request$8(frame);
                case 8:
                return _PyInner.close_request$9(frame);
                case 9:
                return _PyInner.handle_error$10(frame);
                case 10:
                return _PyInner.BaseServer$11(frame);
                case 11:
                return _PyInner.__init__$12(frame);
                case 12:
                return _PyInner.server_bind$13(frame);
                case 13:
                return _PyInner.server_activate$14(frame);
                case 14:
                return _PyInner.server_close$15(frame);
                case 15:
                return _PyInner.fileno$16(frame);
                case 16:
                return _PyInner.get_request$17(frame);
                case 17:
                return _PyInner.close_request$18(frame);
                case 18:
                return _PyInner.TCPServer$19(frame);
                case 19:
                return _PyInner.get_request$20(frame);
                case 20:
                return _PyInner.server_activate$21(frame);
                case 21:
                return _PyInner.close_request$22(frame);
                case 22:
                return _PyInner.UDPServer$23(frame);
                case 23:
                return _PyInner.collect_children$24(frame);
                case 24:
                return _PyInner.process_request$25(frame);
                case 25:
                return _PyInner.ForkingMixIn$26(frame);
                case 26:
                return _PyInner.process_request$27(frame);
                case 27:
                return _PyInner.ThreadingMixIn$28(frame);
                case 28:
                return _PyInner.ForkingUDPServer$29(frame);
                case 29:
                return _PyInner.ForkingTCPServer$30(frame);
                case 30:
                return _PyInner.ThreadingUDPServer$31(frame);
                case 31:
                return _PyInner.ThreadingTCPServer$32(frame);
                case 32:
                return _PyInner.UnixStreamServer$33(frame);
                case 33:
                return _PyInner.UnixDatagramServer$34(frame);
                case 34:
                return _PyInner.ThreadingUnixStreamServer$35(frame);
                case 35:
                return _PyInner.ThreadingUnixDatagramServer$36(frame);
                case 36:
                return _PyInner.__init__$37(frame);
                case 37:
                return _PyInner.setup$38(frame);
                case 38:
                return _PyInner.__del__$39(frame);
                case 39:
                return _PyInner.handle$40(frame);
                case 40:
                return _PyInner.finish$41(frame);
                case 41:
                return _PyInner.BaseRequestHandler$42(frame);
                case 42:
                return _PyInner.setup$43(frame);
                case 43:
                return _PyInner.finish$44(frame);
                case 44:
                return _PyInner.StreamRequestHandler$45(frame);
                case 45:
                return _PyInner.setup$46(frame);
                case 46:
                return _PyInner.finish$47(frame);
                case 47:
                return _PyInner.DatagramRequestHandler$48(frame);
                case 48:
                return _PyInner.main$49(frame);
                default:
                return null;
            }
        }
        
        private static PyObject __init__$1(PyFrame frame) {
            /* Constructor.  May be extended, do not override. */
            frame.getlocal(0).__setattr__("server_address", frame.getlocal(1));
            frame.getlocal(0).__setattr__("RequestHandlerClass", frame.getlocal(2));
            return Py.None;
        }
        
        private static PyObject server_activate$2(PyFrame frame) {
            /* Called by constructor to activate the server.
            
                    May be overridden.
            
                     */
            // pass
            return Py.None;
        }
        
        private static PyObject serve_forever$3(PyFrame frame) {
            /* Handle one request at a time until doomsday. */
            while (i$22.__nonzero__()) {
                frame.getlocal(0).invoke("handle_request");
            }
            return Py.None;
        }
        
        private static PyObject handle_request$4(PyFrame frame) {
            // Temporary Variables
            PyObject[] t$0$PyObject__;
            PyException t$0$PyException;
            
            // Code
            /* Handle one request, possibly blocking. */
            try {
                t$0$PyObject__ = org.python.core.Py.unpackSequence(frame.getlocal(0).invoke("get_request"), 2);
                frame.setlocal(2, t$0$PyObject__[0]);
                frame.setlocal(1, t$0$PyObject__[1]);
            }
            catch (Throwable x$0) {
                t$0$PyException = Py.setException(x$0, frame);
                if (Py.matchException(t$0$PyException, frame.getglobal("socket").__getattr__("error"))) {
                    return Py.None;
                }
                else throw t$0$PyException;
            }
            if (frame.getlocal(0).invoke("verify_request", frame.getlocal(2), frame.getlocal(1)).__nonzero__()) {
                try {
                    frame.getlocal(0).invoke("process_request", frame.getlocal(2), frame.getlocal(1));
                }
                catch (Throwable x$1) {
                    t$0$PyException = Py.setException(x$1, frame);
                    frame.getlocal(0).invoke("handle_error", frame.getlocal(2), frame.getlocal(1));
                    frame.getlocal(0).invoke("close_request", frame.getlocal(2));
                }
            }
            return Py.None;
        }
        
        private static PyObject verify_request$5(PyFrame frame) {
            /* Verify the request.  May be overridden.
            
                    Return true if we should proceed with this request.
            
                     */
            return i$22;
        }
        
        private static PyObject process_request$6(PyFrame frame) {
            /* Call finish_request.
            
                    Overridden by ForkingMixIn and ThreadingMixIn.
            
                     */
            frame.getlocal(0).invoke("finish_request", frame.getlocal(1), frame.getlocal(2));
            frame.getlocal(0).invoke("close_request", frame.getlocal(1));
            return Py.None;
        }
        
        private static PyObject server_close$7(PyFrame frame) {
            /* Called to clean-up the server.
            
                    May be overridden.
            
                     */
            // pass
            return Py.None;
        }
        
        private static PyObject finish_request$8(PyFrame frame) {
            /* Finish one request by instantiating RequestHandlerClass. */
            frame.getlocal(0).invoke("RequestHandlerClass", new PyObject[] {frame.getlocal(1), frame.getlocal(2), frame.getlocal(0)});
            return Py.None;
        }
        
        private static PyObject close_request$9(PyFrame frame) {
            /* Called to clean up an individual request. */
            // pass
            return Py.None;
        }
        
        private static PyObject handle_error$10(PyFrame frame) {
            /* Handle an error gracefully.  May be overridden.
            
                    The default is to print a traceback and continue.
            
                     */
            Py.println(s$30._mul(i$31));
            Py.printComma(s$32);
            Py.println(frame.getlocal(2));
            frame.setlocal(3, org.python.core.imp.importOne("traceback", frame));
            frame.getlocal(3).__getattr__("print_exc").__call__();
            Py.println(s$30._mul(i$31));
            return Py.None;
        }
        
        private static PyObject BaseServer$11(PyFrame frame) {
            /* Base class for server classes.
            
                Methods for the caller:
            
                - __init__(server_address, RequestHandlerClass)
                - serve_forever()
                - handle_request()  # if you do not use serve_forever()
                - fileno() -> int   # for select()
            
                Methods that may be overridden:
            
                - server_bind()
                - server_activate()
                - get_request() -> request, client_address
                - verify_request(request, client_address)
                - server_close()
                - process_request(request, client_address)
                - close_request(request)
                - handle_error()
            
                Methods for derived classes:
            
                - finish_request(request, client_address)
            
                Class variables that may be overridden by derived classes or
                instances:
            
                - address_family
                - socket_type
                - reuse_address
            
                Instance variables:
            
                - RequestHandlerClass
                - socket
            
                 */
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {}, c$0___init__));
            frame.setlocal("server_activate", new PyFunction(frame.f_globals, new PyObject[] {}, c$1_server_activate));
            frame.setlocal("serve_forever", new PyFunction(frame.f_globals, new PyObject[] {}, c$2_serve_forever));
            frame.setlocal("handle_request", new PyFunction(frame.f_globals, new PyObject[] {}, c$3_handle_request));
            frame.setlocal("verify_request", new PyFunction(frame.f_globals, new PyObject[] {}, c$4_verify_request));
            frame.setlocal("process_request", new PyFunction(frame.f_globals, new PyObject[] {}, c$5_process_request));
            frame.setlocal("server_close", new PyFunction(frame.f_globals, new PyObject[] {}, c$6_server_close));
            frame.setlocal("finish_request", new PyFunction(frame.f_globals, new PyObject[] {}, c$7_finish_request));
            frame.setlocal("close_request", new PyFunction(frame.f_globals, new PyObject[] {}, c$8_close_request));
            frame.setlocal("handle_error", new PyFunction(frame.f_globals, new PyObject[] {}, c$9_handle_error));
            return frame.getf_locals();
        }
        
        private static PyObject __init__$12(PyFrame frame) {
            /* Constructor.  May be extended, do not override. */
            frame.getglobal("BaseServer").invoke("__init__", new PyObject[] {frame.getlocal(0), frame.getlocal(1), frame.getlocal(2)});
            frame.getlocal(0).__setattr__("socket", frame.getglobal("socket").__getattr__("socket").__call__(frame.getlocal(0).__getattr__("address_family"), frame.getlocal(0).__getattr__("socket_type")));
            frame.getlocal(0).invoke("server_bind");
            frame.getlocal(0).invoke("server_activate");
            return Py.None;
        }
        
        private static PyObject server_bind$13(PyFrame frame) {
            /* Called by constructor to bind the socket.
            
                    May be overridden.
            
                     */
            if (frame.getlocal(0).__getattr__("allow_reuse_address").__nonzero__()) {
                frame.getlocal(0).__getattr__("socket").invoke("setsockopt", new PyObject[] {frame.getglobal("socket").__getattr__("SOL_SOCKET"), frame.getglobal("socket").__getattr__("SO_REUSEADDR"), i$22});
            }
            frame.getlocal(0).__getattr__("socket").invoke("bind", frame.getlocal(0).__getattr__("server_address"));
            return Py.None;
        }
        
        private static PyObject server_activate$14(PyFrame frame) {
            /* Called by constructor to activate the server.
            
                    May be overridden.
            
                     */
            frame.getlocal(0).__getattr__("socket").invoke("listen", frame.getlocal(0).__getattr__("request_queue_size"));
            return Py.None;
        }
        
        private static PyObject server_close$15(PyFrame frame) {
            /* Called to clean-up the server.
            
                    May be overridden.
            
                     */
            frame.getlocal(0).__getattr__("socket").invoke("close");
            return Py.None;
        }
        
        private static PyObject fileno$16(PyFrame frame) {
            /* Return socket file number.
            
                    Interface required by select().
            
                     */
            return frame.getlocal(0).__getattr__("socket").invoke("fileno");
        }
        
        private static PyObject get_request$17(PyFrame frame) {
            /* Get the request and client address from the socket.
            
                    May be overridden.
            
                     */
            return frame.getlocal(0).__getattr__("socket").invoke("accept");
        }
        
        private static PyObject close_request$18(PyFrame frame) {
            /* Called to clean up an individual request. */
            frame.getlocal(1).invoke("close");
            return Py.None;
        }
        
        private static PyObject TCPServer$19(PyFrame frame) {
            /* Base class for various socket-based server classes.
            
                Defaults to synchronous IP stream (i.e., TCP).
            
                Methods for the caller:
            
                - __init__(server_address, RequestHandlerClass)
                - serve_forever()
                - handle_request()  # if you don't use serve_forever()
                - fileno() -> int   # for select()
            
                Methods that may be overridden:
            
                - server_bind()
                - server_activate()
                - get_request() -> request, client_address
                - verify_request(request, client_address)
                - process_request(request, client_address)
                - close_request(request)
                - handle_error()
            
                Methods for derived classes:
            
                - finish_request(request, client_address)
            
                Class variables that may be overridden by derived classes or
                instances:
            
                - address_family
                - socket_type
                - request_queue_size (only for stream sockets)
                - reuse_address
            
                Instance variables:
            
                - server_address
                - RequestHandlerClass
                - socket
            
                 */
            frame.setlocal("address_family", frame.getname("socket").__getattr__("AF_INET"));
            frame.setlocal("socket_type", frame.getname("socket").__getattr__("SOCK_STREAM"));
            frame.setlocal("request_queue_size", i$34);
            frame.setlocal("allow_reuse_address", i$35);
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {}, c$11___init__));
            frame.setlocal("server_bind", new PyFunction(frame.f_globals, new PyObject[] {}, c$12_server_bind));
            frame.setlocal("server_activate", new PyFunction(frame.f_globals, new PyObject[] {}, c$13_server_activate));
            frame.setlocal("server_close", new PyFunction(frame.f_globals, new PyObject[] {}, c$14_server_close));
            frame.setlocal("fileno", new PyFunction(frame.f_globals, new PyObject[] {}, c$15_fileno));
            frame.setlocal("get_request", new PyFunction(frame.f_globals, new PyObject[] {}, c$16_get_request));
            frame.setlocal("close_request", new PyFunction(frame.f_globals, new PyObject[] {}, c$17_close_request));
            return frame.getf_locals();
        }
        
        private static PyObject get_request$20(PyFrame frame) {
            // Temporary Variables
            PyObject[] t$0$PyObject__;
            
            // Code
            t$0$PyObject__ = org.python.core.Py.unpackSequence(frame.getlocal(0).__getattr__("socket").invoke("recvfrom", frame.getlocal(0).__getattr__("max_packet_size")), 2);
            frame.setlocal(2, t$0$PyObject__[0]);
            frame.setlocal(1, t$0$PyObject__[1]);
            return new PyTuple(new PyObject[] {new PyTuple(new PyObject[] {frame.getlocal(2), frame.getlocal(0).__getattr__("socket")}), frame.getlocal(1)});
        }
        
        private static PyObject server_activate$21(PyFrame frame) {
            // pass
            return Py.None;
        }
        
        private static PyObject close_request$22(PyFrame frame) {
            // pass
            return Py.None;
        }
        
        private static PyObject UDPServer$23(PyFrame frame) {
            /* UDP server class. */
            frame.setlocal("allow_reuse_address", i$35);
            frame.setlocal("socket_type", frame.getname("socket").__getattr__("SOCK_DGRAM"));
            frame.setlocal("max_packet_size", i$40);
            frame.setlocal("get_request", new PyFunction(frame.f_globals, new PyObject[] {}, c$19_get_request));
            frame.setlocal("server_activate", new PyFunction(frame.f_globals, new PyObject[] {}, c$20_server_activate));
            frame.setlocal("close_request", new PyFunction(frame.f_globals, new PyObject[] {}, c$21_close_request));
            return frame.getf_locals();
        }
        
        private static PyObject collect_children$24(PyFrame frame) {
            // Temporary Variables
            PyObject[] t$0$PyObject__;
            PyException t$0$PyException;
            
            // Code
            /* Internal routine to wait for died children. */
            while (frame.getlocal(0).__getattr__("active_children").__nonzero__()) {
                if (frame.getglobal("len").__call__(frame.getlocal(0).__getattr__("active_children"))._lt(frame.getlocal(0).__getattr__("max_children")).__nonzero__()) {
                    frame.setlocal(3, frame.getglobal("os").__getattr__("WNOHANG"));
                }
                else {
                    frame.setlocal(3, i$35);
                }
                try {
                    t$0$PyObject__ = org.python.core.Py.unpackSequence(frame.getglobal("os").__getattr__("waitpid").__call__(i$35, frame.getlocal(3)), 2);
                    frame.setlocal(2, t$0$PyObject__[0]);
                    frame.setlocal(1, t$0$PyObject__[1]);
                }
                catch (Throwable x$0) {
                    t$0$PyException = Py.setException(x$0, frame);
                    if (Py.matchException(t$0$PyException, frame.getglobal("os").__getattr__("error"))) {
                        frame.setlocal(2, frame.getglobal("None"));
                    }
                    else throw t$0$PyException;
                }
                if (frame.getlocal(2).__not__().__nonzero__()) {
                    break;
                }
                frame.getlocal(0).__getattr__("active_children").invoke("remove", frame.getlocal(2));
            }
            return Py.None;
        }
        
        private static PyObject process_request$25(PyFrame frame) {
            // Temporary Variables
            PyException t$0$PyException;
            
            // Code
            /* Fork a new subprocess to process the request. */
            frame.getlocal(0).invoke("collect_children");
            frame.setlocal(3, frame.getglobal("os").__getattr__("fork").__call__());
            if (frame.getlocal(3).__nonzero__()) {
                if (frame.getlocal(0).__getattr__("active_children")._is(frame.getglobal("None")).__nonzero__()) {
                    frame.getlocal(0).__setattr__("active_children", new PyList(new PyObject[] {}));
                }
                frame.getlocal(0).__getattr__("active_children").invoke("append", frame.getlocal(3));
                frame.getlocal(0).invoke("close_request", frame.getlocal(1));
                return Py.None;
            }
            else {
                try {
                    frame.getlocal(0).invoke("finish_request", frame.getlocal(1), frame.getlocal(2));
                    frame.getglobal("os").__getattr__("_exit").__call__(i$35);
                }
                catch (Throwable x$0) {
                    t$0$PyException = Py.setException(x$0, frame);
                    try {
                        frame.getlocal(0).invoke("handle_error", frame.getlocal(1), frame.getlocal(2));
                    }
                    finally {
                        frame.getglobal("os").__getattr__("_exit").__call__(i$22);
                    }
                }
            }
            return Py.None;
        }
        
        private static PyObject ForkingMixIn$26(PyFrame frame) {
            /* Mix-in class to handle each request in a new process. */
            frame.setlocal("active_children", frame.getname("None"));
            frame.setlocal("max_children", i$31);
            frame.setlocal("collect_children", new PyFunction(frame.f_globals, new PyObject[] {}, c$23_collect_children));
            frame.setlocal("process_request", new PyFunction(frame.f_globals, new PyObject[] {}, c$24_process_request));
            return frame.getf_locals();
        }
        
        private static PyObject process_request$27(PyFrame frame) {
            /* Start a new thread to process the request. */
            frame.setlocal(4, org.python.core.imp.importOne("threading", frame));
            frame.setlocal(3, frame.getlocal(4).__getattr__("Thread").__call__(new PyObject[] {frame.getlocal(0).__getattr__("finish_request"), new PyTuple(new PyObject[] {frame.getlocal(1), frame.getlocal(2)})}, new String[] {"target", "args"}));
            frame.getlocal(3).invoke("start");
            return Py.None;
        }
        
        private static PyObject ThreadingMixIn$28(PyFrame frame) {
            /* Mix-in class to handle each request in a new thread. */
            frame.setlocal("process_request", new PyFunction(frame.f_globals, new PyObject[] {}, c$26_process_request));
            return frame.getf_locals();
        }
        
        private static PyObject ForkingUDPServer$29(PyFrame frame) {
            // pass
            return frame.getf_locals();
        }
        
        private static PyObject ForkingTCPServer$30(PyFrame frame) {
            // pass
            return frame.getf_locals();
        }
        
        private static PyObject ThreadingUDPServer$31(PyFrame frame) {
            // pass
            return frame.getf_locals();
        }
        
        private static PyObject ThreadingTCPServer$32(PyFrame frame) {
            // pass
            return frame.getf_locals();
        }
        
        private static PyObject UnixStreamServer$33(PyFrame frame) {
            frame.setlocal("address_family", frame.getname("socket").__getattr__("AF_UNIX"));
            return frame.getf_locals();
        }
        
        private static PyObject UnixDatagramServer$34(PyFrame frame) {
            frame.setlocal("address_family", frame.getname("socket").__getattr__("AF_UNIX"));
            return frame.getf_locals();
        }
        
        private static PyObject ThreadingUnixStreamServer$35(PyFrame frame) {
            // pass
            return frame.getf_locals();
        }
        
        private static PyObject ThreadingUnixDatagramServer$36(PyFrame frame) {
            // pass
            return frame.getf_locals();
        }
        
        private static PyObject __init__$37(PyFrame frame) {
            frame.getlocal(0).__setattr__("request", frame.getlocal(1));
            frame.getlocal(0).__setattr__("client_address", frame.getlocal(2));
            frame.getlocal(0).__setattr__("server", frame.getlocal(3));
            try {
                frame.getlocal(0).invoke("setup");
                frame.getlocal(0).invoke("handle");
                frame.getlocal(0).invoke("finish");
            }
            finally {
                frame.getglobal("sys").__setattr__("exc_traceback", frame.getglobal("None"));
            }
            return Py.None;
        }
        
        private static PyObject setup$38(PyFrame frame) {
            // pass
            return Py.None;
        }
        
        private static PyObject __del__$39(PyFrame frame) {
            // pass
            return Py.None;
        }
        
        private static PyObject handle$40(PyFrame frame) {
            // pass
            return Py.None;
        }
        
        private static PyObject finish$41(PyFrame frame) {
            // pass
            return Py.None;
        }
        
        private static PyObject BaseRequestHandler$42(PyFrame frame) {
            /* Base class for request handler classes.
            
                This class is instantiated for each request to be handled.  The
                constructor sets the instance variables request, client_address
                and server, and then calls the handle() method.  To implement a
                specific service, all you need to do is to derive a class which
                defines a handle() method.
            
                The handle() method can find the request as self.request, the
                client address as self.client_address, and the server (in case it
                needs access to per-server information) as self.server.  Since a
                separate instance is created for each request, the handle() method
                can define arbitrary other instance variariables.
            
                 */
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {}, c$36___init__));
            frame.setlocal("setup", new PyFunction(frame.f_globals, new PyObject[] {}, c$37_setup));
            frame.setlocal("__del__", new PyFunction(frame.f_globals, new PyObject[] {}, c$38___del__));
            frame.setlocal("handle", new PyFunction(frame.f_globals, new PyObject[] {}, c$39_handle));
            frame.setlocal("finish", new PyFunction(frame.f_globals, new PyObject[] {}, c$40_finish));
            return frame.getf_locals();
        }
        
        private static PyObject setup$43(PyFrame frame) {
            frame.getlocal(0).__setattr__("connection", frame.getlocal(0).__getattr__("request"));
            frame.getlocal(0).__setattr__("rfile", frame.getlocal(0).__getattr__("connection").invoke("makefile", s$48, frame.getlocal(0).__getattr__("rbufsize")));
            frame.getlocal(0).__setattr__("wfile", frame.getlocal(0).__getattr__("connection").invoke("makefile", s$49, frame.getlocal(0).__getattr__("wbufsize")));
            return Py.None;
        }
        
        private static PyObject finish$44(PyFrame frame) {
            frame.getlocal(0).__getattr__("wfile").invoke("flush");
            frame.getlocal(0).__getattr__("wfile").invoke("close");
            frame.getlocal(0).__getattr__("rfile").invoke("close");
            return Py.None;
        }
        
        private static PyObject StreamRequestHandler$45(PyFrame frame) {
            /* Define self.rfile and self.wfile for stream sockets. */
            frame.setlocal("rbufsize", i$22.__neg__());
            frame.setlocal("wbufsize", i$35);
            frame.setlocal("setup", new PyFunction(frame.f_globals, new PyObject[] {}, c$42_setup));
            frame.setlocal("finish", new PyFunction(frame.f_globals, new PyObject[] {}, c$43_finish));
            return frame.getf_locals();
        }
        
        private static PyObject setup$46(PyFrame frame) {
            // Temporary Variables
            PyObject[] t$0$PyObject__;
            
            // Code
            frame.setlocal(1, org.python.core.imp.importOne("StringIO", frame));
            t$0$PyObject__ = org.python.core.Py.unpackSequence(frame.getlocal(0).__getattr__("request"), 2);
            frame.getlocal(0).__setattr__("packet", t$0$PyObject__[0]);
            frame.getlocal(0).__setattr__("socket", t$0$PyObject__[1]);
            frame.getlocal(0).__setattr__("rfile", frame.getlocal(1).__getattr__("StringIO").__call__(frame.getlocal(0).__getattr__("packet")));
            frame.getlocal(0).__setattr__("wfile", frame.getlocal(1).__getattr__("StringIO").__call__());
            return Py.None;
        }
        
        private static PyObject finish$47(PyFrame frame) {
            frame.getlocal(0).__getattr__("socket").invoke("sendto", frame.getlocal(0).__getattr__("wfile").invoke("getvalue"), frame.getlocal(0).__getattr__("client_address"));
            return Py.None;
        }
        
        private static PyObject DatagramRequestHandler$48(PyFrame frame) {
            /* Define self.rfile and self.wfile for datagram sockets. */
            frame.setlocal("setup", new PyFunction(frame.f_globals, new PyObject[] {}, c$45_setup));
            frame.setlocal("finish", new PyFunction(frame.f_globals, new PyObject[] {}, c$46_finish));
            return frame.getf_locals();
        }
        
        private static PyObject main$49(PyFrame frame) {
            frame.setglobal("__file__", s$51);
            
            /* Generic socket server classes.
            
            This module tries to capture the various aspects of defining a server:
            
            For socket-based servers:
            
            - address family:
                    - AF_INET: IP (Internet Protocol) sockets (default)
                    - AF_UNIX: Unix domain sockets
                    - others, e.g. AF_DECNET are conceivable (see <socket.h>
            - socket type:
                    - SOCK_STREAM (reliable stream, e.g. TCP)
                    - SOCK_DGRAM (datagrams, e.g. UDP)
            
            For request-based servers (including socket-based):
            
            - client address verification before further looking at the request
                    (This is actually a hook for any processing that needs to look
                     at the request before anything else, e.g. logging)
            - how to handle multiple requests:
                    - synchronous (one request is handled at a time)
                    - forking (each request is handled by a new process)
                    - threading (each request is handled by a new thread)
            
            The classes in this module favor the server type that is simplest to
            write: a synchronous TCP/IP server.  This is bad class design, but
            save some typing.  (There's also the issue that a deep class hierarchy
            slows down method lookups.)
            
            There are five classes in an inheritance diagram, four of which represent
            synchronous servers of four types:
            
                    +------------+
                    | BaseServer |
                    +------------+
                          |
                          v
                    +-----------+        +------------------+
                    | TCPServer |------->| UnixStreamServer |
                    +-----------+        +------------------+
                          |
                          v
                    +-----------+        +--------------------+
                    | UDPServer |------->| UnixDatagramServer |
                    +-----------+        +--------------------+
            
            Note that UnixDatagramServer derives from UDPServer, not from
            UnixStreamServer -- the only difference between an IP and a Unix
            stream server is the address family, which is simply repeated in both
            unix server classes.
            
            Forking and threading versions of each type of server can be created
            using the ForkingServer and ThreadingServer mix-in classes.  For
            instance, a threading UDP server class is created as follows:
            
                    class ThreadingUDPServer(ThreadingMixIn, UDPServer): pass
            
            The Mix-in class must come first, since it overrides a method defined
            in UDPServer!
            
            To implement a service, you must derive a class from
            BaseRequestHandler and redefine its handle() method.  You can then run
            various versions of the service by combining one of the server classes
            with your request handler class.
            
            The request handler class must be different for datagram or stream
            services.  This can be hidden by using the mix-in request handler
            classes StreamRequestHandler or DatagramRequestHandler.
            
            Of course, you still have to use your head!
            
            For instance, it makes no sense to use a forking server if the service
            contains state in memory that can be modified by requests (since the
            modifications in the child process would never reach the initial state
            kept in the parent process and passed to each child).  In this case,
            you can use a threading server, but you will probably have to use
            locks to avoid two requests that come in nearly simultaneous to apply
            conflicting changes to the server state.
            
            On the other hand, if you are building e.g. an HTTP server, where all
            data is stored externally (e.g. in the file system), a synchronous
            class will essentially render the service "deaf" while one request is
            being handled -- which may be for a very long time if a client is slow
            to reqd all the data it has requested.  Here a threading or forking
            server is appropriate.
            
            In some cases, it may be appropriate to process part of a request
            synchronously, but to finish processing in a forked child depending on
            the request data.  This can be implemented by using a synchronous
            server and doing an explicit fork in the request handler class
            handle() method.
            
            Another approach to handling multiple simultaneous requests in an
            environment that supports neither threads nor fork (or where these are
            too expensive or inappropriate for the service) is to maintain an
            explicit table of partially finished requests and to use select() to
            decide which request to work on next (or whether to handle a new
            incoming request).  This is particularly important for stream services
            where each client can potentially be connected for a long time (if
            threads or subprocesses cannot be used).
            
            Future work:
            - Standard classes for Sun RPC (which uses either UDP or TCP)
            - Standard mix-in classes to implement various authentication
              and encryption schemes
            - Standard framework for select-based multiplexing
            
            XXX Open problems:
            - What to do with out-of-band data?
            
            BaseServer:
            - split generic "request" functionality out into BaseServer class.
              Copyright (C) 2000  Luke Kenneth Casson Leighton <lkcl@samba.org>
            
              example: read entries from a SQL database (requires overriding
              get_request() to return a table entry from the database).
              entry is processed by a RequestHandlerClass.
            
             */
            frame.setlocal("__version__", s$1);
            frame.setlocal("socket", org.python.core.imp.importOne("socket", frame));
            frame.setlocal("sys", org.python.core.imp.importOne("sys", frame));
            frame.setlocal("os", org.python.core.imp.importOne("os", frame));
            frame.setlocal("__all__", new PyList(new PyObject[] {s$2, s$3, s$4, s$5, s$6, s$7, s$8, s$9, s$10, s$11, s$12}));
            if (frame.getname("hasattr").__call__(frame.getname("socket"), s$13).__nonzero__()) {
                frame.getname("__all__").invoke("extend", new PyList(new PyObject[] {s$14, s$15, s$16, s$17}));
            }
            frame.setlocal("BaseServer", Py.makeClass("BaseServer", new PyObject[] {}, c$10_BaseServer, null));
            frame.setlocal("TCPServer", Py.makeClass("TCPServer", new PyObject[] {frame.getname("BaseServer")}, c$18_TCPServer, null));
            frame.setlocal("UDPServer", Py.makeClass("UDPServer", new PyObject[] {frame.getname("TCPServer")}, c$22_UDPServer, null));
            frame.setlocal("ForkingMixIn", Py.makeClass("ForkingMixIn", new PyObject[] {}, c$25_ForkingMixIn, null));
            frame.setlocal("ThreadingMixIn", Py.makeClass("ThreadingMixIn", new PyObject[] {}, c$27_ThreadingMixIn, null));
            frame.setlocal("ForkingUDPServer", Py.makeClass("ForkingUDPServer", new PyObject[] {frame.getname("ForkingMixIn"), frame.getname("UDPServer")}, c$28_ForkingUDPServer, null));
            frame.setlocal("ForkingTCPServer", Py.makeClass("ForkingTCPServer", new PyObject[] {frame.getname("ForkingMixIn"), frame.getname("TCPServer")}, c$29_ForkingTCPServer, null));
            frame.setlocal("ThreadingUDPServer", Py.makeClass("ThreadingUDPServer", new PyObject[] {frame.getname("ThreadingMixIn"), frame.getname("UDPServer")}, c$30_ThreadingUDPServer, null));
            frame.setlocal("ThreadingTCPServer", Py.makeClass("ThreadingTCPServer", new PyObject[] {frame.getname("ThreadingMixIn"), frame.getname("TCPServer")}, c$31_ThreadingTCPServer, null));
            if (frame.getname("hasattr").__call__(frame.getname("socket"), s$13).__nonzero__()) {
                frame.setlocal("UnixStreamServer", Py.makeClass("UnixStreamServer", new PyObject[] {frame.getname("TCPServer")}, c$32_UnixStreamServer, null));
                frame.setlocal("UnixDatagramServer", Py.makeClass("UnixDatagramServer", new PyObject[] {frame.getname("UDPServer")}, c$33_UnixDatagramServer, null));
                frame.setlocal("ThreadingUnixStreamServer", Py.makeClass("ThreadingUnixStreamServer", new PyObject[] {frame.getname("ThreadingMixIn"), frame.getname("UnixStreamServer")}, c$34_ThreadingUnixStreamServer, null));
                frame.setlocal("ThreadingUnixDatagramServer", Py.makeClass("ThreadingUnixDatagramServer", new PyObject[] {frame.getname("ThreadingMixIn"), frame.getname("UnixDatagramServer")}, c$35_ThreadingUnixDatagramServer, null));
            }
            frame.setlocal("BaseRequestHandler", Py.makeClass("BaseRequestHandler", new PyObject[] {}, c$41_BaseRequestHandler, null));
            frame.setlocal("StreamRequestHandler", Py.makeClass("StreamRequestHandler", new PyObject[] {frame.getname("BaseRequestHandler")}, c$44_StreamRequestHandler, null));
            frame.setlocal("DatagramRequestHandler", Py.makeClass("DatagramRequestHandler", new PyObject[] {frame.getname("BaseRequestHandler")}, c$47_DatagramRequestHandler, null));
            return Py.None;
        }
        
    }
    public static void moduleDictInit(PyObject dict) {
        dict.__setitem__("__name__", new PyString("SocketServer"));
        Py.runCode(new _PyInner().getMain(), dict, dict);
    }
    
    public static void main(String[] args) throws java.lang.Exception {
        String[] newargs = new String[args.length+1];
        newargs[0] = "SocketServer";
        System.arraycopy(args, 0, newargs, 1, args.length);
        Py.runMain(SocketServer._PyInner.class, newargs, SocketServer.jpy$packages, SocketServer.jpy$mainProperties, "", new String[] {"string", "random", "util", "traceback", "sre_compile", "atexit", "sre", "sre_constants", "StringIO", "javaos", "socket", "yapm", "calendar", "repr", "copy_reg", "SocketServer", "server", "re", "linecache", "javapath", "UserDict", "copy", "threading", "stat", "PathVFS", "sre_parse"});
    }
    
}
