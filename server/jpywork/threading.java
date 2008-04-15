import org.python.core.*;

public class threading extends java.lang.Object {
    static String[] jpy$mainProperties = new String[] {"python.modules.builtin", "exceptions:org.python.core.exceptions"};
    static String[] jpy$proxyProperties = new String[] {"python.modules.builtin", "exceptions:org.python.core.exceptions", "python.options.showJavaExceptions", "true"};
    static String[] jpy$packages = new String[] {"java.net", null, "java.lang", null, "org.python.core", null, "java.io", null, "java.util.zip", null};
    
    public static class _PyInner extends PyFunctionTable implements PyRunnable {
        private static PyObject s$0;
        private static PyObject i$1;
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
        private static PyObject s$12;
        private static PyObject s$13;
        private static PyObject s$14;
        private static PyObject s$15;
        private static PyObject f$16;
        private static PyObject f$17;
        private static PyObject f$18;
        private static PyObject s$19;
        private static PyObject s$20;
        private static PyObject s$21;
        private static PyObject s$22;
        private static PyObject s$23;
        private static PyObject s$24;
        private static PyObject s$25;
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
        private static PyObject f$60;
        private static PyObject s$61;
        private static PyObject i$62;
        private static PyObject i$63;
        private static PyObject i$64;
        private static PyObject s$65;
        private static PyObject s$66;
        private static PyObject s$67;
        private static PyFunctionTable funcTable;
        private static PyCode c$0___init__;
        private static PyCode c$1__note;
        private static PyCode c$2__Verbose;
        private static PyCode c$3___init__;
        private static PyCode c$4__note;
        private static PyCode c$5__Verbose;
        private static PyCode c$6_RLock;
        private static PyCode c$7___init__;
        private static PyCode c$8___repr__;
        private static PyCode c$9_acquire;
        private static PyCode c$10_release;
        private static PyCode c$11__acquire_restore;
        private static PyCode c$12__release_save;
        private static PyCode c$13__is_owned;
        private static PyCode c$14__RLock;
        private static PyCode c$15_Condition;
        private static PyCode c$16___init__;
        private static PyCode c$17___repr__;
        private static PyCode c$18__release_save;
        private static PyCode c$19__acquire_restore;
        private static PyCode c$20__is_owned;
        private static PyCode c$21_wait;
        private static PyCode c$22_notify;
        private static PyCode c$23_notifyAll;
        private static PyCode c$24__Condition;
        private static PyCode c$25_Semaphore;
        private static PyCode c$26___init__;
        private static PyCode c$27_acquire;
        private static PyCode c$28_release;
        private static PyCode c$29__Semaphore;
        private static PyCode c$30_Event;
        private static PyCode c$31___init__;
        private static PyCode c$32_isSet;
        private static PyCode c$33_set;
        private static PyCode c$34_clear;
        private static PyCode c$35_wait;
        private static PyCode c$36__Event;
        private static PyCode c$37__newname;
        private static PyCode c$38___init__;
        private static PyCode c$39__set_daemon;
        private static PyCode c$40___repr__;
        private static PyCode c$41_start;
        private static PyCode c$42_run;
        private static PyCode c$43__Thread__bootstrap;
        private static PyCode c$44__Thread__stop;
        private static PyCode c$45__Thread__delete;
        private static PyCode c$46_join;
        private static PyCode c$47_getName;
        private static PyCode c$48_setName;
        private static PyCode c$49_isAlive;
        private static PyCode c$50_isDaemon;
        private static PyCode c$51_setDaemon;
        private static PyCode c$52_Thread;
        private static PyCode c$53___init__;
        private static PyCode c$54__set_daemon;
        private static PyCode c$55___MainThread__exitfunc;
        private static PyCode c$56__MainThread;
        private static PyCode c$57__pickSomeNonDaemonThread;
        private static PyCode c$58___init__;
        private static PyCode c$59__set_daemon;
        private static PyCode c$60_join;
        private static PyCode c$61__DummyThread;
        private static PyCode c$62_currentThread;
        private static PyCode c$63_activeCount;
        private static PyCode c$64_enumerate;
        private static PyCode c$65___init__;
        private static PyCode c$66_put;
        private static PyCode c$67_get;
        private static PyCode c$68_BoundedQueue;
        private static PyCode c$69___init__;
        private static PyCode c$70_run;
        private static PyCode c$71_ProducerThread;
        private static PyCode c$72___init__;
        private static PyCode c$73_run;
        private static PyCode c$74_ConsumerThread;
        private static PyCode c$75__test;
        private static PyCode c$76_main;
        private static void initConstants() {
            s$0 = Py.newString("Proposed new threading module, emulating a subset of Java's threading model.");
            i$1 = Py.newInteger(0);
            s$2 = Py.newString("%s: %s\012");
            s$3 = Py.newString("<%s(%s, %d)>");
            i$4 = Py.newInteger(1);
            s$5 = Py.newString("%s.acquire(%s): recursive success");
            s$6 = Py.newString("%s.acquire(%s): initial succes");
            s$7 = Py.newString("%s.acquire(%s): failure");
            s$8 = Py.newString("release() of un-acquire()d lock");
            s$9 = Py.newString("%s.release(): final release");
            s$10 = Py.newString("%s.release(): non-final release");
            s$11 = Py.newString("%s._acquire_restore()");
            s$12 = Py.newString("%s._release_save()");
            s$13 = Py.newString("<Condition(%s, %d)>");
            s$14 = Py.newString("wait() of un-acquire()d lock");
            s$15 = Py.newString("%s.wait(): got it");
            f$16 = Py.newFloat(1.0E-6);
            f$17 = Py.newFloat(1.0);
            f$18 = Py.newFloat(2.0);
            s$19 = Py.newString("%s.wait(%s): timed out");
            s$20 = Py.newString("%s.wait(%s): got it");
            s$21 = Py.newString("notify() of un-acquire()d lock");
            s$22 = Py.newString("%s.notify(): no waiters");
            s$23 = Py.newString("%s.notify(): notifying %d waiter%s");
            s$24 = Py.newString("s");
            s$25 = Py.newString("");
            s$26 = Py.newString("Semaphore initial value must be >= 0");
            s$27 = Py.newString("Thread-%d");
            s$28 = Py.newString("group argument must be None for now");
            s$29 = Py.newString("Thread.__init__() was not called");
            s$30 = Py.newString("initial");
            s$31 = Py.newString("started");
            s$32 = Py.newString("stopped");
            s$33 = Py.newString(" daemon");
            s$34 = Py.newString("<%s(%s, %s)>");
            s$35 = Py.newString("Thread.__init__() not called");
            s$36 = Py.newString("thread already started");
            s$37 = Py.newString("%s.start(): starting thread");
            s$38 = Py.newString("%s.__bootstrap(): thread started");
            s$39 = Py.newString("%s.__bootstrap(): raised SystemExit");
            s$40 = Py.newString("%s.__bootstrap(): unhandled exception");
            s$41 = Py.newString("Exception in thread %s:\012%s\012");
            s$42 = Py.newString("%s.__bootstrap(): normal return");
            s$43 = Py.newString("cannot join thread before it is started");
            s$44 = Py.newString("cannot join current thread");
            s$45 = Py.newString("%s.join(): waiting until thread stops");
            s$46 = Py.newString("%s.join(): thread stopped");
            s$47 = Py.newString("%s.join(): timed out");
            s$48 = Py.newString("cannot set daemon status of active thread");
            s$49 = Py.newString("MainThread");
            s$50 = Py.newString("%s: waiting for other threads");
            s$51 = Py.newString("%s: exiting");
            s$52 = Py.newString("Dummy-%d");
            s$53 = Py.newString("cannot join a dummy thread");
            s$54 = Py.newString("put(%s): queue full");
            s$55 = Py.newString("put(%s): appended, length now %d");
            s$56 = Py.newString("get(): queue empty");
            s$57 = Py.newString("get(): got %s, %d left");
            s$58 = Py.newString("Producer");
            s$59 = Py.newString("%s.%d");
            f$60 = Py.newFloat(1.0E-5);
            s$61 = Py.newString("Consumer");
            i$62 = Py.newInteger(3);
            i$63 = Py.newInteger(4);
            i$64 = Py.newInteger(5);
            s$65 = Py.newString("Producer-%d");
            s$66 = Py.newString("__main__");
            s$67 = Py.newString("/usr/share/jython/Lib-cpython/threading.py");
            funcTable = new _PyInner();
            c$0___init__ = Py.newCode(2, new String[] {"self", "verbose"}, "/usr/share/jython/Lib-cpython/threading.py", "__init__", false, false, funcTable, 0, null, null, 0, 1);
            c$1__note = Py.newCode(3, new String[] {"self", "format", "args"}, "/usr/share/jython/Lib-cpython/threading.py", "_note", true, false, funcTable, 1, null, null, 0, 1);
            c$2__Verbose = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/threading.py", "_Verbose", false, false, funcTable, 2, null, null, 0, 0);
            c$3___init__ = Py.newCode(2, new String[] {"self", "verbose"}, "/usr/share/jython/Lib-cpython/threading.py", "__init__", false, false, funcTable, 3, null, null, 0, 1);
            c$4__note = Py.newCode(2, new String[] {"self", "args"}, "/usr/share/jython/Lib-cpython/threading.py", "_note", true, false, funcTable, 4, null, null, 0, 1);
            c$5__Verbose = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/threading.py", "_Verbose", false, false, funcTable, 5, null, null, 0, 0);
            c$6_RLock = Py.newCode(2, new String[] {"args", "kwargs"}, "/usr/share/jython/Lib-cpython/threading.py", "RLock", true, true, funcTable, 6, null, null, 0, 1);
            c$7___init__ = Py.newCode(2, new String[] {"self", "verbose"}, "/usr/share/jython/Lib-cpython/threading.py", "__init__", false, false, funcTable, 7, null, null, 0, 1);
            c$8___repr__ = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "__repr__", false, false, funcTable, 8, null, null, 0, 1);
            c$9_acquire = Py.newCode(2, new String[] {"self", "blocking", "me", "rc"}, "/usr/share/jython/Lib-cpython/threading.py", "acquire", false, false, funcTable, 9, null, null, 0, 1);
            c$10_release = Py.newCode(1, new String[] {"self", "count", "me"}, "/usr/share/jython/Lib-cpython/threading.py", "release", false, false, funcTable, 10, null, null, 0, 1);
            c$11__acquire_restore = Py.newCode(2, new String[] {"self", "(count, owner)", "owner", "count"}, "/usr/share/jython/Lib-cpython/threading.py", "_acquire_restore", false, false, funcTable, 11, null, null, 0, 1);
            c$12__release_save = Py.newCode(1, new String[] {"self", "owner", "count"}, "/usr/share/jython/Lib-cpython/threading.py", "_release_save", false, false, funcTable, 12, null, null, 0, 1);
            c$13__is_owned = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "_is_owned", false, false, funcTable, 13, null, null, 0, 1);
            c$14__RLock = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/threading.py", "_RLock", false, false, funcTable, 14, null, null, 0, 0);
            c$15_Condition = Py.newCode(2, new String[] {"args", "kwargs"}, "/usr/share/jython/Lib-cpython/threading.py", "Condition", true, true, funcTable, 15, null, null, 0, 1);
            c$16___init__ = Py.newCode(3, new String[] {"self", "lock", "verbose"}, "/usr/share/jython/Lib-cpython/threading.py", "__init__", false, false, funcTable, 16, null, null, 0, 1);
            c$17___repr__ = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "__repr__", false, false, funcTable, 17, null, null, 0, 1);
            c$18__release_save = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "_release_save", false, false, funcTable, 18, null, null, 0, 1);
            c$19__acquire_restore = Py.newCode(2, new String[] {"self", "x"}, "/usr/share/jython/Lib-cpython/threading.py", "_acquire_restore", false, false, funcTable, 19, null, null, 0, 1);
            c$20__is_owned = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "_is_owned", false, false, funcTable, 20, null, null, 0, 1);
            c$21_wait = Py.newCode(2, new String[] {"self", "timeout", "endtime", "saved_state", "delay", "me", "gotit", "waiter"}, "/usr/share/jython/Lib-cpython/threading.py", "wait", false, false, funcTable, 21, null, null, 0, 1);
            c$22_notify = Py.newCode(2, new String[] {"self", "n", "__waiters", "waiters", "me", "waiter"}, "/usr/share/jython/Lib-cpython/threading.py", "notify", false, false, funcTable, 22, null, null, 0, 1);
            c$23_notifyAll = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "notifyAll", false, false, funcTable, 23, null, null, 0, 1);
            c$24__Condition = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/threading.py", "_Condition", false, false, funcTable, 24, null, null, 0, 0);
            c$25_Semaphore = Py.newCode(2, new String[] {"args", "kwargs"}, "/usr/share/jython/Lib-cpython/threading.py", "Semaphore", true, true, funcTable, 25, null, null, 0, 1);
            c$26___init__ = Py.newCode(3, new String[] {"self", "value", "verbose"}, "/usr/share/jython/Lib-cpython/threading.py", "__init__", false, false, funcTable, 26, null, null, 0, 1);
            c$27_acquire = Py.newCode(2, new String[] {"self", "blocking", "rc"}, "/usr/share/jython/Lib-cpython/threading.py", "acquire", false, false, funcTable, 27, null, null, 0, 1);
            c$28_release = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "release", false, false, funcTable, 28, null, null, 0, 1);
            c$29__Semaphore = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/threading.py", "_Semaphore", false, false, funcTable, 29, null, null, 0, 0);
            c$30_Event = Py.newCode(2, new String[] {"args", "kwargs"}, "/usr/share/jython/Lib-cpython/threading.py", "Event", true, true, funcTable, 30, null, null, 0, 1);
            c$31___init__ = Py.newCode(2, new String[] {"self", "verbose"}, "/usr/share/jython/Lib-cpython/threading.py", "__init__", false, false, funcTable, 31, null, null, 0, 1);
            c$32_isSet = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "isSet", false, false, funcTable, 32, null, null, 0, 1);
            c$33_set = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "set", false, false, funcTable, 33, null, null, 0, 1);
            c$34_clear = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "clear", false, false, funcTable, 34, null, null, 0, 1);
            c$35_wait = Py.newCode(2, new String[] {"self", "timeout"}, "/usr/share/jython/Lib-cpython/threading.py", "wait", false, false, funcTable, 35, null, null, 0, 1);
            c$36__Event = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/threading.py", "_Event", false, false, funcTable, 36, null, null, 0, 0);
            c$37__newname = Py.newCode(1, new String[] {"template"}, "/usr/share/jython/Lib-cpython/threading.py", "_newname", false, false, funcTable, 37, null, null, 0, 1);
            c$38___init__ = Py.newCode(7, new String[] {"self", "group", "target", "name", "args", "kwargs", "verbose"}, "/usr/share/jython/Lib-cpython/threading.py", "__init__", false, false, funcTable, 38, null, null, 0, 1);
            c$39__set_daemon = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "_set_daemon", false, false, funcTable, 39, null, null, 0, 1);
            c$40___repr__ = Py.newCode(1, new String[] {"self", "status"}, "/usr/share/jython/Lib-cpython/threading.py", "__repr__", false, false, funcTable, 40, null, null, 0, 1);
            c$41_start = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "start", false, false, funcTable, 41, null, null, 0, 1);
            c$42_run = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "run", false, false, funcTable, 42, null, null, 0, 1);
            c$43__Thread__bootstrap = Py.newCode(1, new String[] {"self", "s"}, "/usr/share/jython/Lib-cpython/threading.py", "_Thread__bootstrap", false, false, funcTable, 43, null, null, 0, 1);
            c$44__Thread__stop = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "_Thread__stop", false, false, funcTable, 44, null, null, 0, 1);
            c$45__Thread__delete = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "_Thread__delete", false, false, funcTable, 45, null, null, 0, 1);
            c$46_join = Py.newCode(2, new String[] {"self", "timeout", "delay", "deadline"}, "/usr/share/jython/Lib-cpython/threading.py", "join", false, false, funcTable, 46, null, null, 0, 1);
            c$47_getName = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "getName", false, false, funcTable, 47, null, null, 0, 1);
            c$48_setName = Py.newCode(2, new String[] {"self", "name"}, "/usr/share/jython/Lib-cpython/threading.py", "setName", false, false, funcTable, 48, null, null, 0, 1);
            c$49_isAlive = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "isAlive", false, false, funcTable, 49, null, null, 0, 1);
            c$50_isDaemon = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "isDaemon", false, false, funcTable, 50, null, null, 0, 1);
            c$51_setDaemon = Py.newCode(2, new String[] {"self", "daemonic"}, "/usr/share/jython/Lib-cpython/threading.py", "setDaemon", false, false, funcTable, 51, null, null, 0, 1);
            c$52_Thread = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/threading.py", "Thread", false, false, funcTable, 52, null, null, 0, 0);
            c$53___init__ = Py.newCode(1, new String[] {"self", "atexit"}, "/usr/share/jython/Lib-cpython/threading.py", "__init__", false, false, funcTable, 53, null, null, 0, 1);
            c$54__set_daemon = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "_set_daemon", false, false, funcTable, 54, null, null, 0, 1);
            c$55___MainThread__exitfunc = Py.newCode(1, new String[] {"self", "t"}, "/usr/share/jython/Lib-cpython/threading.py", "__MainThread__exitfunc", false, false, funcTable, 55, null, null, 0, 1);
            c$56__MainThread = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/threading.py", "_MainThread", false, false, funcTable, 56, null, null, 0, 0);
            c$57__pickSomeNonDaemonThread = Py.newCode(0, new String[] {"t"}, "/usr/share/jython/Lib-cpython/threading.py", "_pickSomeNonDaemonThread", false, false, funcTable, 57, null, null, 0, 1);
            c$58___init__ = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "__init__", false, false, funcTable, 58, null, null, 0, 1);
            c$59__set_daemon = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "_set_daemon", false, false, funcTable, 59, null, null, 0, 1);
            c$60_join = Py.newCode(1, new String[] {"self"}, "/usr/share/jython/Lib-cpython/threading.py", "join", false, false, funcTable, 60, null, null, 0, 1);
            c$61__DummyThread = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/threading.py", "_DummyThread", false, false, funcTable, 61, null, null, 0, 0);
            c$62_currentThread = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/threading.py", "currentThread", false, false, funcTable, 62, null, null, 0, 1);
            c$63_activeCount = Py.newCode(0, new String[] {"count"}, "/usr/share/jython/Lib-cpython/threading.py", "activeCount", false, false, funcTable, 63, null, null, 0, 1);
            c$64_enumerate = Py.newCode(0, new String[] {"active"}, "/usr/share/jython/Lib-cpython/threading.py", "enumerate", false, false, funcTable, 64, null, null, 0, 1);
            c$65___init__ = Py.newCode(2, new String[] {"self", "limit"}, "/usr/share/jython/Lib-cpython/threading.py", "__init__", false, false, funcTable, 65, null, null, 0, 1);
            c$66_put = Py.newCode(2, new String[] {"self", "item"}, "/usr/share/jython/Lib-cpython/threading.py", "put", false, false, funcTable, 66, null, null, 0, 1);
            c$67_get = Py.newCode(1, new String[] {"self", "item"}, "/usr/share/jython/Lib-cpython/threading.py", "get", false, false, funcTable, 67, null, null, 0, 1);
            c$68_BoundedQueue = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/threading.py", "BoundedQueue", false, false, funcTable, 68, null, null, 0, 0);
            c$69___init__ = Py.newCode(3, new String[] {"self", "queue", "quota"}, "/usr/share/jython/Lib-cpython/threading.py", "__init__", false, false, funcTable, 69, null, null, 0, 1);
            c$70_run = Py.newCode(1, new String[] {"self", "counter", "random"}, "/usr/share/jython/Lib-cpython/threading.py", "run", false, false, funcTable, 70, null, null, 0, 1);
            c$71_ProducerThread = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/threading.py", "ProducerThread", false, false, funcTable, 71, null, null, 0, 0);
            c$72___init__ = Py.newCode(3, new String[] {"self", "queue", "count"}, "/usr/share/jython/Lib-cpython/threading.py", "__init__", false, false, funcTable, 72, null, null, 0, 1);
            c$73_run = Py.newCode(1, new String[] {"self", "item"}, "/usr/share/jython/Lib-cpython/threading.py", "run", false, false, funcTable, 73, null, null, 0, 1);
            c$74_ConsumerThread = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/threading.py", "ConsumerThread", false, false, funcTable, 74, null, null, 0, 0);
            c$75__test = Py.newCode(0, new String[] {"random", "Q", "P", "time", "ProducerThread", "t", "C", "BoundedQueue", "ConsumerThread", "i", "NP", "QL", "NI"}, "/usr/share/jython/Lib-cpython/threading.py", "_test", false, false, funcTable, 75, null, null, 0, 1);
            c$76_main = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/threading.py", "main", false, false, funcTable, 76, null, null, 0, 0);
        }
        
        
        public PyCode getMain() {
            if (c$76_main == null) _PyInner.initConstants();
            return c$76_main;
        }
        
        public PyObject call_function(int index, PyFrame frame) {
            switch (index){
                case 0:
                return _PyInner.__init__$1(frame);
                case 1:
                return _PyInner._note$2(frame);
                case 2:
                return _PyInner._Verbose$3(frame);
                case 3:
                return _PyInner.__init__$4(frame);
                case 4:
                return _PyInner._note$5(frame);
                case 5:
                return _PyInner._Verbose$6(frame);
                case 6:
                return _PyInner.RLock$7(frame);
                case 7:
                return _PyInner.__init__$8(frame);
                case 8:
                return _PyInner.__repr__$9(frame);
                case 9:
                return _PyInner.acquire$10(frame);
                case 10:
                return _PyInner.release$11(frame);
                case 11:
                return _PyInner._acquire_restore$12(frame);
                case 12:
                return _PyInner._release_save$13(frame);
                case 13:
                return _PyInner._is_owned$14(frame);
                case 14:
                return _PyInner._RLock$15(frame);
                case 15:
                return _PyInner.Condition$16(frame);
                case 16:
                return _PyInner.__init__$17(frame);
                case 17:
                return _PyInner.__repr__$18(frame);
                case 18:
                return _PyInner._release_save$19(frame);
                case 19:
                return _PyInner._acquire_restore$20(frame);
                case 20:
                return _PyInner._is_owned$21(frame);
                case 21:
                return _PyInner.wait$22(frame);
                case 22:
                return _PyInner.notify$23(frame);
                case 23:
                return _PyInner.notifyAll$24(frame);
                case 24:
                return _PyInner._Condition$25(frame);
                case 25:
                return _PyInner.Semaphore$26(frame);
                case 26:
                return _PyInner.__init__$27(frame);
                case 27:
                return _PyInner.acquire$28(frame);
                case 28:
                return _PyInner.release$29(frame);
                case 29:
                return _PyInner._Semaphore$30(frame);
                case 30:
                return _PyInner.Event$31(frame);
                case 31:
                return _PyInner.__init__$32(frame);
                case 32:
                return _PyInner.isSet$33(frame);
                case 33:
                return _PyInner.set$34(frame);
                case 34:
                return _PyInner.clear$35(frame);
                case 35:
                return _PyInner.wait$36(frame);
                case 36:
                return _PyInner._Event$37(frame);
                case 37:
                return _PyInner._newname$38(frame);
                case 38:
                return _PyInner.__init__$39(frame);
                case 39:
                return _PyInner._set_daemon$40(frame);
                case 40:
                return _PyInner.__repr__$41(frame);
                case 41:
                return _PyInner.start$42(frame);
                case 42:
                return _PyInner.run$43(frame);
                case 43:
                return _PyInner._Thread__bootstrap$44(frame);
                case 44:
                return _PyInner._Thread__stop$45(frame);
                case 45:
                return _PyInner._Thread__delete$46(frame);
                case 46:
                return _PyInner.join$47(frame);
                case 47:
                return _PyInner.getName$48(frame);
                case 48:
                return _PyInner.setName$49(frame);
                case 49:
                return _PyInner.isAlive$50(frame);
                case 50:
                return _PyInner.isDaemon$51(frame);
                case 51:
                return _PyInner.setDaemon$52(frame);
                case 52:
                return _PyInner.Thread$53(frame);
                case 53:
                return _PyInner.__init__$54(frame);
                case 54:
                return _PyInner._set_daemon$55(frame);
                case 55:
                return _PyInner.__MainThread__exitfunc$56(frame);
                case 56:
                return _PyInner._MainThread$57(frame);
                case 57:
                return _PyInner._pickSomeNonDaemonThread$58(frame);
                case 58:
                return _PyInner.__init__$59(frame);
                case 59:
                return _PyInner._set_daemon$60(frame);
                case 60:
                return _PyInner.join$61(frame);
                case 61:
                return _PyInner._DummyThread$62(frame);
                case 62:
                return _PyInner.currentThread$63(frame);
                case 63:
                return _PyInner.activeCount$64(frame);
                case 64:
                return _PyInner.enumerate$65(frame);
                case 65:
                return _PyInner.__init__$66(frame);
                case 66:
                return _PyInner.put$67(frame);
                case 67:
                return _PyInner.get$68(frame);
                case 68:
                return _PyInner.BoundedQueue$69(frame);
                case 69:
                return _PyInner.__init__$70(frame);
                case 70:
                return _PyInner.run$71(frame);
                case 71:
                return _PyInner.ProducerThread$72(frame);
                case 72:
                return _PyInner.__init__$73(frame);
                case 73:
                return _PyInner.run$74(frame);
                case 74:
                return _PyInner.ConsumerThread$75(frame);
                case 75:
                return _PyInner._test$76(frame);
                case 76:
                return _PyInner.main$77(frame);
                default:
                return null;
            }
        }
        
        private static PyObject __init__$1(PyFrame frame) {
            if (frame.getlocal(1)._is(frame.getglobal("None")).__nonzero__()) {
                frame.setlocal(1, frame.getglobal("_VERBOSE"));
            }
            frame.getlocal(0).__setattr__("__Verbose__verbose", frame.getlocal(1));
            return Py.None;
        }
        
        private static PyObject _note$2(PyFrame frame) {
            if (frame.getlocal(0).__getattr__("__Verbose__verbose").__nonzero__()) {
                frame.setlocal(1, frame.getlocal(1)._mod(frame.getlocal(2)));
                frame.setlocal(1, s$2._mod(new PyTuple(new PyObject[] {frame.getglobal("currentThread").__call__().invoke("getName"), frame.getlocal(1)})));
                frame.getglobal("_sys").__getattr__("stderr").__getattr__("write").__call__(frame.getlocal(1));
            }
            return Py.None;
        }
        
        private static PyObject _Verbose$3(PyFrame frame) {
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$0___init__));
            frame.setlocal("_note", new PyFunction(frame.f_globals, new PyObject[] {}, c$1__note));
            return frame.getf_locals();
        }
        
        private static PyObject __init__$4(PyFrame frame) {
            // pass
            return Py.None;
        }
        
        private static PyObject _note$5(PyFrame frame) {
            // pass
            return Py.None;
        }
        
        private static PyObject _Verbose$6(PyFrame frame) {
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$3___init__));
            frame.setlocal("_note", new PyFunction(frame.f_globals, new PyObject[] {}, c$4__note));
            return frame.getf_locals();
        }
        
        private static PyObject RLock$7(PyFrame frame) {
            return frame.getglobal("apply").__call__(frame.getglobal("_RLock"), frame.getlocal(0), frame.getlocal(1));
        }
        
        private static PyObject __init__$8(PyFrame frame) {
            frame.getglobal("_Verbose").invoke("__init__", frame.getlocal(0), frame.getlocal(1));
            frame.getlocal(0).__setattr__("__RLock__block", frame.getglobal("_allocate_lock").__call__());
            frame.getlocal(0).__setattr__("__RLock__owner", frame.getglobal("None"));
            frame.getlocal(0).__setattr__("__RLock__count", i$1);
            return Py.None;
        }
        
        private static PyObject __repr__$9(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject;
            
            // Code
            return s$3._mod(new PyTuple(new PyObject[] {frame.getlocal(0).__getattr__("__class__").__getattr__("__name__"), (t$0$PyObject = frame.getlocal(0).__getattr__("__RLock__owner")).__nonzero__() ? frame.getlocal(0).__getattr__("__RLock__owner").invoke("getName") : t$0$PyObject, frame.getlocal(0).__getattr__("__RLock__count")}));
        }
        
        private static PyObject acquire$10(PyFrame frame) {
            frame.setlocal(2, frame.getglobal("currentThread").__call__());
            if (frame.getlocal(0).__getattr__("__RLock__owner")._is(frame.getlocal(2)).__nonzero__()) {
                frame.getlocal(0).__setattr__("__RLock__count", frame.getlocal(0).__getattr__("__RLock__count")._add(i$4));
                if (frame.getglobal("__debug__").__nonzero__()) {
                    frame.getlocal(0).invoke("_note", new PyObject[] {s$5, frame.getlocal(0), frame.getlocal(1)});
                }
                return i$4;
            }
            frame.setlocal(3, frame.getlocal(0).__getattr__("__RLock__block").invoke("acquire", frame.getlocal(1)));
            if (frame.getlocal(3).__nonzero__()) {
                frame.getlocal(0).__setattr__("__RLock__owner", frame.getlocal(2));
                frame.getlocal(0).__setattr__("__RLock__count", i$4);
                if (frame.getglobal("__debug__").__nonzero__()) {
                    frame.getlocal(0).invoke("_note", new PyObject[] {s$6, frame.getlocal(0), frame.getlocal(1)});
                }
            }
            else {
                if (frame.getglobal("__debug__").__nonzero__()) {
                    frame.getlocal(0).invoke("_note", new PyObject[] {s$7, frame.getlocal(0), frame.getlocal(1)});
                }
            }
            return frame.getlocal(3);
        }
        
        private static PyObject release$11(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject;
            
            // Code
            frame.setlocal(2, frame.getglobal("currentThread").__call__());
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("__RLock__owner")._is(frame.getlocal(2)), s$8);
            t$0$PyObject = frame.getlocal(0).__getattr__("__RLock__count")._sub(i$4);
            frame.getlocal(0).__setattr__("__RLock__count", t$0$PyObject);
            frame.setlocal(1, t$0$PyObject);
            if (frame.getlocal(1).__not__().__nonzero__()) {
                frame.getlocal(0).__setattr__("__RLock__owner", frame.getglobal("None"));
                frame.getlocal(0).__getattr__("__RLock__block").invoke("release");
                if (frame.getglobal("__debug__").__nonzero__()) {
                    frame.getlocal(0).invoke("_note", s$9, frame.getlocal(0));
                }
            }
            else {
                if (frame.getglobal("__debug__").__nonzero__()) {
                    frame.getlocal(0).invoke("_note", s$10, frame.getlocal(0));
                }
            }
            return Py.None;
        }
        
        private static PyObject _acquire_restore$12(PyFrame frame) {
            // Temporary Variables
            PyObject[] t$0$PyObject__;
            
            // Code
            t$0$PyObject__ = org.python.core.Py.unpackSequence(frame.getlocal(1), 2);
            frame.setlocal(3, t$0$PyObject__[0]);
            frame.setlocal(2, t$0$PyObject__[1]);
            frame.getlocal(0).__getattr__("__RLock__block").invoke("acquire");
            frame.getlocal(0).__setattr__("__RLock__count", frame.getlocal(3));
            frame.getlocal(0).__setattr__("__RLock__owner", frame.getlocal(2));
            if (frame.getglobal("__debug__").__nonzero__()) {
                frame.getlocal(0).invoke("_note", s$11, frame.getlocal(0));
            }
            return Py.None;
        }
        
        private static PyObject _release_save$13(PyFrame frame) {
            if (frame.getglobal("__debug__").__nonzero__()) {
                frame.getlocal(0).invoke("_note", s$12, frame.getlocal(0));
            }
            frame.setlocal(2, frame.getlocal(0).__getattr__("__RLock__count"));
            frame.getlocal(0).__setattr__("__RLock__count", i$1);
            frame.setlocal(1, frame.getlocal(0).__getattr__("__RLock__owner"));
            frame.getlocal(0).__setattr__("__RLock__owner", frame.getglobal("None"));
            frame.getlocal(0).__getattr__("__RLock__block").invoke("release");
            return new PyTuple(new PyObject[] {frame.getlocal(2), frame.getlocal(1)});
        }
        
        private static PyObject _is_owned$14(PyFrame frame) {
            return frame.getlocal(0).__getattr__("__RLock__owner")._is(frame.getglobal("currentThread").__call__());
        }
        
        private static PyObject _RLock$15(PyFrame frame) {
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$7___init__));
            frame.setlocal("__repr__", new PyFunction(frame.f_globals, new PyObject[] {}, c$8___repr__));
            frame.setlocal("acquire", new PyFunction(frame.f_globals, new PyObject[] {i$4}, c$9_acquire));
            frame.setlocal("release", new PyFunction(frame.f_globals, new PyObject[] {}, c$10_release));
            frame.setlocal("_acquire_restore", new PyFunction(frame.f_globals, new PyObject[] {}, c$11__acquire_restore));
            frame.setlocal("_release_save", new PyFunction(frame.f_globals, new PyObject[] {}, c$12__release_save));
            frame.setlocal("_is_owned", new PyFunction(frame.f_globals, new PyObject[] {}, c$13__is_owned));
            return frame.getf_locals();
        }
        
        private static PyObject Condition$16(PyFrame frame) {
            return frame.getglobal("apply").__call__(frame.getglobal("_Condition"), frame.getlocal(0), frame.getlocal(1));
        }
        
        private static PyObject __init__$17(PyFrame frame) {
            // Temporary Variables
            PyException t$0$PyException;
            
            // Code
            frame.getglobal("_Verbose").invoke("__init__", frame.getlocal(0), frame.getlocal(2));
            if (frame.getlocal(1)._is(frame.getglobal("None")).__nonzero__()) {
                frame.setlocal(1, frame.getglobal("RLock").__call__());
            }
            frame.getlocal(0).__setattr__("__Condition__lock", frame.getlocal(1));
            frame.getlocal(0).__setattr__("acquire", frame.getlocal(1).__getattr__("acquire"));
            frame.getlocal(0).__setattr__("release", frame.getlocal(1).__getattr__("release"));
            try {
                frame.getlocal(0).__setattr__("_release_save", frame.getlocal(1).__getattr__("_release_save"));
            }
            catch (Throwable x$0) {
                t$0$PyException = Py.setException(x$0, frame);
                if (Py.matchException(t$0$PyException, frame.getglobal("AttributeError"))) {
                    // pass
                }
                else throw t$0$PyException;
            }
            try {
                frame.getlocal(0).__setattr__("_acquire_restore", frame.getlocal(1).__getattr__("_acquire_restore"));
            }
            catch (Throwable x$1) {
                t$0$PyException = Py.setException(x$1, frame);
                if (Py.matchException(t$0$PyException, frame.getglobal("AttributeError"))) {
                    // pass
                }
                else throw t$0$PyException;
            }
            try {
                frame.getlocal(0).__setattr__("_is_owned", frame.getlocal(1).__getattr__("_is_owned"));
            }
            catch (Throwable x$2) {
                t$0$PyException = Py.setException(x$2, frame);
                if (Py.matchException(t$0$PyException, frame.getglobal("AttributeError"))) {
                    // pass
                }
                else throw t$0$PyException;
            }
            frame.getlocal(0).__setattr__("__Condition__waiters", new PyList(new PyObject[] {}));
            return Py.None;
        }
        
        private static PyObject __repr__$18(PyFrame frame) {
            return s$13._mod(new PyTuple(new PyObject[] {frame.getlocal(0).__getattr__("__Condition__lock"), frame.getglobal("len").__call__(frame.getlocal(0).__getattr__("__Condition__waiters"))}));
        }
        
        private static PyObject _release_save$19(PyFrame frame) {
            frame.getlocal(0).__getattr__("__Condition__lock").invoke("release");
            return Py.None;
        }
        
        private static PyObject _acquire_restore$20(PyFrame frame) {
            frame.getlocal(0).__getattr__("__Condition__lock").invoke("acquire");
            return Py.None;
        }
        
        private static PyObject _is_owned$21(PyFrame frame) {
            if (frame.getlocal(0).__getattr__("__Condition__lock").invoke("acquire", i$1).__nonzero__()) {
                frame.getlocal(0).__getattr__("__Condition__lock").invoke("release");
                return i$1;
            }
            else {
                return i$4;
            }
        }
        
        private static PyObject wait$22(PyFrame frame) {
            // Temporary Variables
            PyException t$0$PyException;
            PyObject t$0$PyObject;
            
            // Code
            frame.setlocal(5, frame.getglobal("currentThread").__call__());
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).invoke("_is_owned"), s$14);
            frame.setlocal(7, frame.getglobal("_allocate_lock").__call__());
            frame.getlocal(7).invoke("acquire");
            frame.getlocal(0).__getattr__("__Condition__waiters").invoke("append", frame.getlocal(7));
            frame.setlocal(3, frame.getlocal(0).invoke("_release_save"));
            try {
                if (frame.getlocal(1)._is(frame.getglobal("None")).__nonzero__()) {
                    frame.getlocal(7).invoke("acquire");
                    if (frame.getglobal("__debug__").__nonzero__()) {
                        frame.getlocal(0).invoke("_note", s$15, frame.getlocal(0));
                    }
                }
                else {
                    frame.setlocal(2, frame.getglobal("_time").__call__()._add(frame.getlocal(1)));
                    frame.setlocal(4, f$16);
                    while (i$4.__nonzero__()) {
                        frame.setlocal(6, frame.getlocal(7).invoke("acquire", i$1));
                        if (((t$0$PyObject = frame.getlocal(6)).__nonzero__() ? t$0$PyObject : frame.getglobal("_time").__call__()._ge(frame.getlocal(2))).__nonzero__()) {
                            break;
                        }
                        frame.getglobal("_sleep").__call__(frame.getlocal(4));
                        if (frame.getlocal(4)._lt(f$17).__nonzero__()) {
                            frame.setlocal(4, frame.getlocal(4)._mul(f$18));
                        }
                    }
                    if (frame.getlocal(6).__not__().__nonzero__()) {
                        if (frame.getglobal("__debug__").__nonzero__()) {
                            frame.getlocal(0).invoke("_note", new PyObject[] {s$19, frame.getlocal(0), frame.getlocal(1)});
                        }
                        try {
                            frame.getlocal(0).__getattr__("__Condition__waiters").invoke("remove", frame.getlocal(7));
                        }
                        catch (Throwable x$0) {
                            t$0$PyException = Py.setException(x$0, frame);
                            if (Py.matchException(t$0$PyException, frame.getglobal("ValueError"))) {
                                // pass
                            }
                            else throw t$0$PyException;
                        }
                    }
                    else {
                        if (frame.getglobal("__debug__").__nonzero__()) {
                            frame.getlocal(0).invoke("_note", new PyObject[] {s$20, frame.getlocal(0), frame.getlocal(1)});
                        }
                    }
                }
            }
            finally {
                frame.getlocal(0).invoke("_acquire_restore", frame.getlocal(3));
            }
            return Py.None;
        }
        
        private static PyObject notify$23(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyException t$0$PyException;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            frame.setlocal(4, frame.getglobal("currentThread").__call__());
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).invoke("_is_owned"), s$21);
            frame.setlocal(2, frame.getlocal(0).__getattr__("__Condition__waiters"));
            frame.setlocal(3, frame.getlocal(2).__getslice__(null, frame.getlocal(1), null));
            if (frame.getlocal(3).__not__().__nonzero__()) {
                if (frame.getglobal("__debug__").__nonzero__()) {
                    frame.getlocal(0).invoke("_note", s$22, frame.getlocal(0));
                }
                return Py.None;
            }
            frame.getlocal(0).invoke("_note", new PyObject[] {s$23, frame.getlocal(0), frame.getlocal(1), (t$0$PyObject = ((t$1$PyObject = frame.getlocal(1)._ne(i$4)).__nonzero__() ? s$24 : t$1$PyObject)).__nonzero__() ? t$0$PyObject : s$25});
            t$0$int = 0;
            t$1$PyObject = frame.getlocal(3);
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                frame.setlocal(5, t$0$PyObject);
                frame.getlocal(5).invoke("release");
                try {
                    frame.getlocal(2).invoke("remove", frame.getlocal(5));
                }
                catch (Throwable x$0) {
                    t$0$PyException = Py.setException(x$0, frame);
                    if (Py.matchException(t$0$PyException, frame.getglobal("ValueError"))) {
                        // pass
                    }
                    else throw t$0$PyException;
                }
            }
            return Py.None;
        }
        
        private static PyObject notifyAll$24(PyFrame frame) {
            frame.getlocal(0).invoke("notify", frame.getglobal("len").__call__(frame.getlocal(0).__getattr__("__Condition__waiters")));
            return Py.None;
        }
        
        private static PyObject _Condition$25(PyFrame frame) {
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None"), frame.getname("None")}, c$16___init__));
            frame.setlocal("__repr__", new PyFunction(frame.f_globals, new PyObject[] {}, c$17___repr__));
            frame.setlocal("_release_save", new PyFunction(frame.f_globals, new PyObject[] {}, c$18__release_save));
            frame.setlocal("_acquire_restore", new PyFunction(frame.f_globals, new PyObject[] {}, c$19__acquire_restore));
            frame.setlocal("_is_owned", new PyFunction(frame.f_globals, new PyObject[] {}, c$20__is_owned));
            frame.setlocal("wait", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$21_wait));
            frame.setlocal("notify", new PyFunction(frame.f_globals, new PyObject[] {i$4}, c$22_notify));
            frame.setlocal("notifyAll", new PyFunction(frame.f_globals, new PyObject[] {}, c$23_notifyAll));
            return frame.getf_locals();
        }
        
        private static PyObject Semaphore$26(PyFrame frame) {
            return frame.getglobal("apply").__call__(frame.getglobal("_Semaphore"), frame.getlocal(0), frame.getlocal(1));
        }
        
        private static PyObject __init__$27(PyFrame frame) {
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(1)._ge(i$1), s$26);
            frame.getglobal("_Verbose").invoke("__init__", frame.getlocal(0), frame.getlocal(2));
            frame.getlocal(0).__setattr__("__Semaphore__cond", frame.getglobal("Condition").__call__(frame.getglobal("Lock").__call__()));
            frame.getlocal(0).__setattr__("__Semaphore__value", frame.getlocal(1));
            return Py.None;
        }
        
        private static PyObject acquire$28(PyFrame frame) {
            // Temporary Variables
            boolean t$0$boolean;
            
            // Code
            frame.setlocal(2, i$1);
            frame.getlocal(0).__getattr__("__Semaphore__cond").invoke("acquire");
            while (t$0$boolean=frame.getlocal(0).__getattr__("__Semaphore__value")._eq(i$1).__nonzero__()) {
                if (frame.getlocal(1).__not__().__nonzero__()) {
                    break;
                }
                frame.getlocal(0).__getattr__("__Semaphore__cond").invoke("wait");
            }
            if (!t$0$boolean) {
                frame.getlocal(0).__setattr__("__Semaphore__value", frame.getlocal(0).__getattr__("__Semaphore__value")._sub(i$4));
                frame.setlocal(2, i$4);
            }
            frame.getlocal(0).__getattr__("__Semaphore__cond").invoke("release");
            return frame.getlocal(2);
        }
        
        private static PyObject release$29(PyFrame frame) {
            frame.getlocal(0).__getattr__("__Semaphore__cond").invoke("acquire");
            frame.getlocal(0).__setattr__("__Semaphore__value", frame.getlocal(0).__getattr__("__Semaphore__value")._add(i$4));
            frame.getlocal(0).__getattr__("__Semaphore__cond").invoke("notify");
            frame.getlocal(0).__getattr__("__Semaphore__cond").invoke("release");
            return Py.None;
        }
        
        private static PyObject _Semaphore$30(PyFrame frame) {
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {i$4, frame.getname("None")}, c$26___init__));
            frame.setlocal("acquire", new PyFunction(frame.f_globals, new PyObject[] {i$4}, c$27_acquire));
            frame.setlocal("release", new PyFunction(frame.f_globals, new PyObject[] {}, c$28_release));
            return frame.getf_locals();
        }
        
        private static PyObject Event$31(PyFrame frame) {
            return frame.getglobal("apply").__call__(frame.getglobal("_Event"), frame.getlocal(0), frame.getlocal(1));
        }
        
        private static PyObject __init__$32(PyFrame frame) {
            frame.getglobal("_Verbose").invoke("__init__", frame.getlocal(0), frame.getlocal(1));
            frame.getlocal(0).__setattr__("__Event__cond", frame.getglobal("Condition").__call__(frame.getglobal("Lock").__call__()));
            frame.getlocal(0).__setattr__("__Event__flag", i$1);
            return Py.None;
        }
        
        private static PyObject isSet$33(PyFrame frame) {
            return frame.getlocal(0).__getattr__("__Event__flag");
        }
        
        private static PyObject set$34(PyFrame frame) {
            frame.getlocal(0).__getattr__("__Event__cond").invoke("acquire");
            frame.getlocal(0).__setattr__("__Event__flag", i$4);
            frame.getlocal(0).__getattr__("__Event__cond").invoke("notifyAll");
            frame.getlocal(0).__getattr__("__Event__cond").invoke("release");
            return Py.None;
        }
        
        private static PyObject clear$35(PyFrame frame) {
            frame.getlocal(0).__getattr__("__Event__cond").invoke("acquire");
            frame.getlocal(0).__setattr__("__Event__flag", i$1);
            frame.getlocal(0).__getattr__("__Event__cond").invoke("release");
            return Py.None;
        }
        
        private static PyObject wait$36(PyFrame frame) {
            frame.getlocal(0).__getattr__("__Event__cond").invoke("acquire");
            if (frame.getlocal(0).__getattr__("__Event__flag").__not__().__nonzero__()) {
                frame.getlocal(0).__getattr__("__Event__cond").invoke("wait", frame.getlocal(1));
            }
            frame.getlocal(0).__getattr__("__Event__cond").invoke("release");
            return Py.None;
        }
        
        private static PyObject _Event$37(PyFrame frame) {
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$31___init__));
            frame.setlocal("isSet", new PyFunction(frame.f_globals, new PyObject[] {}, c$32_isSet));
            frame.setlocal("set", new PyFunction(frame.f_globals, new PyObject[] {}, c$33_set));
            frame.setlocal("clear", new PyFunction(frame.f_globals, new PyObject[] {}, c$34_clear));
            frame.setlocal("wait", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$35_wait));
            return frame.getf_locals();
        }
        
        private static PyObject _newname$38(PyFrame frame) {
            // global _counter
            frame.setglobal("_counter", frame.getglobal("_counter")._add(i$4));
            return frame.getlocal(0)._mod(frame.getglobal("_counter"));
        }
        
        private static PyObject __init__$39(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject;
            
            // Code
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(1)._is(frame.getglobal("None")), s$28);
            frame.getglobal("_Verbose").invoke("__init__", frame.getlocal(0), frame.getlocal(6));
            frame.getlocal(0).__setattr__("_Thread__target", frame.getlocal(2));
            frame.getlocal(0).__setattr__("_Thread__name", frame.getglobal("str").__call__((t$0$PyObject = frame.getlocal(3)).__nonzero__() ? t$0$PyObject : frame.getglobal("_newname").__call__()));
            frame.getlocal(0).__setattr__("_Thread__args", frame.getlocal(4));
            frame.getlocal(0).__setattr__("_Thread__kwargs", frame.getlocal(5));
            frame.getlocal(0).__setattr__("_Thread__daemonic", frame.getlocal(0).invoke("_set_daemon"));
            frame.getlocal(0).__setattr__("_Thread__started", i$1);
            frame.getlocal(0).__setattr__("_Thread__stopped", i$1);
            frame.getlocal(0).__setattr__("_Thread__block", frame.getglobal("Condition").__call__(frame.getglobal("Lock").__call__()));
            frame.getlocal(0).__setattr__("_Thread__initialized", i$4);
            return Py.None;
        }
        
        private static PyObject _set_daemon$40(PyFrame frame) {
            return frame.getglobal("currentThread").__call__().invoke("isDaemon");
        }
        
        private static PyObject __repr__$41(PyFrame frame) {
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("_Thread__initialized"), s$29);
            frame.setlocal(1, s$30);
            if (frame.getlocal(0).__getattr__("_Thread__started").__nonzero__()) {
                frame.setlocal(1, s$31);
            }
            if (frame.getlocal(0).__getattr__("_Thread__stopped").__nonzero__()) {
                frame.setlocal(1, s$32);
            }
            if (frame.getlocal(0).__getattr__("_Thread__daemonic").__nonzero__()) {
                frame.setlocal(1, frame.getlocal(1)._add(s$33));
            }
            return s$34._mod(new PyTuple(new PyObject[] {frame.getlocal(0).__getattr__("__class__").__getattr__("__name__"), frame.getlocal(0).__getattr__("_Thread__name"), frame.getlocal(1)}));
        }
        
        private static PyObject start$42(PyFrame frame) {
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("_Thread__initialized"), s$35);
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("_Thread__started").__not__(), s$36);
            if (frame.getglobal("__debug__").__nonzero__()) {
                frame.getlocal(0).invoke("_note", s$37, frame.getlocal(0));
            }
            frame.getglobal("_active_limbo_lock").invoke("acquire");
            frame.getglobal("_limbo").__setitem__(frame.getlocal(0), frame.getlocal(0));
            frame.getglobal("_active_limbo_lock").invoke("release");
            frame.getglobal("_start_new_thread").__call__(frame.getlocal(0).__getattr__("_Thread__bootstrap"), new PyTuple(new PyObject[] {}));
            frame.getlocal(0).__setattr__("_Thread__started", i$4);
            frame.getglobal("_sleep").__call__(f$16);
            return Py.None;
        }
        
        private static PyObject run$43(PyFrame frame) {
            if (frame.getlocal(0).__getattr__("_Thread__target").__nonzero__()) {
                frame.getglobal("apply").__call__(frame.getlocal(0).__getattr__("_Thread__target"), frame.getlocal(0).__getattr__("_Thread__args"), frame.getlocal(0).__getattr__("_Thread__kwargs"));
            }
            return Py.None;
        }
        
        private static PyObject _Thread__bootstrap$44(PyFrame frame) {
            // Temporary Variables
            boolean t$0$boolean;
            PyException t$0$PyException;
            
            // Code
            try {
                frame.getlocal(0).__setattr__("_Thread__started", i$4);
                frame.getglobal("_active_limbo_lock").invoke("acquire");
                frame.getglobal("_active").__setitem__(frame.getglobal("_get_ident").__call__(), frame.getlocal(0));
                frame.getglobal("_limbo").__delitem__(frame.getlocal(0));
                frame.getglobal("_active_limbo_lock").invoke("release");
                if (frame.getglobal("__debug__").__nonzero__()) {
                    frame.getlocal(0).invoke("_note", s$38, frame.getlocal(0));
                }
                t$0$boolean = true;
                try {
                    frame.getlocal(0).invoke("run");
                }
                catch (Throwable x$0) {
                    t$0$boolean = false;
                    t$0$PyException = Py.setException(x$0, frame);
                    if (Py.matchException(t$0$PyException, frame.getglobal("SystemExit"))) {
                        if (frame.getglobal("__debug__").__nonzero__()) {
                            frame.getlocal(0).invoke("_note", s$39, frame.getlocal(0));
                        }
                    }
                    else {
                        if (frame.getglobal("__debug__").__nonzero__()) {
                            frame.getlocal(0).invoke("_note", s$40, frame.getlocal(0));
                        }
                        frame.setlocal(1, frame.getglobal("_StringIO").__call__());
                        frame.getglobal("_print_exc").__call__(new PyObject[] {frame.getlocal(1)}, new String[] {"file"});
                        frame.getglobal("_sys").__getattr__("stderr").__getattr__("write").__call__(s$41._mod(new PyTuple(new PyObject[] {frame.getlocal(0).invoke("getName"), frame.getlocal(1).invoke("getvalue")})));
                    }
                }
                if (t$0$boolean) {
                    if (frame.getglobal("__debug__").__nonzero__()) {
                        frame.getlocal(0).invoke("_note", s$42, frame.getlocal(0));
                    }
                }
            }
            finally {
                frame.getlocal(0).invoke("_Thread__stop");
                try {
                    frame.getlocal(0).invoke("_Thread__delete");
                }
                catch (Throwable x$1) {
                    t$0$PyException = Py.setException(x$1, frame);
                    // pass
                }
            }
            return Py.None;
        }
        
        private static PyObject _Thread__stop$45(PyFrame frame) {
            frame.getlocal(0).__getattr__("_Thread__block").invoke("acquire");
            frame.getlocal(0).__setattr__("_Thread__stopped", i$4);
            frame.getlocal(0).__getattr__("_Thread__block").invoke("notifyAll");
            frame.getlocal(0).__getattr__("_Thread__block").invoke("release");
            return Py.None;
        }
        
        private static PyObject _Thread__delete$46(PyFrame frame) {
            frame.getglobal("_active_limbo_lock").invoke("acquire");
            frame.getglobal("_active").__delitem__(frame.getglobal("_get_ident").__call__());
            frame.getglobal("_active_limbo_lock").invoke("release");
            return Py.None;
        }
        
        private static PyObject join$47(PyFrame frame) {
            // Temporary Variables
            boolean t$0$boolean;
            
            // Code
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("_Thread__initialized"), s$35);
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("_Thread__started"), s$43);
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0)._isnot(frame.getglobal("currentThread").__call__()), s$44);
            if (frame.getglobal("__debug__").__nonzero__()) {
                if (frame.getlocal(0).__getattr__("_Thread__stopped").__not__().__nonzero__()) {
                    frame.getlocal(0).invoke("_note", s$45, frame.getlocal(0));
                }
            }
            frame.getlocal(0).__getattr__("_Thread__block").invoke("acquire");
            if (frame.getlocal(1)._is(frame.getglobal("None")).__nonzero__()) {
                while (frame.getlocal(0).__getattr__("_Thread__stopped").__not__().__nonzero__()) {
                    frame.getlocal(0).__getattr__("_Thread__block").invoke("wait");
                }
                if (frame.getglobal("__debug__").__nonzero__()) {
                    frame.getlocal(0).invoke("_note", s$46, frame.getlocal(0));
                }
            }
            else {
                frame.setlocal(3, frame.getglobal("_time").__call__()._add(frame.getlocal(1)));
                while (t$0$boolean=frame.getlocal(0).__getattr__("_Thread__stopped").__not__().__nonzero__()) {
                    frame.setlocal(2, frame.getlocal(3)._sub(frame.getglobal("_time").__call__()));
                    if (frame.getlocal(2)._le(i$1).__nonzero__()) {
                        if (frame.getglobal("__debug__").__nonzero__()) {
                            frame.getlocal(0).invoke("_note", s$47, frame.getlocal(0));
                        }
                        break;
                    }
                    frame.getlocal(0).__getattr__("_Thread__block").invoke("wait", frame.getlocal(2));
                }
                if (!t$0$boolean) {
                    if (frame.getglobal("__debug__").__nonzero__()) {
                        frame.getlocal(0).invoke("_note", s$46, frame.getlocal(0));
                    }
                }
            }
            frame.getlocal(0).__getattr__("_Thread__block").invoke("release");
            return Py.None;
        }
        
        private static PyObject getName$48(PyFrame frame) {
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("_Thread__initialized"), s$35);
            return frame.getlocal(0).__getattr__("_Thread__name");
        }
        
        private static PyObject setName$49(PyFrame frame) {
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("_Thread__initialized"), s$35);
            frame.getlocal(0).__setattr__("_Thread__name", frame.getglobal("str").__call__(frame.getlocal(1)));
            return Py.None;
        }
        
        private static PyObject isAlive$50(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject;
            
            // Code
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("_Thread__initialized"), s$35);
            return (t$0$PyObject = frame.getlocal(0).__getattr__("_Thread__started")).__nonzero__() ? frame.getlocal(0).__getattr__("_Thread__stopped").__not__() : t$0$PyObject;
        }
        
        private static PyObject isDaemon$51(PyFrame frame) {
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("_Thread__initialized"), s$35);
            return frame.getlocal(0).__getattr__("_Thread__daemonic");
        }
        
        private static PyObject setDaemon$52(PyFrame frame) {
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("_Thread__initialized"), s$35);
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(0).__getattr__("_Thread__started").__not__(), s$48);
            frame.getlocal(0).__setattr__("_Thread__daemonic", frame.getlocal(1));
            return Py.None;
        }
        
        private static PyObject Thread$53(PyFrame frame) {
            frame.setlocal("_Thread__initialized", i$1);
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None"), frame.getname("None"), frame.getname("None"), new PyTuple(new PyObject[] {}), new PyDictionary(new PyObject[] {}), frame.getname("None")}, c$38___init__));
            frame.setlocal("_set_daemon", new PyFunction(frame.f_globals, new PyObject[] {}, c$39__set_daemon));
            frame.setlocal("__repr__", new PyFunction(frame.f_globals, new PyObject[] {}, c$40___repr__));
            frame.setlocal("start", new PyFunction(frame.f_globals, new PyObject[] {}, c$41_start));
            frame.setlocal("run", new PyFunction(frame.f_globals, new PyObject[] {}, c$42_run));
            frame.setlocal("_Thread__bootstrap", new PyFunction(frame.f_globals, new PyObject[] {}, c$43__Thread__bootstrap));
            frame.setlocal("_Thread__stop", new PyFunction(frame.f_globals, new PyObject[] {}, c$44__Thread__stop));
            frame.setlocal("_Thread__delete", new PyFunction(frame.f_globals, new PyObject[] {}, c$45__Thread__delete));
            frame.setlocal("join", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("None")}, c$46_join));
            frame.setlocal("getName", new PyFunction(frame.f_globals, new PyObject[] {}, c$47_getName));
            frame.setlocal("setName", new PyFunction(frame.f_globals, new PyObject[] {}, c$48_setName));
            frame.setlocal("isAlive", new PyFunction(frame.f_globals, new PyObject[] {}, c$49_isAlive));
            frame.setlocal("isDaemon", new PyFunction(frame.f_globals, new PyObject[] {}, c$50_isDaemon));
            frame.setlocal("setDaemon", new PyFunction(frame.f_globals, new PyObject[] {}, c$51_setDaemon));
            return frame.getf_locals();
        }
        
        private static PyObject __init__$54(PyFrame frame) {
            frame.getglobal("Thread").__getattr__("__init__").__call__(new PyObject[] {frame.getlocal(0), s$49}, new String[] {"name"});
            frame.getlocal(0).__setattr__("_Thread__started", i$4);
            frame.getglobal("_active_limbo_lock").invoke("acquire");
            frame.getglobal("_active").__setitem__(frame.getglobal("_get_ident").__call__(), frame.getlocal(0));
            frame.getglobal("_active_limbo_lock").invoke("release");
            frame.setlocal(1, org.python.core.imp.importOne("atexit", frame));
            frame.getlocal(1).__getattr__("register").__call__(frame.getlocal(0).__getattr__("__MainThread__exitfunc"));
            return Py.None;
        }
        
        private static PyObject _set_daemon$55(PyFrame frame) {
            return i$1;
        }
        
        private static PyObject __MainThread__exitfunc$56(PyFrame frame) {
            frame.getlocal(0).invoke("_Thread__stop");
            frame.setlocal(1, frame.getglobal("_pickSomeNonDaemonThread").__call__());
            if (frame.getlocal(1).__nonzero__()) {
                if (frame.getglobal("__debug__").__nonzero__()) {
                    frame.getlocal(0).invoke("_note", s$50, frame.getlocal(0));
                }
            }
            while (frame.getlocal(1).__nonzero__()) {
                frame.getlocal(1).invoke("join");
                frame.setlocal(1, frame.getglobal("_pickSomeNonDaemonThread").__call__());
            }
            if (frame.getglobal("__debug__").__nonzero__()) {
                frame.getlocal(0).invoke("_note", s$51, frame.getlocal(0));
            }
            frame.getlocal(0).invoke("_Thread__delete");
            return Py.None;
        }
        
        private static PyObject _MainThread$57(PyFrame frame) {
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {}, c$53___init__));
            frame.setlocal("_set_daemon", new PyFunction(frame.f_globals, new PyObject[] {}, c$54__set_daemon));
            frame.setlocal("__MainThread__exitfunc", new PyFunction(frame.f_globals, new PyObject[] {}, c$55___MainThread__exitfunc));
            return frame.getf_locals();
        }
        
        private static PyObject _pickSomeNonDaemonThread$58(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyObject t$0$PyObject, t$1$PyObject, t$2$PyObject;
            
            // Code
            t$0$int = 0;
            t$1$PyObject = frame.getglobal("enumerate").__call__();
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                frame.setlocal(0, t$0$PyObject);
                if (((t$2$PyObject = frame.getlocal(0).invoke("isDaemon").__not__()).__nonzero__() ? frame.getlocal(0).invoke("isAlive") : t$2$PyObject).__nonzero__()) {
                    return frame.getlocal(0);
                }
            }
            return frame.getglobal("None");
        }
        
        private static PyObject __init__$59(PyFrame frame) {
            frame.getglobal("Thread").__getattr__("__init__").__call__(new PyObject[] {frame.getlocal(0), frame.getglobal("_newname").__call__(s$52)}, new String[] {"name"});
            frame.getlocal(0).__setattr__("_Thread__started", i$4);
            frame.getglobal("_active_limbo_lock").invoke("acquire");
            frame.getglobal("_active").__setitem__(frame.getglobal("_get_ident").__call__(), frame.getlocal(0));
            frame.getglobal("_active_limbo_lock").invoke("release");
            return Py.None;
        }
        
        private static PyObject _set_daemon$60(PyFrame frame) {
            return i$4;
        }
        
        private static PyObject join$61(PyFrame frame) {
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(i$1, s$53);
            return Py.None;
        }
        
        private static PyObject _DummyThread$62(PyFrame frame) {
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {}, c$58___init__));
            frame.setlocal("_set_daemon", new PyFunction(frame.f_globals, new PyObject[] {}, c$59__set_daemon));
            frame.setlocal("join", new PyFunction(frame.f_globals, new PyObject[] {}, c$60_join));
            return frame.getf_locals();
        }
        
        private static PyObject currentThread$63(PyFrame frame) {
            // Temporary Variables
            PyException t$0$PyException;
            
            // Code
            try {
                return frame.getglobal("_active").__getitem__(frame.getglobal("_get_ident").__call__());
            }
            catch (Throwable x$0) {
                t$0$PyException = Py.setException(x$0, frame);
                if (Py.matchException(t$0$PyException, frame.getglobal("KeyError"))) {
                    return frame.getglobal("_DummyThread").__call__();
                }
                else throw t$0$PyException;
            }
        }
        
        private static PyObject activeCount$64(PyFrame frame) {
            frame.getglobal("_active_limbo_lock").invoke("acquire");
            frame.setlocal(0, frame.getglobal("len").__call__(frame.getglobal("_active"))._add(frame.getglobal("len").__call__(frame.getglobal("_limbo"))));
            frame.getglobal("_active_limbo_lock").invoke("release");
            return frame.getlocal(0);
        }
        
        private static PyObject enumerate$65(PyFrame frame) {
            frame.getglobal("_active_limbo_lock").invoke("acquire");
            frame.setlocal(0, frame.getglobal("_active").invoke("values")._add(frame.getglobal("_limbo").invoke("values")));
            frame.getglobal("_active_limbo_lock").invoke("release");
            return frame.getlocal(0);
        }
        
        private static PyObject __init__$66(PyFrame frame) {
            frame.getglobal("_Verbose").invoke("__init__", frame.getlocal(0));
            frame.getlocal(0).__setattr__("mon", frame.getglobal("RLock").__call__());
            frame.getlocal(0).__setattr__("rc", frame.getglobal("Condition").__call__(frame.getlocal(0).__getattr__("mon")));
            frame.getlocal(0).__setattr__("wc", frame.getglobal("Condition").__call__(frame.getlocal(0).__getattr__("mon")));
            frame.getlocal(0).__setattr__("limit", frame.getlocal(1));
            frame.getlocal(0).__setattr__("queue", new PyList(new PyObject[] {}));
            return Py.None;
        }
        
        private static PyObject put$67(PyFrame frame) {
            frame.getlocal(0).__getattr__("mon").invoke("acquire");
            while (frame.getglobal("len").__call__(frame.getlocal(0).__getattr__("queue"))._ge(frame.getlocal(0).__getattr__("limit")).__nonzero__()) {
                frame.getlocal(0).invoke("_note", s$54, frame.getlocal(1));
                frame.getlocal(0).__getattr__("wc").invoke("wait");
            }
            frame.getlocal(0).__getattr__("queue").invoke("append", frame.getlocal(1));
            frame.getlocal(0).invoke("_note", new PyObject[] {s$55, frame.getlocal(1), frame.getglobal("len").__call__(frame.getlocal(0).__getattr__("queue"))});
            frame.getlocal(0).__getattr__("rc").invoke("notify");
            frame.getlocal(0).__getattr__("mon").invoke("release");
            return Py.None;
        }
        
        private static PyObject get$68(PyFrame frame) {
            frame.getlocal(0).__getattr__("mon").invoke("acquire");
            while (frame.getlocal(0).__getattr__("queue").__not__().__nonzero__()) {
                frame.getlocal(0).invoke("_note", s$56);
                frame.getlocal(0).__getattr__("rc").invoke("wait");
            }
            frame.setlocal(1, frame.getlocal(0).__getattr__("queue").__getitem__(i$1));
            frame.getlocal(0).__getattr__("queue").__delitem__(i$1);
            frame.getlocal(0).invoke("_note", new PyObject[] {s$57, frame.getlocal(1), frame.getglobal("len").__call__(frame.getlocal(0).__getattr__("queue"))});
            frame.getlocal(0).__getattr__("wc").invoke("notify");
            frame.getlocal(0).__getattr__("mon").invoke("release");
            return frame.getlocal(1);
        }
        
        private static PyObject BoundedQueue$69(PyFrame frame) {
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {}, c$65___init__));
            frame.setlocal("put", new PyFunction(frame.f_globals, new PyObject[] {}, c$66_put));
            frame.setlocal("get", new PyFunction(frame.f_globals, new PyObject[] {}, c$67_get));
            return frame.getf_locals();
        }
        
        private static PyObject __init__$70(PyFrame frame) {
            frame.getglobal("Thread").__getattr__("__init__").__call__(new PyObject[] {frame.getlocal(0), s$58}, new String[] {"name"});
            frame.getlocal(0).__setattr__("queue", frame.getlocal(1));
            frame.getlocal(0).__setattr__("quota", frame.getlocal(2));
            return Py.None;
        }
        
        private static PyObject run$71(PyFrame frame) {
            PyObject[] imp_accu;
            // Code
            imp_accu = org.python.core.imp.importFrom("random", new String[] {"random"}, frame);
            frame.setlocal(2, imp_accu[0]);
            imp_accu = null;
            frame.setlocal(1, i$1);
            while (frame.getlocal(1)._lt(frame.getlocal(0).__getattr__("quota")).__nonzero__()) {
                frame.setlocal(1, frame.getlocal(1)._add(i$4));
                frame.getlocal(0).__getattr__("queue").invoke("put", s$59._mod(new PyTuple(new PyObject[] {frame.getlocal(0).invoke("getName"), frame.getlocal(1)})));
                frame.getglobal("_sleep").__call__(frame.getlocal(2).__call__()._mul(f$60));
            }
            return Py.None;
        }
        
        private static PyObject ProducerThread$72(PyFrame frame) {
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {}, c$69___init__));
            frame.setlocal("run", new PyFunction(frame.f_globals, new PyObject[] {}, c$70_run));
            return frame.getf_locals();
        }
        
        private static PyObject __init__$73(PyFrame frame) {
            frame.getglobal("Thread").__getattr__("__init__").__call__(new PyObject[] {frame.getlocal(0), s$61}, new String[] {"name"});
            frame.getlocal(0).__setattr__("queue", frame.getlocal(1));
            frame.getlocal(0).__setattr__("count", frame.getlocal(2));
            return Py.None;
        }
        
        private static PyObject run$74(PyFrame frame) {
            while (frame.getlocal(0).__getattr__("count")._gt(i$1).__nonzero__()) {
                frame.setlocal(1, frame.getlocal(0).__getattr__("queue").invoke("get"));
                Py.println(frame.getlocal(1));
                frame.getlocal(0).__setattr__("count", frame.getlocal(0).__getattr__("count")._sub(i$4));
            }
            return Py.None;
        }
        
        private static PyObject ConsumerThread$75(PyFrame frame) {
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {}, c$72___init__));
            frame.setlocal("run", new PyFunction(frame.f_globals, new PyObject[] {}, c$73_run));
            return frame.getf_locals();
        }
        
        private static PyObject _test$76(PyFrame frame) {
            // Temporary Variables
            int t$0$int, t$1$int, t$2$int;
            PyObject t$0$PyObject, t$1$PyObject, t$2$PyObject, t$3$PyObject, t$4$PyObject, t$5$PyObject;
            
            // Code
            frame.setlocal(0, org.python.core.imp.importOne("random", frame));
            frame.setlocal(7, Py.makeClass("BoundedQueue", new PyObject[] {frame.getglobal("_Verbose")}, c$68_BoundedQueue, null));
            frame.setlocal(4, Py.makeClass("ProducerThread", new PyObject[] {frame.getglobal("Thread")}, c$71_ProducerThread, null));
            frame.setlocal(8, Py.makeClass("ConsumerThread", new PyObject[] {frame.getglobal("Thread")}, c$74_ConsumerThread, null));
            frame.setlocal(3, org.python.core.imp.importOne("time", frame));
            frame.setlocal(10, i$62);
            frame.setlocal(11, i$63);
            frame.setlocal(12, i$64);
            frame.setlocal(1, frame.getlocal(7).__call__(frame.getlocal(11)));
            frame.setlocal(2, new PyList(new PyObject[] {}));
            t$0$int = 0;
            t$1$PyObject = frame.getglobal("range").__call__(frame.getlocal(10));
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                frame.setlocal(9, t$0$PyObject);
                frame.setlocal(5, frame.getlocal(4).__call__(frame.getlocal(1), frame.getlocal(12)));
                frame.getlocal(5).invoke("setName", s$65._mod(frame.getlocal(9)._add(i$4)));
                frame.getlocal(2).invoke("append", frame.getlocal(5));
            }
            frame.setlocal(6, frame.getlocal(8).__call__(frame.getlocal(1), frame.getlocal(12)._mul(frame.getlocal(10))));
            t$1$int = 0;
            t$3$PyObject = frame.getlocal(2);
            while ((t$2$PyObject = t$3$PyObject.__finditem__(t$1$int++)) != null) {
                frame.setlocal(5, t$2$PyObject);
                frame.getlocal(5).invoke("start");
                frame.getglobal("_sleep").__call__(f$16);
            }
            frame.getlocal(6).invoke("start");
            t$2$int = 0;
            t$5$PyObject = frame.getlocal(2);
            while ((t$4$PyObject = t$5$PyObject.__finditem__(t$2$int++)) != null) {
                frame.setlocal(5, t$4$PyObject);
                frame.getlocal(5).invoke("join");
            }
            frame.getlocal(6).invoke("join");
            return Py.None;
        }
        
        private static PyObject main$77(PyFrame frame) {
            frame.setglobal("__file__", s$67);
            
            /* Proposed new threading module, emulating a subset of Java's threading model. */
            frame.setlocal("sys", org.python.core.imp.importOne("sys", frame));
            frame.setlocal("time", org.python.core.imp.importOne("time", frame));
            frame.setlocal("thread", org.python.core.imp.importOne("thread", frame));
            frame.setlocal("traceback", org.python.core.imp.importOne("traceback", frame));
            frame.setlocal("StringIO", org.python.core.imp.importOne("StringIO", frame));
            frame.setlocal("_sys", frame.getname("sys"));
            frame.dellocal("sys");
            frame.setlocal("_time", frame.getname("time").__getattr__("time"));
            frame.setlocal("_sleep", frame.getname("time").__getattr__("sleep"));
            frame.dellocal("time");
            frame.setlocal("_start_new_thread", frame.getname("thread").__getattr__("start_new_thread"));
            frame.setlocal("_allocate_lock", frame.getname("thread").__getattr__("allocate_lock"));
            frame.setlocal("_get_ident", frame.getname("thread").__getattr__("get_ident"));
            frame.setlocal("ThreadError", frame.getname("thread").__getattr__("error"));
            frame.dellocal("thread");
            frame.setlocal("_print_exc", frame.getname("traceback").__getattr__("print_exc"));
            frame.dellocal("traceback");
            frame.setlocal("_StringIO", frame.getname("StringIO").__getattr__("StringIO"));
            frame.dellocal("StringIO");
            frame.setlocal("_VERBOSE", i$1);
            if (frame.getname("__debug__").__nonzero__()) {
                frame.setlocal("_Verbose", Py.makeClass("_Verbose", new PyObject[] {}, c$2__Verbose, null));
            }
            else {
                frame.setlocal("_Verbose", Py.makeClass("_Verbose", new PyObject[] {}, c$5__Verbose, null));
            }
            frame.setlocal("Lock", frame.getname("_allocate_lock"));
            frame.setlocal("RLock", new PyFunction(frame.f_globals, new PyObject[] {}, c$6_RLock));
            frame.setlocal("_RLock", Py.makeClass("_RLock", new PyObject[] {frame.getname("_Verbose")}, c$14__RLock, null));
            frame.setlocal("Condition", new PyFunction(frame.f_globals, new PyObject[] {}, c$15_Condition));
            frame.setlocal("_Condition", Py.makeClass("_Condition", new PyObject[] {frame.getname("_Verbose")}, c$24__Condition, null));
            frame.setlocal("Semaphore", new PyFunction(frame.f_globals, new PyObject[] {}, c$25_Semaphore));
            frame.setlocal("_Semaphore", Py.makeClass("_Semaphore", new PyObject[] {frame.getname("_Verbose")}, c$29__Semaphore, null));
            frame.setlocal("Event", new PyFunction(frame.f_globals, new PyObject[] {}, c$30_Event));
            frame.setlocal("_Event", Py.makeClass("_Event", new PyObject[] {frame.getname("_Verbose")}, c$36__Event, null));
            frame.setlocal("_counter", i$1);
            frame.setlocal("_newname", new PyFunction(frame.f_globals, new PyObject[] {s$27}, c$37__newname));
            frame.setlocal("_active_limbo_lock", frame.getname("_allocate_lock").__call__());
            frame.setlocal("_active", new PyDictionary(new PyObject[] {}));
            frame.setlocal("_limbo", new PyDictionary(new PyObject[] {}));
            frame.setlocal("Thread", Py.makeClass("Thread", new PyObject[] {frame.getname("_Verbose")}, c$52_Thread, null));
            frame.setlocal("_MainThread", Py.makeClass("_MainThread", new PyObject[] {frame.getname("Thread")}, c$56__MainThread, null));
            frame.setlocal("_pickSomeNonDaemonThread", new PyFunction(frame.f_globals, new PyObject[] {}, c$57__pickSomeNonDaemonThread));
            frame.setlocal("_DummyThread", Py.makeClass("_DummyThread", new PyObject[] {frame.getname("Thread")}, c$61__DummyThread, null));
            frame.setlocal("currentThread", new PyFunction(frame.f_globals, new PyObject[] {}, c$62_currentThread));
            frame.setlocal("activeCount", new PyFunction(frame.f_globals, new PyObject[] {}, c$63_activeCount));
            frame.setlocal("enumerate", new PyFunction(frame.f_globals, new PyObject[] {}, c$64_enumerate));
            frame.getname("_MainThread").__call__();
            frame.setlocal("_test", new PyFunction(frame.f_globals, new PyObject[] {}, c$75__test));
            if (frame.getname("__name__")._eq(s$66).__nonzero__()) {
                frame.getname("_test").__call__();
            }
            return Py.None;
        }
        
    }
    public static void moduleDictInit(PyObject dict) {
        dict.__setitem__("__name__", new PyString("threading"));
        Py.runCode(new _PyInner().getMain(), dict, dict);
    }
    
    public static void main(String[] args) throws java.lang.Exception {
        String[] newargs = new String[args.length+1];
        newargs[0] = "threading";
        System.arraycopy(args, 0, newargs, 1, args.length);
        Py.runMain(threading._PyInner.class, newargs, threading.jpy$packages, threading.jpy$mainProperties, "", new String[] {"string", "random", "util", "traceback", "sre_compile", "atexit", "sre", "sre_constants", "StringIO", "javaos", "socket", "yapm", "calendar", "repr", "copy_reg", "SocketServer", "server", "re", "linecache", "javapath", "UserDict", "copy", "threading", "stat", "PathVFS", "sre_parse"});
    }
    
}
