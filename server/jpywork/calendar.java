import org.python.core.*;

public class calendar extends java.lang.Object {
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
        private static PyObject i$59;
        private static PyObject s$60;
        private static PyObject s$61;
        private static PyObject s$62;
        private static PyObject i$63;
        private static PyObject i$64;
        private static PyObject i$65;
        private static PyObject s$66;
        private static PyObject s$67;
        private static PyObject i$68;
        private static PyObject s$69;
        private static PyObject i$70;
        private static PyObject s$71;
        private static PyObject s$72;
        private static PyObject i$73;
        private static PyObject s$74;
        private static PyObject s$75;
        private static PyObject s$76;
        private static PyObject s$77;
        private static PyObject s$78;
        private static PyObject s$79;
        private static PyObject i$80;
        private static PyObject s$81;
        private static PyObject s$82;
        private static PyObject s$83;
        private static PyObject i$84;
        private static PyObject s$85;
        private static PyObject s$86;
        private static PyObject s$87;
        private static PyObject s$88;
        private static PyObject i$89;
        private static PyObject s$90;
        private static PyObject i$91;
        private static PyObject i$92;
        private static PyObject i$93;
        private static PyObject s$94;
        private static PyFunctionTable funcTable;
        private static PyCode c$0_firstweekday;
        private static PyCode c$1_setfirstweekday;
        private static PyCode c$2_isleap;
        private static PyCode c$3_leapdays;
        private static PyCode c$4_weekday;
        private static PyCode c$5_monthrange;
        private static PyCode c$6_monthcalendar;
        private static PyCode c$7__center;
        private static PyCode c$8_prweek;
        private static PyCode c$9_week;
        private static PyCode c$10_weekheader;
        private static PyCode c$11_prmonth;
        private static PyCode c$12_month;
        private static PyCode c$13_format3c;
        private static PyCode c$14_format3cstring;
        private static PyCode c$15_prcal;
        private static PyCode c$16_calendar;
        private static PyCode c$17_timegm;
        private static PyCode c$18_main;
        private static void initConstants() {
            s$0 = Py.newString("Calendar printing functions\012\012Note when comparing these calendars to the ones printed by cal(1): By\012default, these calendars have Monday as the first day of the week, and\012Sunday as the last (the European convention). Use setfirstweekday() to\012set the first day of the week (0=Monday, 6=Sunday).");
            s$1 = Py.newString("error");
            s$2 = Py.newString("setfirstweekday");
            s$3 = Py.newString("firstweekday");
            s$4 = Py.newString("isleap");
            s$5 = Py.newString("leapdays");
            s$6 = Py.newString("weekday");
            s$7 = Py.newString("monthrange");
            s$8 = Py.newString("monthcalendar");
            s$9 = Py.newString("prmonth");
            s$10 = Py.newString("month");
            s$11 = Py.newString("prcal");
            s$12 = Py.newString("calendar");
            s$13 = Py.newString("timegm");
            i$14 = Py.newInteger(1);
            i$15 = Py.newInteger(2);
            i$16 = Py.newInteger(0);
            i$17 = Py.newInteger(31);
            i$18 = Py.newInteger(28);
            i$19 = Py.newInteger(30);
            s$20 = Py.newString("Monday");
            s$21 = Py.newString("Tuesday");
            s$22 = Py.newString("Wednesday");
            s$23 = Py.newString("Thursday");
            s$24 = Py.newString("Friday");
            s$25 = Py.newString("Saturday");
            s$26 = Py.newString("Sunday");
            s$27 = Py.newString("Mon");
            s$28 = Py.newString("Tue");
            s$29 = Py.newString("Wed");
            s$30 = Py.newString("Thu");
            s$31 = Py.newString("Fri");
            s$32 = Py.newString("Sat");
            s$33 = Py.newString("Sun");
            s$34 = Py.newString("");
            s$35 = Py.newString("January");
            s$36 = Py.newString("February");
            s$37 = Py.newString("March");
            s$38 = Py.newString("April");
            s$39 = Py.newString("May");
            s$40 = Py.newString("June");
            s$41 = Py.newString("July");
            s$42 = Py.newString("August");
            s$43 = Py.newString("September");
            s$44 = Py.newString("October");
            s$45 = Py.newString("November");
            s$46 = Py.newString("December");
            s$47 = Py.newString("   ");
            s$48 = Py.newString("Jan");
            s$49 = Py.newString("Feb");
            s$50 = Py.newString("Mar");
            s$51 = Py.newString("Apr");
            s$52 = Py.newString("Jun");
            s$53 = Py.newString("Jul");
            s$54 = Py.newString("Aug");
            s$55 = Py.newString("Sep");
            s$56 = Py.newString("Oct");
            s$57 = Py.newString("Nov");
            s$58 = Py.newString("Dec");
            i$59 = Py.newInteger(7);
            s$60 = Py.newString("Set weekday (Monday=0, Sunday=6) to start each week.");
            s$61 = Py.newString("bad weekday number; must be 0 (Monday) to 6 (Sunday)");
            s$62 = Py.newString("Return 1 for leap years, 0 for non-leap years.");
            i$63 = Py.newInteger(4);
            i$64 = Py.newInteger(100);
            i$65 = Py.newInteger(400);
            s$66 = Py.newString("Return number of leap years in range [y1, y2).\012       Assume y1 <= y2.");
            s$67 = Py.newString("Return weekday (0-6 ~ Mon-Sun) for year (1970-...), month (1-12),\012       day (1-31).");
            i$68 = Py.newInteger(6);
            s$69 = Py.newString("Return weekday (0-6 ~ Mon-Sun) and number of days (28-31) for\012       year, month.");
            i$70 = Py.newInteger(12);
            s$71 = Py.newString("bad month number");
            s$72 = Py.newString("Return a matrix representing a month's calendar.\012       Each row represents a week; days outside this month are zero.");
            i$73 = Py.newInteger(5);
            s$74 = Py.newString("Center a string in a field.");
            s$75 = Py.newString(" ");
            s$76 = Py.newString("Print a single week (no newline).");
            s$77 = Py.newString("Returns a single week in a string (no newline).");
            s$78 = Py.newString("%2i");
            s$79 = Py.newString("Return a header for a week.");
            i$80 = Py.newInteger(9);
            s$81 = Py.newString("Print a month's calendar.");
            s$82 = Py.newString("Return a month's calendar string (multi-line).");
            s$83 = Py.newString("\012");
            i$84 = Py.newInteger(3);
            s$85 = Py.newString("Prints 3-column formatting for year calendars");
            s$86 = Py.newString("Returns a string formatted from 3 strings, centered within 3 columns.");
            s$87 = Py.newString("Print a year's calendar.");
            s$88 = Py.newString("Returns a year's calendar as a multi-line string.");
            i$89 = Py.newInteger(1970);
            s$90 = Py.newString("Unrelated but handy function to calculate Unix timestamp from GMT.");
            i$91 = Py.newInteger(365);
            i$92 = Py.newInteger(24);
            i$93 = Py.newInteger(60);
            s$94 = Py.newString("/usr/share/jython/Lib-cpython/calendar.py");
            funcTable = new _PyInner();
            c$0_firstweekday = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/calendar.py", "firstweekday", false, false, funcTable, 0, null, null, 0, 1);
            c$1_setfirstweekday = Py.newCode(1, new String[] {"weekday"}, "/usr/share/jython/Lib-cpython/calendar.py", "setfirstweekday", false, false, funcTable, 1, null, null, 0, 1);
            c$2_isleap = Py.newCode(1, new String[] {"year"}, "/usr/share/jython/Lib-cpython/calendar.py", "isleap", false, false, funcTable, 2, null, null, 0, 1);
            c$3_leapdays = Py.newCode(2, new String[] {"y1", "y2"}, "/usr/share/jython/Lib-cpython/calendar.py", "leapdays", false, false, funcTable, 3, null, null, 0, 1);
            c$4_weekday = Py.newCode(3, new String[] {"year", "month", "day", "tuple", "secs"}, "/usr/share/jython/Lib-cpython/calendar.py", "weekday", false, false, funcTable, 4, null, null, 0, 1);
            c$5_monthrange = Py.newCode(2, new String[] {"year", "month", "ndays", "day1"}, "/usr/share/jython/Lib-cpython/calendar.py", "monthrange", false, false, funcTable, 5, null, null, 0, 1);
            c$6_monthcalendar = Py.newCode(2, new String[] {"year", "month", "ndays", "i", "day", "day1", "r7", "row", "rows"}, "/usr/share/jython/Lib-cpython/calendar.py", "monthcalendar", false, false, funcTable, 6, null, null, 0, 1);
            c$7__center = Py.newCode(2, new String[] {"str", "width", "n"}, "/usr/share/jython/Lib-cpython/calendar.py", "_center", false, false, funcTable, 7, null, null, 0, 1);
            c$8_prweek = Py.newCode(2, new String[] {"theweek", "width"}, "/usr/share/jython/Lib-cpython/calendar.py", "prweek", false, false, funcTable, 8, null, null, 0, 1);
            c$9_week = Py.newCode(2, new String[] {"theweek", "width", "day", "s", "days"}, "/usr/share/jython/Lib-cpython/calendar.py", "week", false, false, funcTable, 9, null, null, 0, 1);
            c$10_weekheader = Py.newCode(1, new String[] {"width", "i", "names", "days"}, "/usr/share/jython/Lib-cpython/calendar.py", "weekheader", false, false, funcTable, 10, null, null, 0, 1);
            c$11_prmonth = Py.newCode(4, new String[] {"theyear", "themonth", "w", "l"}, "/usr/share/jython/Lib-cpython/calendar.py", "prmonth", false, false, funcTable, 11, null, null, 0, 1);
            c$12_month = Py.newCode(4, new String[] {"theyear", "themonth", "w", "l", "aweek", "s"}, "/usr/share/jython/Lib-cpython/calendar.py", "month", false, false, funcTable, 12, null, null, 0, 1);
            c$13_format3c = Py.newCode(5, new String[] {"a", "b", "c", "colwidth", "spacing"}, "/usr/share/jython/Lib-cpython/calendar.py", "format3c", false, false, funcTable, 13, null, null, 0, 1);
            c$14_format3cstring = Py.newCode(5, new String[] {"a", "b", "c", "colwidth", "spacing"}, "/usr/share/jython/Lib-cpython/calendar.py", "format3cstring", false, false, funcTable, 14, null, null, 0, 1);
            c$15_prcal = Py.newCode(4, new String[] {"year", "w", "l", "c"}, "/usr/share/jython/Lib-cpython/calendar.py", "prcal", false, false, funcTable, 15, null, null, 0, 1);
            c$16_calendar = Py.newCode(4, new String[] {"year", "w", "l", "c", "weeks", "cal", "s", "height", "q", "colwidth", "amonth", "i", "header", "data"}, "/usr/share/jython/Lib-cpython/calendar.py", "calendar", false, false, funcTable, 16, null, null, 0, 1);
            c$17_timegm = Py.newCode(1, new String[] {"tuple", "second", "minute", "minutes", "hour", "i", "month", "year", "day", "hours", "seconds", "days"}, "/usr/share/jython/Lib-cpython/calendar.py", "timegm", false, false, funcTable, 17, null, null, 0, 1);
            c$18_main = Py.newCode(0, new String[] {}, "/usr/share/jython/Lib-cpython/calendar.py", "main", false, false, funcTable, 18, null, null, 0, 0);
        }
        
        
        public PyCode getMain() {
            if (c$18_main == null) _PyInner.initConstants();
            return c$18_main;
        }
        
        public PyObject call_function(int index, PyFrame frame) {
            switch (index){
                case 0:
                return _PyInner.firstweekday$1(frame);
                case 1:
                return _PyInner.setfirstweekday$2(frame);
                case 2:
                return _PyInner.isleap$3(frame);
                case 3:
                return _PyInner.leapdays$4(frame);
                case 4:
                return _PyInner.weekday$5(frame);
                case 5:
                return _PyInner.monthrange$6(frame);
                case 6:
                return _PyInner.monthcalendar$7(frame);
                case 7:
                return _PyInner._center$8(frame);
                case 8:
                return _PyInner.prweek$9(frame);
                case 9:
                return _PyInner.week$10(frame);
                case 10:
                return _PyInner.weekheader$11(frame);
                case 11:
                return _PyInner.prmonth$12(frame);
                case 12:
                return _PyInner.month$13(frame);
                case 13:
                return _PyInner.format3c$14(frame);
                case 14:
                return _PyInner.format3cstring$15(frame);
                case 15:
                return _PyInner.prcal$16(frame);
                case 16:
                return _PyInner.calendar$17(frame);
                case 17:
                return _PyInner.timegm$18(frame);
                case 18:
                return _PyInner.main$19(frame);
                default:
                return null;
            }
        }
        
        private static PyObject firstweekday$1(PyFrame frame) {
            return frame.getglobal("_firstweekday");
        }
        
        private static PyObject setfirstweekday$2(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject;
            
            // Code
            /* Set weekday (Monday=0, Sunday=6) to start each week. */
            // global _firstweekday
            if ((frame.getglobal("MONDAY")._le(t$0$PyObject = frame.getlocal(0)).__nonzero__() ? t$0$PyObject._le(frame.getglobal("SUNDAY")) : Py.Zero).__not__().__nonzero__()) {
                throw Py.makeException(frame.getglobal("ValueError"), s$61);
            }
            frame.setglobal("_firstweekday", frame.getlocal(0));
            return Py.None;
        }
        
        private static PyObject isleap$3(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            /* Return 1 for leap years, 0 for non-leap years. */
            return (t$0$PyObject = frame.getlocal(0)._mod(i$63)._eq(i$16)).__nonzero__() ? ((t$1$PyObject = frame.getlocal(0)._mod(i$64)._ne(i$16)).__nonzero__() ? t$1$PyObject : frame.getlocal(0)._mod(i$65)._eq(i$16)) : t$0$PyObject;
        }
        
        private static PyObject leapdays$4(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject;
            
            // Code
            /* Return number of leap years in range [y1, y2).
                   Assume y1 <= y2. */
            t$0$PyObject = i$14;
            frame.setlocal(0, frame.getlocal(0).__isub__(t$0$PyObject));
            t$0$PyObject = i$14;
            frame.setlocal(1, frame.getlocal(1).__isub__(t$0$PyObject));
            return frame.getlocal(1)._div(i$63)._sub(frame.getlocal(0)._div(i$63))._sub(frame.getlocal(1)._div(i$64)._sub(frame.getlocal(0)._div(i$64)))._add(frame.getlocal(1)._div(i$65)._sub(frame.getlocal(0)._div(i$65)));
        }
        
        private static PyObject weekday$5(PyFrame frame) {
            /* Return weekday (0-6 ~ Mon-Sun) for year (1970-...), month (1-12),
                   day (1-31). */
            frame.setlocal(4, frame.getglobal("mktime").__call__(new PyTuple(new PyObject[] {frame.getlocal(0), frame.getlocal(1), frame.getlocal(2), i$16, i$16, i$16, i$16, i$16, i$16})));
            frame.setlocal(3, frame.getglobal("localtime").__call__(frame.getlocal(4)));
            return frame.getlocal(3).__getitem__(i$68);
        }
        
        private static PyObject monthrange$6(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject;
            
            // Code
            /* Return weekday (0-6 ~ Mon-Sun) and number of days (28-31) for
                   year, month. */
            if ((i$14._le(t$0$PyObject = frame.getlocal(1)).__nonzero__() ? t$0$PyObject._le(i$70) : Py.Zero).__not__().__nonzero__()) {
                throw Py.makeException(frame.getglobal("ValueError"), s$71);
            }
            frame.setlocal(3, frame.getglobal("weekday").__call__(frame.getlocal(0), frame.getlocal(1), i$14));
            frame.setlocal(2, frame.getglobal("mdays").__getitem__(frame.getlocal(1))._add((t$0$PyObject = frame.getlocal(1)._eq(frame.getglobal("February"))).__nonzero__() ? frame.getglobal("isleap").__call__(frame.getlocal(0)) : t$0$PyObject));
            return new PyTuple(new PyObject[] {frame.getlocal(3), frame.getlocal(2)});
        }
        
        private static PyObject monthcalendar$7(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyObject[] t$0$PyObject__;
            PyObject t$0$PyObject, t$1$PyObject, t$2$PyObject;
            
            // Code
            /* Return a matrix representing a month's calendar.
                   Each row represents a week; days outside this month are zero. */
            t$0$PyObject__ = org.python.core.Py.unpackSequence(frame.getglobal("monthrange").__call__(frame.getlocal(0), frame.getlocal(1)), 2);
            frame.setlocal(5, t$0$PyObject__[0]);
            frame.setlocal(2, t$0$PyObject__[1]);
            frame.setlocal(8, new PyList(new PyObject[] {}));
            frame.setlocal(6, frame.getglobal("range").__call__(i$59));
            frame.setlocal(4, frame.getglobal("_firstweekday")._sub(frame.getlocal(5))._add(i$68)._mod(i$59)._sub(i$73));
            while (frame.getlocal(4)._le(frame.getlocal(2)).__nonzero__()) {
                frame.setlocal(7, new PyList(new PyObject[] {i$16, i$16, i$16, i$16, i$16, i$16, i$16}));
                t$0$int = 0;
                t$1$PyObject = frame.getlocal(6);
                while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                    frame.setlocal(3, t$0$PyObject);
                    if ((i$14._le(t$2$PyObject = frame.getlocal(4)).__nonzero__() ? t$2$PyObject._le(frame.getlocal(2)) : Py.Zero).__nonzero__()) {
                        frame.getlocal(7).__setitem__(frame.getlocal(3), frame.getlocal(4));
                    }
                    frame.setlocal(4, frame.getlocal(4)._add(i$14));
                }
                frame.getlocal(8).invoke("append", frame.getlocal(7));
            }
            return frame.getlocal(8);
        }
        
        private static PyObject _center$8(PyFrame frame) {
            /* Center a string in a field. */
            frame.setlocal(2, frame.getlocal(1)._sub(frame.getglobal("len").__call__(frame.getlocal(0))));
            if (frame.getlocal(2)._le(i$16).__nonzero__()) {
                return frame.getlocal(0);
            }
            return s$75._mul(frame.getlocal(2)._add(i$14)._div(i$15))._add(frame.getlocal(0))._add(s$75._mul(frame.getlocal(2)._div(i$15)));
        }
        
        private static PyObject prweek$9(PyFrame frame) {
            /* Print a single week (no newline). */
            Py.printComma(frame.getglobal("week").__call__(frame.getlocal(0), frame.getlocal(1)));
            return Py.None;
        }
        
        private static PyObject week$10(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            /* Returns a single week in a string (no newline). */
            frame.setlocal(4, new PyList(new PyObject[] {}));
            t$0$int = 0;
            t$1$PyObject = frame.getlocal(0);
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                frame.setlocal(2, t$0$PyObject);
                if (frame.getlocal(2)._eq(i$16).__nonzero__()) {
                    frame.setlocal(3, s$34);
                }
                else {
                    frame.setlocal(3, s$78._mod(frame.getlocal(2)));
                }
                frame.getlocal(4).invoke("append", frame.getglobal("_center").__call__(frame.getlocal(3), frame.getlocal(1)));
            }
            return s$75.invoke("join", frame.getlocal(4));
        }
        
        private static PyObject weekheader$11(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            /* Return a header for a week. */
            if (frame.getlocal(0)._ge(i$80).__nonzero__()) {
                frame.setlocal(2, frame.getglobal("day_name"));
            }
            else {
                frame.setlocal(2, frame.getglobal("day_abbr"));
            }
            frame.setlocal(3, new PyList(new PyObject[] {}));
            t$0$int = 0;
            t$1$PyObject = frame.getglobal("range").__call__(frame.getglobal("_firstweekday"), frame.getglobal("_firstweekday")._add(i$59));
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                frame.setlocal(1, t$0$PyObject);
                frame.getlocal(3).invoke("append", frame.getglobal("_center").__call__(frame.getlocal(2).__getitem__(frame.getlocal(1)._mod(i$59)).__getslice__(null, frame.getlocal(0), null), frame.getlocal(0)));
            }
            return s$75.invoke("join", frame.getlocal(3));
        }
        
        private static PyObject prmonth$12(PyFrame frame) {
            /* Print a month's calendar. */
            Py.printComma(frame.getglobal("month").__call__(new PyObject[] {frame.getlocal(0), frame.getlocal(1), frame.getlocal(2), frame.getlocal(3)}));
            return Py.None;
        }
        
        private static PyObject month$13(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            /* Return a month's calendar string (multi-line). */
            frame.setlocal(2, frame.getglobal("max").__call__(i$15, frame.getlocal(2)));
            frame.setlocal(3, frame.getglobal("max").__call__(i$14, frame.getlocal(3)));
            frame.setlocal(5, frame.getglobal("_center").__call__(frame.getglobal("month_name").__getitem__(frame.getlocal(1))._add(s$75)._add(frame.getlocal(0).__repr__()), i$59._mul(frame.getlocal(2)._add(i$14))._sub(i$14)).invoke("rstrip")._add(s$83._mul(frame.getlocal(3)))._add(frame.getglobal("weekheader").__call__(frame.getlocal(2)).invoke("rstrip"))._add(s$83._mul(frame.getlocal(3))));
            t$0$int = 0;
            t$1$PyObject = frame.getglobal("monthcalendar").__call__(frame.getlocal(0), frame.getlocal(1));
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                frame.setlocal(4, t$0$PyObject);
                frame.setlocal(5, frame.getlocal(5)._add(frame.getglobal("week").__call__(frame.getlocal(4), frame.getlocal(2)).invoke("rstrip"))._add(s$83._mul(frame.getlocal(3))));
            }
            return frame.getlocal(5).__getslice__(null, frame.getlocal(3).__neg__(), null)._add(s$83);
        }
        
        private static PyObject format3c$14(PyFrame frame) {
            /* Prints 3-column formatting for year calendars */
            Py.println(frame.getglobal("format3cstring").__call__(new PyObject[] {frame.getlocal(0), frame.getlocal(1), frame.getlocal(2), frame.getlocal(3), frame.getlocal(4)}));
            return Py.None;
        }
        
        private static PyObject format3cstring$15(PyFrame frame) {
            /* Returns a string formatted from 3 strings, centered within 3 columns. */
            return frame.getglobal("_center").__call__(frame.getlocal(0), frame.getlocal(3))._add(s$75._mul(frame.getlocal(4)))._add(frame.getglobal("_center").__call__(frame.getlocal(1), frame.getlocal(3)))._add(s$75._mul(frame.getlocal(4)))._add(frame.getglobal("_center").__call__(frame.getlocal(2), frame.getlocal(3)));
        }
        
        private static PyObject prcal$16(PyFrame frame) {
            /* Print a year's calendar. */
            Py.printComma(frame.getglobal("calendar").__call__(new PyObject[] {frame.getlocal(0), frame.getlocal(1), frame.getlocal(2), frame.getlocal(3)}));
            return Py.None;
        }
        
        private static PyObject calendar$17(PyFrame frame) {
            // Temporary Variables
            int t$0$int, t$1$int, t$2$int, t$3$int;
            PyObject t$0$PyObject, t$1$PyObject, t$2$PyObject, t$3$PyObject, t$4$PyObject, t$5$PyObject, t$6$PyObject, t$7$PyObject;
            
            // Code
            /* Returns a year's calendar as a multi-line string. */
            frame.setlocal(1, frame.getglobal("max").__call__(i$15, frame.getlocal(1)));
            frame.setlocal(2, frame.getglobal("max").__call__(i$14, frame.getlocal(2)));
            frame.setlocal(3, frame.getglobal("max").__call__(i$15, frame.getlocal(3)));
            frame.setlocal(9, frame.getlocal(1)._add(i$14)._mul(i$59)._sub(i$14));
            frame.setlocal(6, frame.getglobal("_center").__call__(frame.getlocal(0).__repr__(), frame.getlocal(9)._mul(i$84)._add(frame.getlocal(3)._mul(i$15))).invoke("rstrip")._add(s$83._mul(frame.getlocal(2))));
            frame.setlocal(12, frame.getglobal("weekheader").__call__(frame.getlocal(1)));
            frame.setlocal(12, frame.getglobal("format3cstring").__call__(new PyObject[] {frame.getlocal(12), frame.getlocal(12), frame.getlocal(12), frame.getlocal(9), frame.getlocal(3)}).invoke("rstrip"));
            t$0$int = 0;
            t$1$PyObject = frame.getglobal("range").__call__(frame.getglobal("January"), frame.getglobal("January")._add(i$70), i$84);
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                frame.setlocal(8, t$0$PyObject);
                frame.setlocal(6, frame.getlocal(6)._add(s$83._mul(frame.getlocal(2)))._add(frame.getglobal("format3cstring").__call__(new PyObject[] {frame.getglobal("month_name").__getitem__(frame.getlocal(8)), frame.getglobal("month_name").__getitem__(frame.getlocal(8)._add(i$14)), frame.getglobal("month_name").__getitem__(frame.getlocal(8)._add(i$15)), frame.getlocal(9), frame.getlocal(3)}).invoke("rstrip"))._add(s$83._mul(frame.getlocal(2)))._add(frame.getlocal(12))._add(s$83._mul(frame.getlocal(2))));
                frame.setlocal(13, new PyList(new PyObject[] {}));
                frame.setlocal(7, i$16);
                t$1$int = 0;
                t$3$PyObject = frame.getglobal("range").__call__(frame.getlocal(8), frame.getlocal(8)._add(i$84));
                while ((t$2$PyObject = t$3$PyObject.__finditem__(t$1$int++)) != null) {
                    frame.setlocal(10, t$2$PyObject);
                    frame.setlocal(5, frame.getglobal("monthcalendar").__call__(frame.getlocal(0), frame.getlocal(10)));
                    if (frame.getglobal("len").__call__(frame.getlocal(5))._gt(frame.getlocal(7)).__nonzero__()) {
                        frame.setlocal(7, frame.getglobal("len").__call__(frame.getlocal(5)));
                    }
                    frame.getlocal(13).invoke("append", frame.getlocal(5));
                }
                t$2$int = 0;
                t$5$PyObject = frame.getglobal("range").__call__(frame.getlocal(7));
                while ((t$4$PyObject = t$5$PyObject.__finditem__(t$2$int++)) != null) {
                    frame.setlocal(11, t$4$PyObject);
                    frame.setlocal(4, new PyList(new PyObject[] {}));
                    t$3$int = 0;
                    t$7$PyObject = frame.getlocal(13);
                    while ((t$6$PyObject = t$7$PyObject.__finditem__(t$3$int++)) != null) {
                        frame.setlocal(5, t$6$PyObject);
                        if (frame.getlocal(11)._ge(frame.getglobal("len").__call__(frame.getlocal(5))).__nonzero__()) {
                            frame.getlocal(4).invoke("append", s$34);
                        }
                        else {
                            frame.getlocal(4).invoke("append", frame.getglobal("week").__call__(frame.getlocal(5).__getitem__(frame.getlocal(11)), frame.getlocal(1)));
                        }
                    }
                    frame.setlocal(6, frame.getlocal(6)._add(frame.getglobal("format3cstring").__call__(new PyObject[] {frame.getlocal(4).__getitem__(i$16), frame.getlocal(4).__getitem__(i$14), frame.getlocal(4).__getitem__(i$15), frame.getlocal(9), frame.getlocal(3)}).invoke("rstrip"))._add(s$83._mul(frame.getlocal(2))));
                }
            }
            return frame.getlocal(6).__getslice__(null, frame.getlocal(2).__neg__(), null)._add(s$83);
        }
        
        private static PyObject timegm$18(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyObject[] t$0$PyObject__;
            PyObject t$0$PyObject, t$1$PyObject, t$2$PyObject;
            
            // Code
            /* Unrelated but handy function to calculate Unix timestamp from GMT. */
            t$0$PyObject__ = org.python.core.Py.unpackSequence(frame.getlocal(0).__getslice__(null, i$68, null), 6);
            frame.setlocal(7, t$0$PyObject__[0]);
            frame.setlocal(6, t$0$PyObject__[1]);
            frame.setlocal(8, t$0$PyObject__[2]);
            frame.setlocal(4, t$0$PyObject__[3]);
            frame.setlocal(2, t$0$PyObject__[4]);
            frame.setlocal(1, t$0$PyObject__[5]);
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(frame.getlocal(7)._ge(frame.getglobal("EPOCH")));
            if (frame.getglobal("__debug__").__nonzero__()) Py.assert(i$14._le(t$0$PyObject = frame.getlocal(6)).__nonzero__() ? t$0$PyObject._le(i$70) : Py.Zero);
            frame.setlocal(11, i$91._mul(frame.getlocal(7)._sub(frame.getglobal("EPOCH")))._add(frame.getglobal("leapdays").__call__(frame.getglobal("EPOCH"), frame.getlocal(7))));
            t$0$int = 0;
            t$1$PyObject = frame.getglobal("range").__call__(i$14, frame.getlocal(6));
            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                frame.setlocal(5, t$0$PyObject);
                frame.setlocal(11, frame.getlocal(11)._add(frame.getglobal("mdays").__getitem__(frame.getlocal(5))));
            }
            if (((t$2$PyObject = frame.getlocal(6)._gt(i$15)).__nonzero__() ? frame.getglobal("isleap").__call__(frame.getlocal(7)) : t$2$PyObject).__nonzero__()) {
                frame.setlocal(11, frame.getlocal(11)._add(i$14));
            }
            frame.setlocal(11, frame.getlocal(11)._add(frame.getlocal(8))._sub(i$14));
            frame.setlocal(9, frame.getlocal(11)._mul(i$92)._add(frame.getlocal(4)));
            frame.setlocal(3, frame.getlocal(9)._mul(i$93)._add(frame.getlocal(2)));
            frame.setlocal(10, frame.getlocal(3)._mul(i$93)._add(frame.getlocal(1)));
            return frame.getlocal(10);
        }
        
        private static PyObject main$19(PyFrame frame) {
            frame.setglobal("__file__", s$94);
            
            PyObject[] imp_accu;
            // Temporary Variables
            PyObject[] t$0$PyObject__;
            
            // Code
            /* Calendar printing functions
            
            Note when comparing these calendars to the ones printed by cal(1): By
            default, these calendars have Monday as the first day of the week, and
            Sunday as the last (the European convention). Use setfirstweekday() to
            set the first day of the week (0=Monday, 6=Sunday). */
            imp_accu = org.python.core.imp.importFrom("time", new String[] {"localtime", "mktime"}, frame);
            frame.setlocal("localtime", imp_accu[0]);
            frame.setlocal("mktime", imp_accu[1]);
            imp_accu = null;
            frame.setlocal("__all__", new PyList(new PyObject[] {s$1, s$2, s$3, s$4, s$5, s$6, s$7, s$8, s$9, s$10, s$11, s$12, s$13}));
            frame.setlocal("error", frame.getname("ValueError"));
            frame.setlocal("January", i$14);
            frame.setlocal("February", i$15);
            frame.setlocal("mdays", new PyList(new PyObject[] {i$16, i$17, i$18, i$17, i$19, i$17, i$19, i$17, i$17, i$19, i$17, i$19, i$17}));
            frame.setlocal("day_name", new PyList(new PyObject[] {s$20, s$21, s$22, s$23, s$24, s$25, s$26}));
            frame.setlocal("day_abbr", new PyList(new PyObject[] {s$27, s$28, s$29, s$30, s$31, s$32, s$33}));
            frame.setlocal("month_name", new PyList(new PyObject[] {s$34, s$35, s$36, s$37, s$38, s$39, s$40, s$41, s$42, s$43, s$44, s$45, s$46}));
            frame.setlocal("month_abbr", new PyList(new PyObject[] {s$47, s$48, s$49, s$50, s$51, s$39, s$52, s$53, s$54, s$55, s$56, s$57, s$58}));
            t$0$PyObject__ = org.python.core.Py.unpackSequence(frame.getname("range").__call__(i$59), 7);
            frame.setlocal("MONDAY", t$0$PyObject__[0]);
            frame.setlocal("TUESDAY", t$0$PyObject__[1]);
            frame.setlocal("WEDNESDAY", t$0$PyObject__[2]);
            frame.setlocal("THURSDAY", t$0$PyObject__[3]);
            frame.setlocal("FRIDAY", t$0$PyObject__[4]);
            frame.setlocal("SATURDAY", t$0$PyObject__[5]);
            frame.setlocal("SUNDAY", t$0$PyObject__[6]);
            frame.setlocal("_firstweekday", i$16);
            frame.setlocal("firstweekday", new PyFunction(frame.f_globals, new PyObject[] {}, c$0_firstweekday));
            frame.setlocal("setfirstweekday", new PyFunction(frame.f_globals, new PyObject[] {}, c$1_setfirstweekday));
            frame.setlocal("isleap", new PyFunction(frame.f_globals, new PyObject[] {}, c$2_isleap));
            frame.setlocal("leapdays", new PyFunction(frame.f_globals, new PyObject[] {}, c$3_leapdays));
            frame.setlocal("weekday", new PyFunction(frame.f_globals, new PyObject[] {}, c$4_weekday));
            frame.setlocal("monthrange", new PyFunction(frame.f_globals, new PyObject[] {}, c$5_monthrange));
            frame.setlocal("monthcalendar", new PyFunction(frame.f_globals, new PyObject[] {}, c$6_monthcalendar));
            frame.setlocal("_center", new PyFunction(frame.f_globals, new PyObject[] {}, c$7__center));
            frame.setlocal("prweek", new PyFunction(frame.f_globals, new PyObject[] {}, c$8_prweek));
            frame.setlocal("week", new PyFunction(frame.f_globals, new PyObject[] {}, c$9_week));
            frame.setlocal("weekheader", new PyFunction(frame.f_globals, new PyObject[] {}, c$10_weekheader));
            frame.setlocal("prmonth", new PyFunction(frame.f_globals, new PyObject[] {i$16, i$16}, c$11_prmonth));
            frame.setlocal("month", new PyFunction(frame.f_globals, new PyObject[] {i$16, i$16}, c$12_month));
            frame.setlocal("_colwidth", i$59._mul(i$84)._sub(i$14));
            frame.setlocal("_spacing", i$68);
            frame.setlocal("format3c", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("_colwidth"), frame.getname("_spacing")}, c$13_format3c));
            frame.setlocal("format3cstring", new PyFunction(frame.f_globals, new PyObject[] {frame.getname("_colwidth"), frame.getname("_spacing")}, c$14_format3cstring));
            frame.setlocal("prcal", new PyFunction(frame.f_globals, new PyObject[] {i$16, i$16, frame.getname("_spacing")}, c$15_prcal));
            frame.setlocal("calendar", new PyFunction(frame.f_globals, new PyObject[] {i$16, i$16, frame.getname("_spacing")}, c$16_calendar));
            frame.setlocal("EPOCH", i$89);
            frame.setlocal("timegm", new PyFunction(frame.f_globals, new PyObject[] {}, c$17_timegm));
            return Py.None;
        }
        
    }
    public static void moduleDictInit(PyObject dict) {
        dict.__setitem__("__name__", new PyString("calendar"));
        Py.runCode(new _PyInner().getMain(), dict, dict);
    }
    
    public static void main(String[] args) throws java.lang.Exception {
        String[] newargs = new String[args.length+1];
        newargs[0] = "calendar";
        System.arraycopy(args, 0, newargs, 1, args.length);
        Py.runMain(calendar._PyInner.class, newargs, calendar.jpy$packages, calendar.jpy$mainProperties, "", new String[] {"string", "random", "util", "traceback", "sre_compile", "atexit", "sre", "sre_constants", "StringIO", "javaos", "socket", "yapm", "calendar", "repr", "copy_reg", "SocketServer", "server", "re", "linecache", "javapath", "UserDict", "copy", "threading", "stat", "PathVFS", "sre_parse"});
    }
    
}
