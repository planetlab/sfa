import org.python.core.*;

public class server extends java.lang.Object {
    static String[] jpy$mainProperties = new String[] {"python.modules.builtin", "exceptions:org.python.core.exceptions"};
    static String[] jpy$proxyProperties = new String[] {"python.modules.builtin", "exceptions:org.python.core.exceptions", "python.options.showJavaExceptions", "true"};
    static String[] jpy$packages = new String[] {"java.net", null, "java.lang", null, "org.python.core", null, "java.io", null, "java.util.zip", null};
    
    public static class _PyInner extends PyFunctionTable implements PyRunnable {
        private static PyObject s$0;
        private static PyObject i$1;
        private static PyObject s$2;
        private static PyObject s$3;
        private static PyObject s$4;
        private static PyObject s$5;
        private static PyObject s$6;
        private static PyObject s$7;
        private static PyObject i$8;
        private static PyObject i$9;
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
        private static PyObject i$36;
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
        private static PyObject i$110;
        private static PyObject s$111;
        private static PyObject s$112;
        private static PyObject i$113;
        private static PyObject s$114;
        private static PyObject s$115;
        private static PyObject s$116;
        private static PyObject s$117;
        private static PyObject s$118;
        private static PyObject s$119;
        private static PyObject s$120;
        private static PyObject s$121;
        private static PyObject s$122;
        private static PyObject s$123;
        private static PyObject s$124;
        private static PyObject s$125;
        private static PyObject s$126;
        private static PyObject s$127;
        private static PyObject s$128;
        private static PyObject s$129;
        private static PyObject s$130;
        private static PyObject s$131;
        private static PyObject s$132;
        private static PyObject s$133;
        private static PyFunctionTable funcTable;
        private static PyCode c$0_register;
        private static PyCode c$1_update;
        private static PyCode c$2_remove;
        private static PyCode c$3_lookup;
        private static PyCode c$4_list;
        private static PyCode c$5_getCredential;
        private static PyCode c$6_getAccounting;
        private static PyCode c$7___init__;
        private static PyCode c$8_construct_hierarchy;
        private static PyCode c$9_sec_init;
        private static PyCode c$10_save_state;
        private static PyCode c$11_GENIServer;
        private static PyCode c$12_handle;
        private static PyCode c$13_handle_connection;
        private static PyCode c$14_main;
        private static PyCode c$15_main;
        private static void initConstants() {
            s$0 = Py.newString("127.0.0.1");
            i$1 = Py.newInteger(8002);
            s$2 = Py.newString("interface_tree_sr");
            s$3 = Py.newString("interface_tree_cr");
            s$4 = Py.newString("../");
            s$5 = Py.newString("../util");
            s$6 = Py.newString("../util/sec");
            s$7 = Py.newString("../PLCAPI/trunk");
            i$8 = Py.newInteger(0);
            i$9 = Py.newInteger(1);
            s$10 = Py.newString("type");
            s$11 = Py.newString("g_params");
            s$12 = Py.newString("Record ");
            s$13 = Py.newString("hrn");
            s$14 = Py.newString(" already exists.\012");
            s$15 = Py.newString("SA");
            s$16 = Py.newString("MA");
            s$17 = Py.newString("local");
            s$18 = Py.newString("wrapperurl");
            s$19 = Py.newString("");
            s$20 = Py.newString("slc");
            s$21 = Py.newString("comp");
            s$22 = Py.newString("(2-0)(4-0)(6-0)(7-0)(8-0)(9-0)(0-1)(1-1)(2-1)(3-1)(4-1)(5-1)(6-1)(7-1)(8-1)(9-1)");
            s$23 = Py.newString("#0:reg:");
            s$24 = Py.newString(":");
            s$25 = Py.newString("#1:reg:");
            s$26 = Py.newString("rights");
            s$27 = Py.newString("p_params");
            s$28 = Py.newString("site_id");
            s$29 = Py.newString("SELECT site_id FROM sites WHERE login_base = '");
            s$30 = Py.newString("';");
            s$31 = Py.newString("login_base");
            s$32 = Py.newString("SELECT * FROM sites WHERE login_base = '");
            s$33 = Py.newString("'");
            s$34 = Py.newString("Site login_base '");
            s$35 = Py.newString(", already exists in the system. Try another name.\012");
            i$36 = Py.newInteger(10);
            s$37 = Py.newString("slice");
            s$38 = Py.newString("component");
            s$39 = Py.newString("/");
            s$40 = Py.newString(".");
            s$41 = Py.newString("rm -rf ");
            s$42 = Py.newString(".cert");
            s$43 = Py.newString("pubkey");
            s$44 = Py.newString("pointer");
            s$45 = Py.newString("INSERT");
            s$46 = Py.newString("DROP TABLE IF EXISTS ");
            s$47 = Py.newString("CREATE TABLE ");
            s$48 = Py.newString(" (                 hrn text,                 type text,                 uuid text,                 userlist text,                 rights text,                 description text,                 pubkey text,                 wrapperURL text,                 disabled text,                 pointer integer);");
            s$49 = Py.newString("db_info");
            s$50 = Py.newString("key_info");
            s$51 = Py.newString(".pkey");
            s$52 = Py.newString("sr");
            s$53 = Py.newString("cr");
            s$54 = Py.newString(" ");
            s$55 = Py.newString(" is successfully added.\012");
            s$56 = Py.newString("_");
            s$57 = Py.newString("name");
            s$58 = Py.newString("UPDATE ");
            s$59 = Py.newString(" SET hrn = '");
            s$60 = Py.newString("userlist");
            s$61 = Py.newString(" userlist = '");
            s$62 = Py.newString(" rights = '");
            s$63 = Py.newString(" WHERE pointer = ");
            s$64 = Py.newString("Slice ");
            s$65 = Py.newString("user");
            s$66 = Py.newString("(2-0)(4-0)(6-0)(7-0)(8-0)(9-0)");
            s$67 = Py.newString("#0:reg:slc:");
            s$68 = Py.newString("User ");
            s$69 = Py.newString("node");
            s$70 = Py.newString("Node ");
            s$71 = Py.newString("Error in 'register():");
            s$72 = Py.newString("Error in register:.");
            s$73 = Py.newString(" does not exist.\012");
            s$74 = Py.newString("geni");
            s$75 = Py.newString("INSERT INTO slice_person VALUES(");
            s$76 = Py.newString(", ");
            s$77 = Py.newString(");");
            s$78 = Py.newString("UPDATE");
            s$79 = Py.newString("The record '");
            s$80 = Py.newString("' is successfully updated.\012");
            s$81 = Py.newString("Error in 'update():'");
            s$82 = Py.newString("Error in update:");
            s$83 = Py.newString("Error in remove.\012");
            s$84 = Py.newString("Site removal should be at the leaves.\012");
            s$85 = Py.newString("DELETE");
            s$86 = Py.newString("' is successfully removed.\012");
            s$87 = Py.newString("Error in 'delete()'");
            s$88 = Py.newString("Error in delete:");
            s$89 = Py.newString("pl");
            s$90 = Py.newString("cred_name");
            s$91 = Py.newString("registry");
            s$92 = Py.newString("SELECT * FROM ");
            s$93 = Py.newString(" WHERE hrn = '");
            s$94 = Py.newString("' ");
            s$95 = Py.newString("admin");
            s$96 = Py.newString("roles");
            s$97 = Py.newString("(0-0)(1-0)(2-0)(3-0)(4-0)(5-0)(6-0)(7-0)(8-0)(9-0)");
            s$98 = Py.newString("(0-1)(1-1)(2-1)(3-1)(4-1)(5-1)(6-1)(7-1)(8-1)(9-1)");
            s$99 = Py.newString("#1:reg:comp:");
            s$100 = Py.newString("pi");
            s$101 = Py.newString("Registry credentials");
            s$102 = Py.newString("is_deleted");
            s$103 = Py.newString("expires");
            s$104 = Py.newString("f");
            s$105 = Py.newString("SELECT * FROM person_slice WHERE person_id = ");
            s$106 = Py.newString(" AND slice_id = ");
            s$107 = Py.newString("(10-0)(11-0)(12-0)(13-0)(14-0)(15-0)(16-0)(17-0)(18-0)(20-0)(21-0)(22-0)(23-0)");
            s$108 = Py.newString("#0:comp:planetlab.*");
            s$109 = Py.newString("Credential ");
            i$110 = Py.newInteger(3);
            s$111 = Py.newString("account_name");
            s$112 = Py.newString("uuid");
            i$113 = Py.newInteger(2);
            s$114 = Py.newString("register");
            s$115 = Py.newString("remove");
            s$116 = Py.newString("update");
            s$117 = Py.newString("lookup");
            s$118 = Py.newString("list");
            s$119 = Py.newString("getCredential");
            s$120 = Py.newString("getAccounting");
            s$121 = Py.newString("server");
            s$122 = Py.newString("accounting");
            s$123 = Py.newString("credential");
            s$124 = Py.newString("both");
            s$125 = Py.newString("opname");
            s$126 = Py.newString("WRONG INTERFACE");
            s$127 = Py.newString("NO FUNC");
            s$128 = Py.newString("AUTHORIZATION FAIL");
            s$129 = Py.newString("message");
            s$130 = Py.newString("Requested record does not exist.\012");
            s$131 = Py.newString("There is an error handling the request. ");
            s$132 = Py.newString("__main__");
            s$133 = Py.newString("/home/soners/work/geni/rpc/server/server.py");
            funcTable = new _PyInner();
            c$0_register = Py.newCode(3, new String[] {"self", "record", "dbinfo", "other_tree", "parent_key_info", "user_fields", "existing_res", "login_base", "slice_fields", "rights", "reg_type", "querystr", "cnx", "pointer", "tree", "new_table_name", "table", "dirname", "parent_data", "site_fields", "res", "parent_db_info", "db_info", "curdir", "node_fields", "hrn_suffix", "i", "info", "long_hrn", "e", "dir_type", "key_info", "type"}, "/home/soners/work/geni/rpc/server/server.py", "register", false, false, funcTable, 0, null, null, 0, 1);
            c$1_update = Py.newCode(3, new String[] {"self", "record", "dbinfo", "usr_dbinfo", "type", "user_pointer", "rec", "existing_res", "user_fields", "pl_res", "node_fields", "cnx", "site_fields", "pointer", "querystr", "e", "table", "long_hrn", "slice_fields", "user"}, "/home/soners/work/geni/rpc/server/server.py", "update", false, false, funcTable, 1, null, null, 0, 1);
            c$2_remove = Py.newCode(3, new String[] {"self", "record", "dbinfo", "type", "existing_res", "tree", "cnx", "pointer", "querystr", "hrn_suffix", "leaf", "e", "table", "long_hrn"}, "/home/soners/work/geni/rpc/server/server.py", "remove", false, false, funcTable, 2, null, null, 0, 1);
            c$3_lookup = Py.newCode(3, new String[] {"self", "record", "dbinfo", "pointer", "cnx", "type", "existing_res", "pl_res", "table"}, "/home/soners/work/geni/rpc/server/server.py", "lookup", false, false, funcTable, 3, null, null, 0, 1);
            c$4_list = Py.newCode(3, new String[] {"self", "record", "dbinfo", "x"}, "/home/soners/work/geni/rpc/server/server.py", "list", false, false, funcTable, 4, null, null, 0, 1);
            c$5_getCredential = Py.newCode(5, new String[] {"self", "record", "dbinfo", "keyinfo", "peerinfo", "openssl_cert", "usr_dbinfo", "cname", "has_slc", "cred_name", "slc_result", "expires", "rights", "querystr", "cnx", "pointer", "table", "usr_slc_res", "user_pointer", "cred_pem", "slc_rec", "rec", "deleted", "pl_res", "timenow", "geni_res", "type"}, "/home/soners/work/geni/rpc/server/server.py", "getCredential", false, false, funcTable, 5, null, null, 0, 1);
            c$6_getAccounting = Py.newCode(5, new String[] {"self", "record", "dbinfo", "keyinfo", "peer_cert", "uuid", "cnx", "openssl_cert", "rec", "acc", "res", "table"}, "/home/soners/work/geni/rpc/server/server.py", "getAccounting", false, false, funcTable, 6, null, null, 0, 1);
            c$7___init__ = Py.newCode(3, new String[] {"self", "socket", "handler"}, "/home/soners/work/geni/rpc/server/server.py", "__init__", false, false, funcTable, 7, null, null, 0, 1);
            c$8_construct_hierarchy = Py.newCode(1, new String[] {"self"}, "/home/soners/work/geni/rpc/server/server.py", "construct_hierarchy", false, false, funcTable, 8, null, null, 0, 1);
            c$9_sec_init = Py.newCode(1, new String[] {"self", "id_key_file", "acc_file", "id_file", "key_info", "cred_file"}, "/home/soners/work/geni/rpc/server/server.py", "sec_init", false, false, funcTable, 9, null, null, 0, 1);
            c$10_save_state = Py.newCode(2, new String[] {"self", "type"}, "/home/soners/work/geni/rpc/server/server.py", "save_state", false, false, funcTable, 10, null, null, 0, 1);
            c$11_GENIServer = Py.newCode(0, new String[] {}, "/home/soners/work/geni/rpc/server/server.py", "GENIServer", false, false, funcTable, 11, null, null, 0, 0);
            c$12_handle = Py.newCode(1, new String[] {"self", "type", "op", "peerinfo", "target_hrn", "result", "peer", "dbinfo", "tree", "operation_request", "opname", "hrn_of_call", "reg_type", "e", "params", "keyinfo"}, "/home/soners/work/geni/rpc/server/server.py", "handle", false, false, funcTable, 12, null, null, 0, 1);
            c$13_handle_connection = Py.newCode(0, new String[] {}, "/home/soners/work/geni/rpc/server/server.py", "handle_connection", false, false, funcTable, 13, null, null, 0, 0);
            c$14_main = Py.newCode(0, new String[] {}, "/home/soners/work/geni/rpc/server/server.py", "main", false, false, funcTable, 14, null, null, 0, 1);
            c$15_main = Py.newCode(0, new String[] {}, "/home/soners/work/geni/rpc/server/server.py", "main", false, false, funcTable, 15, null, null, 0, 0);
        }
        
        
        public PyCode getMain() {
            if (c$15_main == null) _PyInner.initConstants();
            return c$15_main;
        }
        
        public PyObject call_function(int index, PyFrame frame) {
            switch (index){
                case 0:
                return _PyInner.register$1(frame);
                case 1:
                return _PyInner.update$2(frame);
                case 2:
                return _PyInner.remove$3(frame);
                case 3:
                return _PyInner.lookup$4(frame);
                case 4:
                return _PyInner.list$5(frame);
                case 5:
                return _PyInner.getCredential$6(frame);
                case 6:
                return _PyInner.getAccounting$7(frame);
                case 7:
                return _PyInner.__init__$8(frame);
                case 8:
                return _PyInner.construct_hierarchy$9(frame);
                case 9:
                return _PyInner.sec_init$10(frame);
                case 10:
                return _PyInner.save_state$11(frame);
                case 11:
                return _PyInner.GENIServer$12(frame);
                case 12:
                return _PyInner.handle$13(frame);
                case 13:
                return _PyInner.handle_connection$14(frame);
                case 14:
                return _PyInner.main$15(frame);
                case 15:
                return _PyInner.main$16(frame);
                default:
                return null;
            }
        }
        
        private static PyObject register$1(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyException t$0$PyException;
            PyObject t$0$PyObject, t$1$PyObject, t$2$PyObject;
            
            // Code
            frame.setlocal(12, frame.getlocal(2).__getitem__(i$8));
            frame.setlocal(16, frame.getlocal(2).__getitem__(i$9));
            frame.setlocal(32, frame.getlocal(1).__getitem__(s$11).__getitem__(s$10));
            try {
                frame.setlocal(6, frame.getglobal("check_exists_geni").__call__(frame.getlocal(1), frame.getlocal(2)));
                if (frame.getlocal(6).__nonzero__()) {
                    throw Py.makeException(frame.getglobal("ExistingRecord").__call__(s$12._add(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13))._add(s$14)));
                }
                if (((t$0$PyObject = frame.getlocal(32)._eq(s$15)).__nonzero__() ? t$0$PyObject : frame.getlocal(32)._eq(s$16)).__nonzero__()) {
                    frame.getlocal(1).__getitem__(s$11).__setitem__(s$18, s$17);
                    frame.setlocal(10, s$19);
                    if (frame.getlocal(32)._eq(s$15).__nonzero__()) {
                        frame.setlocal(10, s$20);
                    }
                    else {
                        frame.setlocal(10, s$21);
                    }
                    frame.setlocal(9, s$22);
                    frame.setlocal(9, frame.getlocal(9)._add(s$23)._add(frame.getlocal(10))._add(s$24)._add(frame.getglobal("obtain_authority").__call__(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13)))._add(s$25)._add(frame.getlocal(10))._add(s$24)._add(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13)));
                    frame.getlocal(1).__getitem__(s$11).__setitem__(s$26, frame.getlocal(9));
                    frame.setlocal(28, frame.getlocal(1).__getitem__(s$11).__getitem__(s$13));
                    frame.setlocal(25, frame.getglobal("get_leaf").__call__(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13)));
                    frame.setlocal(13, i$9.__neg__());
                    frame.setlocal(7, s$19);
                    frame.setlocal(19, frame.getlocal(1).__getitem__(s$27));
                    frame.setlocal(3, frame.getglobal("None"));
                    if (frame.getlocal(10)._eq(s$20).__nonzero__()) {
                        frame.setlocal(3, frame.getlocal(0).__getattr__("cr_tree"));
                    }
                    else {
                        frame.setlocal(3, frame.getlocal(0).__getattr__("sr_tree"));
                    }
                    frame.setlocal(27, frame.getlocal(3).invoke("tree_lookup", frame.getlocal(28)));
                    if (frame.getlocal(27).__nonzero__()) {
                        frame.setlocal(7, frame.getlocal(27).__getattr__("login_base"));
                        frame.setlocal(13, frame.getlocal(12).invoke("query", s$29._add(frame.getlocal(7))._add(s$30)).invoke("dictresult").__getitem__(i$8).__getitem__(s$28));
                    }
                    else {
                        if (frame.getlocal(19).invoke("has_key", s$31).__nonzero__()) {
                            frame.setlocal(7, frame.getlocal(19).__getitem__(s$31));
                            frame.setlocal(11, s$32._add(frame.getlocal(7))._add(s$33));
                            frame.setlocal(20, frame.getlocal(12).invoke("query", frame.getlocal(11)).invoke("dictresult"));
                            if (frame.getlocal(20).__nonzero__()) {
                                return s$34._add(frame.getlocal(7))._add(s$35);
                            }
                        }
                        else {
                            frame.setlocal(7, frame.getglobal("hrn_to_loginbase").__call__(frame.getlocal(28)));
                            t$0$int = 0;
                            t$1$PyObject = frame.getglobal("range").__call__(i$9, i$36);
                            while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                                frame.setlocal(26, t$0$PyObject);
                                frame.setlocal(11, s$32._add(frame.getlocal(7))._add(s$33));
                                frame.setlocal(20, frame.getlocal(12).invoke("query", frame.getlocal(11)).invoke("dictresult"));
                                if (frame.getlocal(20).__not__().__nonzero__()) {
                                    break;
                                }
                                else {
                                    frame.setlocal(7, frame.getglobal("hrn_to_loginbase").__call__(frame.getlocal(28), frame.getlocal(26)));
                                }
                            }
                            frame.getlocal(19).__setitem__(s$31, frame.getlocal(7));
                        }
                        frame.setlocal(13, frame.getglobal("shell").invoke("AddSite", frame.getglobal("pl_auth"), frame.getlocal(19)));
                    }
                    frame.setlocal(23, frame.getglobal("os").__getattr__("getcwd").__call__());
                    if (frame.getlocal(10)._eq(s$20).__nonzero__()) {
                        frame.setlocal(30, s$37);
                    }
                    else {
                        frame.setlocal(30, s$38);
                    }
                    frame.setlocal(17, frame.getlocal(30)._add(s$39)._add(frame.getlocal(28).invoke("replace", s$40, s$39)));
                    if (frame.getglobal("os").__getattr__("path").__getattr__("exists").__call__(frame.getlocal(17)).__nonzero__()) {
                        frame.getglobal("os").__getattr__("system").__call__(s$41._add(frame.getlocal(17)));
                    }
                    frame.getglobal("os").__getattr__("makedirs").__call__(frame.getlocal(17));
                    frame.getglobal("os").__getattr__("chdir").__call__(frame.getlocal(17));
                    frame.getglobal("create_self_cert").__call__(frame.getlocal(25));
                    frame.getglobal("os").__getattr__("chdir").__call__(frame.getlocal(23));
                    frame.getlocal(1).__getitem__(s$11).__setitem__(s$13, frame.getglobal("get_leaf").__call__(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13)));
                    frame.getlocal(1).__getitem__(s$11).__setitem__(s$43, frame.getglobal("X509").__getattr__("load_cert").__call__(frame.getlocal(17)._add(s$39)._add(frame.getlocal(25))._add(s$42)).invoke("get_pubkey").__getattr__("as_pem").__call__(new PyObject[] {frame.getglobal("None")}, new String[] {"cipher"}));
                    frame.getlocal(1).__getitem__(s$11).__setitem__(s$44, frame.getlocal(13));
                    frame.setlocal(11, frame.getglobal("generate_querystr").__call__(s$45, frame.getlocal(16), frame.getlocal(1).__getitem__(s$11)));
                    frame.getlocal(12).invoke("query", frame.getlocal(11));
                    frame.setlocal(15, frame.getglobal("hrn_to_tablename").__call__(frame.getlocal(28), frame.getlocal(10)));
                    frame.getlocal(12).invoke("query", s$46._add(frame.getlocal(15)));
                    frame.setlocal(11, s$47._add(frame.getlocal(15))._add(s$48));
                    frame.getlocal(12).invoke("query", frame.getlocal(11));
                    frame.setlocal(14, frame.getglobal("None"));
                    if (frame.getlocal(32)._eq(s$15).__nonzero__()) {
                        frame.setlocal(14, frame.getlocal(0).__getattr__("sr_tree"));
                    }
                    else {
                        frame.setlocal(14, frame.getlocal(0).__getattr__("cr_tree"));
                    }
                    frame.setlocal(18, frame.getlocal(14).invoke("tree_lookup", frame.getglobal("obtain_authority").__call__(frame.getlocal(28))).__getattr__("node_data"));
                    frame.setlocal(21, frame.getlocal(18).__getitem__(s$49));
                    frame.setlocal(4, frame.getlocal(18).__getitem__(s$50));
                    frame.setlocal(27, frame.getglobal("TreeNodeInfo").__call__());
                    frame.getlocal(27).__setattr__("name", frame.getlocal(28));
                    frame.getlocal(27).__setattr__("login_base", frame.getlocal(7));
                    frame.setlocal(22, frame.getglobal("DbInfo").__call__());
                    frame.setlocal(31, frame.getglobal("KeyInfo").__call__());
                    frame.getlocal(27).__setattr__("node_data", new PyDictionary(new PyObject[] {s$49, frame.getlocal(22), s$50, frame.getlocal(31)}));
                    frame.getlocal(22).__setattr__("table_name", frame.getlocal(15));
                    frame.getlocal(22).__setattr__("db_name", frame.getlocal(21).__getattr__("db_name"));
                    frame.getlocal(22).__setattr__("address", frame.getlocal(21).__getattr__("address"));
                    frame.getlocal(22).__setattr__("port", frame.getlocal(21).__getattr__("port"));
                    frame.getlocal(22).__setattr__("user", frame.getlocal(21).__getattr__("user"));
                    frame.getlocal(22).__setattr__("password", frame.getlocal(21).__getattr__("password"));
                    frame.getlocal(31).__setattr__("acc_file", s$19);
                    frame.getlocal(31).__setattr__("cred_file", s$19);
                    frame.getlocal(31).__setattr__("folder", frame.getlocal(4).__getattr__("folder")._add(s$39)._add(frame.getlocal(25)));
                    frame.getlocal(31).__setattr__("id_file", frame.getlocal(25)._add(s$42));
                    frame.getlocal(31).__setattr__("id_key_file", frame.getlocal(25)._add(s$51));
                    frame.getlocal(14).invoke("tree_add", frame.getlocal(27));
                    if (frame.getlocal(32)._eq(s$15).__nonzero__()) {
                        frame.getlocal(0).invoke("save_state", s$52);
                    }
                    else {
                        frame.getlocal(0).invoke("save_state", s$53);
                    }
                    return frame.getlocal(32)._add(s$54)._add(frame.getlocal(28))._add(s$55);
                }
                else if (frame.getlocal(32)._eq(s$37).__nonzero__()) {
                    frame.setlocal(7, frame.getglobal("get_leaf").__call__(frame.getglobal("obtain_authority").__call__(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13))));
                    frame.setlocal(28, frame.getlocal(1).__getitem__(s$11).__getitem__(s$13));
                    frame.setlocal(25, frame.getglobal("get_leaf").__call__(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13)));
                    frame.setlocal(8, frame.getlocal(1).__getitem__(s$27));
                    frame.getlocal(8).__setitem__(s$57, frame.getlocal(7)._add(s$56)._add(frame.getlocal(25)));
                    frame.setlocal(13, frame.getglobal("shell").invoke("AddSlice", frame.getglobal("pl_auth"), frame.getlocal(8)));
                    frame.getlocal(1).__getitem__(s$11).__setitem__(s$44, frame.getlocal(13));
                    frame.setlocal(11, s$58._add(frame.getlocal(16))._add(s$59)._add(frame.getlocal(25))._add(s$33));
                    if (frame.getlocal(1).__getitem__(s$11).invoke("has_key", s$60).__nonzero__()) {
                        frame.setlocal(11, frame.getlocal(11)._add(s$61)._add(frame.getlocal(1).__getitem__(s$11).__getitem__(s$60))._add(s$33));
                    }
                    if (frame.getlocal(1).__getitem__(s$11).invoke("has_key", s$26).__nonzero__()) {
                        frame.setlocal(11, frame.getlocal(11)._add(s$62)._add(frame.getlocal(1).__getitem__(s$11).__getitem__(s$26))._add(s$33));
                    }
                    frame.setlocal(11, frame.getlocal(11)._add(s$63)._add(frame.getglobal("str").__call__(frame.getlocal(1).__getitem__(s$11).__getitem__(s$44))));
                    frame.getlocal(12).invoke("query", frame.getlocal(11));
                    return s$64._add(frame.getlocal(28))._add(s$55);
                }
                else if (frame.getlocal(32)._eq(s$65).__nonzero__()) {
                    frame.setlocal(28, frame.getlocal(1).__getitem__(s$11).__getitem__(s$13));
                    frame.getlocal(1).__getitem__(s$11).__setitem__(s$13, frame.getglobal("get_leaf").__call__(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13)));
                    frame.setlocal(9, s$66);
                    frame.setlocal(9, frame.getlocal(9)._add(s$67)._add(frame.getglobal("obtain_authority").__call__(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13))));
                    frame.getlocal(1).__getitem__(s$11).__setitem__(s$26, frame.getlocal(9));
                    frame.setlocal(5, frame.getlocal(1).__getitem__(s$27));
                    frame.setlocal(13, frame.getglobal("shell").invoke("AddPerson", frame.getglobal("pl_auth"), frame.getlocal(5)));
                    frame.getlocal(1).__getitem__(s$11).__setitem__(s$44, frame.getlocal(13));
                    frame.setlocal(11, frame.getglobal("generate_querystr").__call__(s$45, frame.getlocal(16), frame.getlocal(1).__getitem__(s$11)));
                    frame.getlocal(12).invoke("query", frame.getlocal(11));
                    return s$68._add(frame.getlocal(28))._add(s$55);
                }
                else if (frame.getlocal(32)._eq(s$69).__nonzero__()) {
                    frame.setlocal(28, frame.getlocal(1).__getitem__(s$11).__getitem__(s$13));
                    frame.setlocal(7, frame.getlocal(0).__getattr__("cr_tree").invoke("tree_lookup", frame.getglobal("obtain_authority").__call__(frame.getlocal(28))).__getattr__("login_base"));
                    frame.getlocal(1).__getitem__(s$11).__setitem__(s$13, frame.getglobal("get_leaf").__call__(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13)));
                    frame.setlocal(9, s$19);
                    frame.getlocal(1).__getitem__(s$11).__setitem__(s$26, frame.getlocal(9));
                    frame.setlocal(24, frame.getlocal(1).__getitem__(s$27));
                    frame.setlocal(13, frame.getglobal("shell").invoke("AddNode", new PyObject[] {frame.getglobal("pl_auth"), frame.getlocal(7), frame.getlocal(24)}));
                    frame.getlocal(1).__getitem__(s$11).__setitem__(s$44, frame.getlocal(13));
                    frame.setlocal(11, s$58._add(frame.getlocal(16))._add(s$59)._add(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13))._add(s$33));
                    if (((t$2$PyObject = frame.getlocal(1).__getitem__(s$11).invoke("has_key", s$26)).__nonzero__() ? frame.getlocal(1).__getitem__(s$11).__getitem__(s$26)._ne(s$19) : t$2$PyObject).__nonzero__()) {
                        frame.setlocal(11, frame.getlocal(11)._add(s$62)._add(frame.getlocal(1).__getitem__(s$11).__getitem__(s$26))._add(s$33));
                    }
                    frame.setlocal(11, frame.getlocal(11)._add(s$63)._add(frame.getglobal("str").__call__(frame.getlocal(1).__getitem__(s$11).__getitem__(s$44))));
                    frame.getlocal(12).invoke("query", frame.getlocal(11));
                    return s$70._add(frame.getlocal(28))._add(s$55);
                }
            }
            catch (Throwable x$0) {
                t$0$PyException = Py.setException(x$0, frame);
                if (Py.matchException(t$0$PyException, frame.getglobal("Exception"))) {
                    frame.setlocal(29, t$0$PyException.value);
                    Py.println(s$71._add(frame.getglobal("str").__call__(frame.getlocal(29))));
                    return s$72._add(frame.getglobal("str").__call__(frame.getlocal(29)));
                }
                else throw t$0$PyException;
            }
            return Py.None;
        }
        
        private static PyObject update$2(PyFrame frame) {
            // Temporary Variables
            int t$0$int;
            PyException t$0$PyException;
            PyObject t$0$PyObject, t$1$PyObject;
            
            // Code
            frame.setlocal(11, frame.getlocal(2).__getitem__(i$8));
            frame.setlocal(16, frame.getlocal(2).__getitem__(i$9));
            try {
                frame.setlocal(7, frame.getglobal("check_exists_geni").__call__(frame.getlocal(1), frame.getlocal(2)));
                if (frame.getlocal(7).__not__().__nonzero__()) {
                    throw Py.makeException(frame.getglobal("NonexistingRecord").__call__(s$12._add(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13))._add(s$73)));
                }
                frame.setlocal(4, frame.getlocal(7).__getitem__(s$10));
                frame.setlocal(13, frame.getlocal(7).__getitem__(s$44));
                frame.setlocal(17, frame.getlocal(1).__getitem__(s$11).__getitem__(s$13));
                if (((t$0$PyObject = frame.getlocal(4)._eq(s$15)).__nonzero__() ? frame.getlocal(13)._ne(i$9.__neg__()) : t$0$PyObject).__nonzero__()) {
                    frame.setlocal(9, frame.getglobal("shell").invoke("GetSites", frame.getglobal("pl_auth"), new PyList(new PyObject[] {frame.getlocal(13)})));
                    if (frame.getlocal(9).__not__().__nonzero__()) {
                        frame.getlocal(0).invoke("remove", frame.getlocal(1), frame.getlocal(2));
                        throw Py.makeException(frame.getglobal("NonexistingRecord").__call__(s$12._add(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13))._add(s$73)));
                    }
                    frame.setlocal(12, frame.getlocal(1).__getitem__(s$27));
                    frame.getglobal("shell").invoke("UpdateSite", new PyObject[] {frame.getglobal("pl_auth"), frame.getlocal(13), frame.getlocal(12)});
                }
                else if (((t$0$PyObject = frame.getlocal(4)._eq(s$16)).__nonzero__() ? frame.getlocal(13)._ne(i$9.__neg__()) : t$0$PyObject).__nonzero__()) {
                    frame.setlocal(9, frame.getglobal("shell").invoke("GetSites", frame.getglobal("pl_auth"), new PyList(new PyObject[] {frame.getlocal(13)})));
                    if (frame.getlocal(9).__not__().__nonzero__()) {
                        frame.getlocal(0).invoke("remove", frame.getlocal(1), frame.getlocal(2));
                        throw Py.makeException(frame.getglobal("NonexistingRecord").__call__(s$12._add(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13))._add(s$73)));
                    }
                    frame.setlocal(12, frame.getlocal(1).__getitem__(s$27));
                    frame.getglobal("shell").invoke("UpdateSite", new PyObject[] {frame.getglobal("pl_auth"), frame.getlocal(13), frame.getlocal(12)});
                }
                else if (frame.getlocal(4)._eq(s$37).__nonzero__()) {
                    frame.setlocal(9, frame.getglobal("shell").invoke("GetSlices", frame.getglobal("pl_auth"), new PyList(new PyObject[] {frame.getlocal(13)})));
                    if (frame.getlocal(9).__not__().__nonzero__()) {
                        frame.getlocal(0).invoke("remove", frame.getlocal(1), frame.getlocal(2));
                        throw Py.makeException(frame.getglobal("NonexistingRecord").__call__(s$12._add(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13))._add(s$73)));
                    }
                    frame.setlocal(18, frame.getlocal(1).__getitem__(s$27));
                    frame.getglobal("shell").invoke("UpdateSlice", new PyObject[] {frame.getglobal("pl_auth"), frame.getlocal(13), frame.getlocal(18)});
                    t$0$int = 0;
                    t$1$PyObject = frame.getlocal(1).__getitem__(s$11).__getitem__(s$60);
                    while ((t$0$PyObject = t$1$PyObject.__finditem__(t$0$int++)) != null) {
                        frame.setlocal(19, t$0$PyObject);
                        frame.setlocal(3, frame.getglobal("determine_dbinfo").__call__(frame.getglobal("get_authority").__call__(frame.getlocal(19)), frame.getlocal(0).__getattr__("tree")));
                        if (frame.getlocal(3).__nonzero__()) {
                            frame.setlocal(6, new PyDictionary(new PyObject[] {s$11, new PyDictionary(new PyObject[] {s$13, frame.getlocal(19)}), s$27, new PyDictionary(new PyObject[] {})}));
                            frame.setlocal(5, frame.getlocal(0).invoke("lookup", frame.getlocal(6), frame.getlocal(3)).__getitem__(s$74).__getitem__(s$44));
                            frame.setlocal(14, s$75._add(frame.getlocal(13))._add(s$76)._add(frame.getlocal(5))._add(s$77));
                            frame.getlocal(11).invoke("query", frame.getlocal(14));
                        }
                    }
                }
                else if (frame.getlocal(4)._eq(s$65).__nonzero__()) {
                    frame.setlocal(9, frame.getglobal("shell").invoke("GetPersons", frame.getglobal("pl_auth"), new PyList(new PyObject[] {frame.getlocal(13)})));
                    if (frame.getlocal(9).__not__().__nonzero__()) {
                        frame.getlocal(0).invoke("remove", frame.getlocal(1), frame.getlocal(2));
                        throw Py.makeException(frame.getglobal("NonexistingRecord").__call__(s$12._add(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13))._add(s$73)));
                    }
                    frame.setlocal(8, frame.getlocal(1).__getitem__(s$27));
                    frame.getglobal("shell").invoke("UpdatePerson", new PyObject[] {frame.getglobal("pl_auth"), frame.getlocal(13), frame.getlocal(8)});
                }
                else if (frame.getlocal(4)._eq(s$69).__nonzero__()) {
                    frame.setlocal(9, frame.getglobal("shell").invoke("GetNodes", frame.getglobal("pl_auth"), new PyList(new PyObject[] {frame.getlocal(13)})));
                    if (frame.getlocal(9).__not__().__nonzero__()) {
                        frame.getlocal(0).invoke("remove", frame.getlocal(1), frame.getlocal(2));
                        throw Py.makeException(frame.getglobal("NonexistingRecord").__call__(s$12._add(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13))._add(s$73)));
                    }
                    frame.setlocal(10, frame.getlocal(1).__getitem__(s$27));
                    frame.getglobal("shell").invoke("UpdateNode", new PyObject[] {frame.getglobal("pl_auth"), frame.getlocal(13), frame.getlocal(10)});
                }
                frame.getlocal(1).__getitem__(s$11).__setitem__(s$13, frame.getglobal("get_leaf").__call__(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13)));
                frame.setlocal(14, frame.getglobal("generate_querystr").__call__(s$78, frame.getlocal(16), frame.getlocal(1).__getitem__(s$11)));
                frame.getlocal(11).invoke("query", frame.getlocal(14));
                return s$79._add(frame.getlocal(17))._add(s$80);
            }
            catch (Throwable x$0) {
                t$0$PyException = Py.setException(x$0, frame);
                if (Py.matchException(t$0$PyException, frame.getglobal("Exception"))) {
                    frame.setlocal(15, t$0$PyException.value);
                    Py.println(s$81._add(frame.getglobal("str").__call__(frame.getlocal(15))));
                    return s$82._add(frame.getglobal("str").__call__(frame.getlocal(15)));
                }
                else throw t$0$PyException;
            }
        }
        
        private static PyObject remove$3(PyFrame frame) {
            // Temporary Variables
            PyException t$0$PyException;
            PyObject t$0$PyObject;
            
            // Code
            frame.setlocal(6, frame.getlocal(2).__getitem__(i$8));
            frame.setlocal(12, frame.getlocal(2).__getitem__(i$9));
            try {
                frame.setlocal(13, frame.getlocal(1).__getitem__(s$11).__getitem__(s$13));
                frame.setlocal(9, frame.getglobal("get_leaf").__call__(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13)));
                frame.setlocal(4, frame.getglobal("check_exists_geni").__call__(frame.getlocal(1), frame.getlocal(2)));
                if (frame.getlocal(4).__not__().__nonzero__()) {
                    throw Py.makeException(frame.getglobal("NonexistingRecord").__call__(s$12._add(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13))._add(s$73)));
                }
                frame.setlocal(3, frame.getlocal(4).__getitem__(s$10));
                frame.setlocal(7, frame.getlocal(4).__getitem__(s$44));
                if (((t$0$PyObject = frame.getlocal(3)._eq(s$15)).__nonzero__() ? t$0$PyObject : frame.getlocal(3)._eq(s$16)).__nonzero__()) {
                    frame.setlocal(5, frame.getglobal("None"));
                    if (frame.getlocal(3)._eq(s$15).__nonzero__()) {
                        frame.setlocal(5, frame.getlocal(0).__getattr__("sr_tree"));
                    }
                    else {
                        frame.setlocal(5, frame.getlocal(0).__getattr__("cr_tree"));
                    }
                    frame.setlocal(10, frame.getlocal(5).invoke("is_leaf", frame.getlocal(13)));
                    if (frame.getlocal(10)._eq(frame.getglobal("None")).__nonzero__()) {
                        return s$83;
                    }
                    else if (frame.getlocal(10)._eq(frame.getglobal("False")).__nonzero__()) {
                        return s$84;
                    }
                    frame.getlocal(5).invoke("tree_remove", frame.getlocal(13));
                    if (frame.getlocal(3)._eq(s$15).__nonzero__()) {
                        frame.getlocal(0).invoke("save_state", s$52);
                    }
                    else {
                        frame.getlocal(0).invoke("save_state", s$53);
                    }
                    if (frame.getglobal("site_to_auth").__call__(frame.getlocal(7)).__not__().__nonzero__()) {
                        try {
                            frame.getglobal("shell").invoke("DeleteSite", frame.getglobal("pl_auth"), frame.getlocal(7));
                        }
                        catch (Throwable x$0) {
                            t$0$PyException = Py.setException(x$0, frame);
                            i$9._eq(i$9);
                        }
                    }
                }
                else if (frame.getlocal(3)._eq(s$65).__nonzero__()) {
                    frame.getglobal("shell").invoke("DeletePerson", frame.getglobal("pl_auth"), frame.getlocal(7));
                }
                else if (frame.getlocal(3)._eq(s$37).__nonzero__()) {
                    frame.getglobal("shell").invoke("DeleteSlice", frame.getglobal("pl_auth"), frame.getlocal(7));
                }
                else if (frame.getlocal(3)._eq(s$69).__nonzero__()) {
                    frame.getglobal("shell").invoke("DeleteNode", frame.getglobal("pl_auth"), frame.getlocal(7));
                }
                frame.setlocal(8, frame.getglobal("generate_querystr").__call__(s$85, frame.getlocal(12), frame.getlocal(1).__getitem__(s$11)));
                frame.getlocal(6).invoke("query", frame.getlocal(8));
                return s$79._add(frame.getlocal(13))._add(s$86);
            }
            catch (Throwable x$1) {
                t$0$PyException = Py.setException(x$1, frame);
                if (Py.matchException(t$0$PyException, frame.getglobal("Exception"))) {
                    frame.setlocal(11, t$0$PyException.value);
                    Py.println(s$87._add(frame.getglobal("str").__call__(frame.getlocal(11))));
                    return s$88._add(frame.getglobal("str").__call__(frame.getlocal(11)));
                }
                else throw t$0$PyException;
            }
        }
        
        private static PyObject lookup$4(PyFrame frame) {
            // Temporary Variables
            PyException t$0$PyException;
            PyObject t$0$PyObject;
            
            // Code
            frame.setlocal(4, frame.getlocal(2).__getitem__(i$8));
            frame.setlocal(8, frame.getlocal(2).__getitem__(i$9));
            try {
                frame.setlocal(6, frame.getglobal("check_exists_geni").__call__(frame.getlocal(1), frame.getlocal(2)));
                if (frame.getlocal(6).__not__().__nonzero__()) {
                    throw Py.makeException(frame.getglobal("NonexistingRecord").__call__(s$12._add(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13))._add(s$73)));
                }
                frame.setlocal(5, frame.getlocal(6).__getitem__(s$10));
                frame.setlocal(3, frame.getlocal(6).__getitem__(s$44));
                frame.setlocal(7, frame.getglobal("None"));
                if (((t$0$PyObject = frame.getlocal(5)._eq(s$15)).__nonzero__() ? frame.getlocal(3)._ne(i$9.__neg__()) : t$0$PyObject).__nonzero__()) {
                    frame.setlocal(7, frame.getglobal("shell").invoke("GetSites", frame.getglobal("pl_auth"), new PyList(new PyObject[] {frame.getlocal(3)})));
                    if (frame.getlocal(7).__not__().__nonzero__()) {
                        frame.getlocal(0).invoke("remove", frame.getlocal(1), frame.getlocal(2));
                        throw Py.makeException(frame.getglobal("NonexistingRecord").__call__(s$12._add(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13))._add(s$73)));
                    }
                    frame.setlocal(7, frame.getlocal(7).__getitem__(i$8));
                }
                else if (((t$0$PyObject = frame.getlocal(5)._eq(s$16)).__nonzero__() ? frame.getlocal(3)._ne(i$9.__neg__()) : t$0$PyObject).__nonzero__()) {
                    frame.setlocal(7, frame.getglobal("shell").invoke("GetSites", frame.getglobal("pl_auth"), new PyList(new PyObject[] {frame.getlocal(3)})));
                    if (frame.getlocal(7).__not__().__nonzero__()) {
                        frame.getlocal(0).invoke("remove", frame.getlocal(1), frame.getlocal(2));
                        throw Py.makeException(frame.getglobal("NonexistingRecord").__call__(s$12._add(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13))._add(s$73)));
                    }
                    frame.setlocal(7, frame.getlocal(7).__getitem__(i$8));
                }
                else if (frame.getlocal(5)._eq(s$37).__nonzero__()) {
                    frame.setlocal(7, frame.getglobal("shell").invoke("GetSlices", frame.getglobal("pl_auth"), new PyList(new PyObject[] {frame.getlocal(3)})));
                    if (frame.getlocal(7).__not__().__nonzero__()) {
                        frame.getlocal(0).invoke("remove", frame.getlocal(1), frame.getlocal(2));
                        throw Py.makeException(frame.getglobal("NonexistingRecord").__call__(s$12._add(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13))._add(s$73)));
                    }
                    frame.setlocal(7, frame.getlocal(7).__getitem__(i$8));
                }
                else if (frame.getlocal(5)._eq(s$65).__nonzero__()) {
                    frame.setlocal(7, frame.getglobal("shell").invoke("GetPersons", frame.getglobal("pl_auth"), new PyList(new PyObject[] {frame.getlocal(3)})));
                    if (frame.getlocal(7).__not__().__nonzero__()) {
                        frame.getlocal(0).invoke("remove", frame.getlocal(1), frame.getlocal(2));
                        throw Py.makeException(frame.getglobal("NonexistingRecord").__call__(s$12._add(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13))._add(s$73)));
                    }
                    frame.setlocal(7, frame.getlocal(7).__getitem__(i$8));
                }
                else if (frame.getlocal(5)._eq(s$69).__nonzero__()) {
                    frame.setlocal(7, frame.getglobal("shell").invoke("GetNodes", frame.getglobal("pl_auth"), new PyList(new PyObject[] {frame.getlocal(3)})));
                    if (frame.getlocal(7).__not__().__nonzero__()) {
                        frame.getlocal(0).invoke("remove", frame.getlocal(1), frame.getlocal(2));
                        throw Py.makeException(frame.getglobal("NonexistingRecord").__call__(s$12._add(frame.getlocal(1).__getitem__(s$11).__getitem__(s$13))._add(s$73)));
                    }
                    frame.setlocal(7, frame.getlocal(7).__getitem__(i$8));
                }
                return frame.getglobal("str").__call__(new PyDictionary(new PyObject[] {s$89, frame.getlocal(7), s$74, frame.getlocal(6)}));
            }
            catch (Throwable x$0) {
                t$0$PyException = Py.setException(x$0, frame);
                return frame.getglobal("None");
            }
        }
        
        private static PyObject list$5(PyFrame frame) {
            frame.setlocal(3, i$9);
            return Py.None;
        }
        
        private static PyObject getCredential$6(PyFrame frame) {
            // Temporary Variables
            PyException t$0$PyException;
            PyObject t$0$PyObject;
            
            // Code
            frame.setlocal(14, frame.getlocal(2).__getitem__(i$8));
            frame.setlocal(16, frame.getlocal(2).__getitem__(i$9));
            try {
                frame.setlocal(19, frame.getglobal("None"));
                if (frame.getlocal(1).__getitem__(s$11).__getitem__(s$90).invoke("split", s$24).__getitem__(i$8)._eq(s$91).__nonzero__()) {
                    frame.setlocal(25, frame.getlocal(14).invoke("query", s$92._add(frame.getlocal(16))._add(s$93)._add(frame.getglobal("get_leaf").__call__(frame.getlocal(4).__getitem__(i$8)))._add(s$94)).invoke("dictresult"));
                    if (frame.getlocal(25).__nonzero__()) {
                        frame.setlocal(25, frame.getlocal(25).__getitem__(i$8));
                    }
                    else {
                        throw Py.makeException(frame.getglobal("NonexistingRecord").__call__(s$12._add(frame.getlocal(4).__getitem__(i$8))._add(s$73)));
                    }
                    frame.setlocal(26, frame.getlocal(25).__getitem__(s$10));
                    frame.setlocal(15, frame.getlocal(25).__getitem__(s$44));
                    frame.setlocal(12, frame.getlocal(25).__getitem__(s$26));
                    frame.setlocal(23, frame.getglobal("None"));
                    if (((t$0$PyObject = frame.getlocal(26)._eq(s$15)).__nonzero__() ? frame.getlocal(15)._ne(i$9.__neg__()) : t$0$PyObject).__nonzero__()) {
                        frame.setlocal(23, frame.getglobal("shell").invoke("GetSites", frame.getglobal("pl_auth"), new PyList(new PyObject[] {frame.getlocal(15)})));
                        if (frame.getlocal(23).__not__().__nonzero__()) {
                            frame.getlocal(0).invoke("remove", frame.getlocal(1), frame.getlocal(2));
                            throw Py.makeException(frame.getglobal("NonexistingRecord").__call__(s$12._add(frame.getlocal(4).__getitem__(i$8))._add(s$73)));
                        }
                    }
                    else if (((t$0$PyObject = frame.getlocal(26)._eq(s$16)).__nonzero__() ? frame.getlocal(15)._ne(i$9.__neg__()) : t$0$PyObject).__nonzero__()) {
                        frame.setlocal(23, frame.getglobal("shell").invoke("GetSites", frame.getglobal("pl_auth"), new PyList(new PyObject[] {frame.getlocal(15)})));
                        if (frame.getlocal(23).__not__().__nonzero__()) {
                            frame.getlocal(0).invoke("remove", frame.getlocal(1), frame.getlocal(2));
                            throw Py.makeException(frame.getglobal("NonexistingRecord").__call__(s$12._add(frame.getlocal(4).__getitem__(i$8))._add(s$73)));
                        }
                    }
                    else if (frame.getlocal(26)._eq(s$65).__nonzero__()) {
                        frame.setlocal(23, frame.getglobal("shell").invoke("GetPersons", frame.getglobal("pl_auth"), new PyList(new PyObject[] {frame.getlocal(15)})));
                        if (frame.getlocal(23).__not__().__nonzero__()) {
                            frame.getlocal(0).invoke("remove", frame.getlocal(1), frame.getlocal(2));
                            throw Py.makeException(frame.getglobal("NonexistingRecord").__call__(s$12._add(frame.getlocal(4).__getitem__(i$8))._add(s$73)));
                        }
                        frame.setlocal(23, frame.getglobal("shell").invoke("GetPersons", frame.getglobal("pl_auth"), new PyList(new PyObject[] {frame.getlocal(15)})).__getitem__(i$8));
                        if (((t$0$PyObject = frame.getlocal(12)._eq(s$19)).__nonzero__() ? t$0$PyObject : frame.getlocal(12)._eq(frame.getglobal("None"))).__nonzero__()) {
                            if (s$95._in(frame.getlocal(23).__getitem__(s$96)).__nonzero__()) {
                                frame.setlocal(12, s$97._add(s$98));
                                frame.setlocal(12, frame.getlocal(12)._add(s$67)._add(frame.getglobal("ROOT_AUTH"))._add(s$99)._add(frame.getglobal("ROOT_AUTH")));
                            }
                            else if (s$100._in(frame.getlocal(23).__getitem__(s$96)).__nonzero__()) {
                                frame.setlocal(12, s$97._add(s$98));
                                frame.setlocal(12, frame.getlocal(12)._add(s$67)._add(frame.getglobal("obtain_authority").__call__(frame.getlocal(4).__getitem__(i$8)))._add(s$99)._add(frame.getglobal("obtain_authority").__call__(frame.getlocal(4).__getitem__(i$8))));
                            }
                            else if (s$65._in(frame.getlocal(23).__getitem__(s$96)).__nonzero__()) {
                                frame.setlocal(12, s$66);
                                frame.setlocal(12, frame.getlocal(12)._add(s$67)._add(frame.getglobal("obtain_authority").__call__(frame.getlocal(4).__getitem__(i$8))));
                            }
                        }
                    }
                    else if (frame.getlocal(26)._eq(s$69).__nonzero__()) {
                        frame.setlocal(23, frame.getglobal("shell").invoke("GetNodes", frame.getglobal("pl_auth"), new PyList(new PyObject[] {frame.getlocal(15)})));
                        if (frame.getlocal(23).__not__().__nonzero__()) {
                            frame.getlocal(0).invoke("remove", frame.getlocal(1), frame.getlocal(2));
                            throw Py.makeException(frame.getglobal("NonexistingRecord").__call__(s$12._add(frame.getlocal(4).__getitem__(i$8))._add(s$73)));
                        }
                    }
                    frame.setlocal(7, s$101);
                    frame.setlocal(5, frame.getlocal(4).__getitem__(i$9));
                    frame.setlocal(19, frame.getglobal("create_cred").__call__(new PyObject[] {frame.getlocal(3).__getitem__(i$8), frame.getlocal(3).__getitem__(i$9), frame.getlocal(5).invoke("get_pubkey"), frame.getlocal(7), frame.getlocal(12)}));
                }
                else {
                    frame.setlocal(9, frame.getlocal(1).__getitem__(s$11).__getitem__(s$90).invoke("split", s$24));
                    if (frame.getlocal(9).__getitem__(i$8)._eq(s$37).__nonzero__()) {
                        frame.setlocal(20, new PyDictionary(new PyObject[] {s$11, new PyDictionary(new PyObject[] {s$13, frame.getlocal(9).__getitem__(i$9)}), s$27, new PyDictionary(new PyObject[] {})}));
                        frame.setlocal(10, frame.getlocal(0).invoke("lookup", frame.getlocal(20), frame.getlocal(2)));
                        frame.setlocal(8, frame.getglobal("False"));
                        frame.setlocal(22, frame.getlocal(10).__getitem__(s$27).__getitem__(s$102));
                        frame.setlocal(11, frame.getglobal("time").__getattr__("strptime").__call__(frame.getlocal(10).__getitem__(s$27).__getitem__(s$103), frame.getglobal("PL_DATETIME_FORMAT")));
                        frame.setlocal(11, frame.getglobal("datetime").__getattr__("timedelta").__call__(new PyObject[] {frame.getglobal("calendar").__getattr__("timegm").__call__(frame.getlocal(11))}, new String[] {"seconds"}));
                        if (((t$0$PyObject = frame.getlocal(10)).__nonzero__() ? frame.getlocal(22)._eq(s$104) : t$0$PyObject).__nonzero__()) {
                            frame.setlocal(6, frame.getglobal("determine_dbinfo").__call__(frame.getglobal("get_authority").__call__(frame.getlocal(4).__getitem__(i$8)), frame.getlocal(0).__getattr__("tree")));
                            if (frame.getlocal(6).__nonzero__()) {
                                frame.setlocal(21, new PyDictionary(new PyObject[] {s$11, new PyDictionary(new PyObject[] {s$13, frame.getlocal(4).__getitem__(i$8)}), s$27, new PyDictionary(new PyObject[] {})}));
                                frame.setlocal(18, frame.getlocal(0).invoke("lookup", frame.getlocal(21), frame.getlocal(6)).__getitem__(s$74).__getitem__(s$44));
                                frame.setlocal(13, s$105._add(frame.getlocal(18))._add(s$106)._add(frame.getlocal(10).__getitem__(s$74).__getitem__(s$44)));
                                frame.setlocal(17, frame.getlocal(14).invoke("query", frame.getlocal(13)).invoke("dictresult"));
                                if (frame.getlocal(17).__nonzero__()) {
                                    frame.setlocal(8, frame.getglobal("True"));
                                }
                            }
                            if (frame.getlocal(8).__nonzero__()) {
                                frame.setlocal(12, s$19);
                                if (((t$0$PyObject = frame.getlocal(10).__getitem__(s$74).__getitem__(s$26)._ne(s$19)).__nonzero__() ? t$0$PyObject : frame.getlocal(10).__getitem__(s$74).__getitem__(s$26)._ne(frame.getglobal("None"))).__nonzero__()) {
                                    frame.setlocal(12, frame.getlocal(10).__getitem__(s$74).__getitem__(s$26));
                                }
                                else {
                                    frame.setlocal(12, s$107);
                                    frame.setlocal(12, frame.getlocal(12)._add(s$108));
                                }
                                frame.setlocal(7, frame.getlocal(10).__getitem__(s$74).__getitem__(s$13));
                                frame.setlocal(24, frame.getglobal("datetime").__getattr__("timedelta").__call__(new PyObject[] {frame.getglobal("time").__getattr__("time").__call__()}, new String[] {"seconds"}));
                                if (frame.getlocal(11)._sub(frame.getlocal(24))._gt(frame.getglobal("CRED_GRANT_TIME")).__nonzero__()) {
                                    frame.setlocal(5, frame.getglobal("crypto").invoke("load_certificate", frame.getglobal("crypto").__getattr__("FILETYPE_PEM"), frame.getlocal(4).__getitem__(i$9)));
                                    frame.setlocal(19, frame.getglobal("create_cred").__call__(new PyObject[] {frame.getlocal(3).__getitem__(i$8), frame.getlocal(3).__getitem__(i$9), frame.getlocal(5).invoke("get_pubkey"), frame.getlocal(7), frame.getlocal(12)}));
                                }
                            }
                        }
                    }
                    else {
                        throw Py.makeException(frame.getglobal("NonexistingCredType").__call__(s$109._add(frame.getlocal(9).__getitem__(i$8))._add(s$73)));
                    }
                }
                if (frame.getlocal(19)._eq(frame.getglobal("None")).__nonzero__()) {
                    return frame.getlocal(19);
                }
                else {
                    return frame.getglobal("crypto").invoke("dump_certificate", frame.getglobal("crypto").__getattr__("FILETYPE_PEM"), frame.getlocal(19))._add(frame.getlocal(3).__getitem__(i$110));
                }
            }
            catch (Throwable x$0) {
                t$0$PyException = Py.setException(x$0, frame);
                return frame.getglobal("None");
            }
        }
        
        private static PyObject getAccounting$7(PyFrame frame) {
            // Temporary Variables
            PyException t$0$PyException;
            
            // Code
            frame.setlocal(6, frame.getlocal(2).__getitem__(i$8));
            frame.setlocal(11, frame.getlocal(2).__getitem__(i$9));
            try {
                frame.setlocal(9, frame.getglobal("None"));
                frame.setlocal(8, new PyDictionary(new PyObject[] {s$11, new PyDictionary(new PyObject[] {s$13, frame.getlocal(1).__getitem__(s$11).__getitem__(s$111)}), s$27, new PyDictionary(new PyObject[] {})}));
                frame.setlocal(10, frame.getglobal("eval").__call__(frame.getlocal(0).invoke("lookup", frame.getlocal(8), frame.getlocal(2))));
                if (frame.getlocal(10).__not__().__nonzero__()) {
                    throw Py.makeException(frame.getglobal("NonexistingRecord").__call__(s$12._add(frame.getlocal(1).__getitem__(s$11).__getitem__(s$111))._add(s$73)));
                }
                if (frame.getlocal(10).__getitem__(s$74).__getitem__(s$43)._eq(frame.getlocal(4).invoke("get_pubkey").__getattr__("as_pem").__call__(new PyObject[] {frame.getglobal("None")}, new String[] {"cipher"})).__nonzero__()) {
                    frame.setlocal(7, frame.getglobal("crypto").invoke("load_certificate", frame.getglobal("crypto").__getattr__("FILETYPE_PEM"), frame.getlocal(4).invoke("as_pem")));
                    frame.setlocal(5, i$8);
                    if (frame.getlocal(10).__getitem__(s$89).__not__().__nonzero__()) {
                        frame.setlocal(5, frame.getlocal(10).__getitem__(s$74).__getitem__(s$112));
                    }
                    else {
                        frame.setlocal(5, frame.getlocal(10).__getitem__(s$89).__getitem__(s$112));
                    }
                    frame.setlocal(9, frame.getglobal("create_acc").__call__(new PyObject[] {frame.getlocal(3).__getitem__(i$8), frame.getlocal(3).__getitem__(i$9), frame.getlocal(7).invoke("get_pubkey"), frame.getlocal(1).__getitem__(s$11).__getitem__(s$111), frame.getlocal(5)}));
                }
                if (frame.getlocal(9)._eq(frame.getglobal("None")).__nonzero__()) {
                    return frame.getlocal(9);
                }
                else {
                    return frame.getglobal("crypto").invoke("dump_certificate", frame.getglobal("crypto").__getattr__("FILETYPE_PEM"), frame.getlocal(9))._add(frame.getlocal(3).__getitem__(i$113));
                }
            }
            catch (Throwable x$0) {
                t$0$PyException = Py.setException(x$0, frame);
                return frame.getglobal("None");
            }
        }
        
        private static PyObject __init__$8(PyFrame frame) {
            frame.getlocal(0).__setattr__("sr_tree_file", frame.getglobal("SR_FILE"));
            frame.getlocal(0).__setattr__("cr_tree_file", frame.getglobal("CR_FILE"));
            frame.getlocal(0).__setattr__("sr_tree", frame.getglobal("None"));
            frame.getlocal(0).__setattr__("cr_tree", frame.getglobal("None"));
            frame.getlocal(0).invoke("construct_hierarchy");
            frame.getglobal("set_tree_globals").__call__(frame.getlocal(0).__getattr__("sr_tree"), frame.getlocal(0).__getattr__("cr_tree"));
            frame.getlocal(0).__setattr__("sec", frame.getglobal("None"));
            frame.getlocal(0).invoke("sec_init");
            frame.getlocal(0).__setattr__("functionList", new PyDictionary(new PyObject[] {s$114, frame.getlocal(0).__getattr__("register"), s$115, frame.getlocal(0).__getattr__("remove"), s$116, frame.getlocal(0).__getattr__("update"), s$117, frame.getlocal(0).__getattr__("lookup"), s$118, frame.getlocal(0).__getattr__("list"), s$119, frame.getlocal(0).__getattr__("getCredential"), s$120, frame.getlocal(0).__getattr__("getAccounting")}));
            frame.getglobal("SSL").__getattr__("SSLServer").__getattr__("__init__").__call__(new PyObject[] {frame.getlocal(0), frame.getlocal(1), frame.getlocal(2), frame.getlocal(0).__getattr__("sec").__getattr__("ctx")});
            return Py.None;
        }
        
        private static PyObject construct_hierarchy$9(PyFrame frame) {
            frame.getlocal(0).__setattr__("sr_tree", frame.getglobal("InterfaceTree").__call__(s$37, frame.getlocal(0).__getattr__("sr_tree_file"), new PyTuple(new PyObject[] {frame.getglobal("AUTH_HOST"), frame.getglobal("AUTH_PORT")})));
            frame.getlocal(0).__setattr__("cr_tree", frame.getglobal("InterfaceTree").__call__(s$38, frame.getlocal(0).__getattr__("cr_tree_file"), new PyTuple(new PyObject[] {frame.getglobal("AUTH_HOST"), frame.getglobal("AUTH_PORT")})));
            return Py.None;
        }
        
        private static PyObject sec_init$10(PyFrame frame) {
            frame.setlocal(4, frame.getlocal(0).__getattr__("sr_tree").__getattr__("my_tree").__getattr__("info").__getattr__("node_data").__getitem__(s$50));
            frame.setlocal(3, frame.getlocal(4).__getattr__("folder")._add(s$39)._add(frame.getlocal(4).__getattr__("id_file")));
            frame.setlocal(1, frame.getlocal(4).__getattr__("folder")._add(s$39)._add(frame.getlocal(4).__getattr__("id_key_file")));
            frame.setlocal(2, frame.getlocal(4).__getattr__("folder")._add(s$39)._add(frame.getlocal(4).__getattr__("acc_file")));
            frame.setlocal(5, frame.getlocal(4).__getattr__("folder")._add(s$39)._add(frame.getlocal(4).__getattr__("cred_file")));
            frame.getlocal(0).__setattr__("sec", frame.getglobal("Sec").__call__(new PyObject[] {s$121, frame.getlocal(3), frame.getlocal(1), frame.getlocal(2), frame.getlocal(5)}));
            frame.getglobal("renew_cert").__call__(new PyObject[] {s$122, frame.getlocal(4).__getattr__("folder"), s$37, frame.getlocal(0).__getattr__("sr_tree").__getattr__("my_tree").__getattr__("info").__getattr__("name"), frame.getglobal("None"), frame.getglobal("None"), new PyTuple(new PyObject[] {frame.getglobal("AUTH_HOST"), frame.getglobal("AUTH_PORT")}), frame.getlocal(0).__getattr__("sec")});
            frame.getglobal("renew_cert").__call__(new PyObject[] {s$123, frame.getlocal(4).__getattr__("folder"), s$37, frame.getlocal(0).__getattr__("sr_tree").__getattr__("my_tree").__getattr__("info").__getattr__("name"), frame.getglobal("None"), frame.getglobal("None"), new PyTuple(new PyObject[] {frame.getglobal("AUTH_HOST"), frame.getglobal("AUTH_PORT")}), frame.getlocal(0).__getattr__("sec")});
            return Py.None;
        }
        
        private static PyObject save_state$11(PyFrame frame) {
            // Temporary Variables
            PyObject t$0$PyObject;
            
            // Code
            if (((t$0$PyObject = frame.getlocal(1)._eq(s$52)).__nonzero__() ? t$0$PyObject : frame.getlocal(1)._eq(s$124)).__nonzero__()) {
                frame.getlocal(0).__getattr__("sr_tree").invoke("save_tree");
            }
            if (((t$0$PyObject = frame.getlocal(1)._eq(s$53)).__nonzero__() ? t$0$PyObject : frame.getlocal(1)._eq(s$124)).__nonzero__()) {
                frame.getlocal(0).__getattr__("cr_tree").invoke("save_tree");
            }
            return Py.None;
        }
        
        private static PyObject GENIServer$12(PyFrame frame) {
            frame.setlocal("register", new PyFunction(frame.f_globals, new PyObject[] {}, c$0_register));
            frame.setlocal("update", new PyFunction(frame.f_globals, new PyObject[] {}, c$1_update));
            frame.setlocal("remove", new PyFunction(frame.f_globals, new PyObject[] {}, c$2_remove));
            frame.setlocal("lookup", new PyFunction(frame.f_globals, new PyObject[] {}, c$3_lookup));
            frame.setlocal("list", new PyFunction(frame.f_globals, new PyObject[] {}, c$4_list));
            frame.setlocal("getCredential", new PyFunction(frame.f_globals, new PyObject[] {}, c$5_getCredential));
            frame.setlocal("getAccounting", new PyFunction(frame.f_globals, new PyObject[] {}, c$6_getAccounting));
            frame.setlocal("__init__", new PyFunction(frame.f_globals, new PyObject[] {}, c$7___init__));
            frame.setlocal("construct_hierarchy", new PyFunction(frame.f_globals, new PyObject[] {}, c$8_construct_hierarchy));
            frame.setlocal("sec_init", new PyFunction(frame.f_globals, new PyObject[] {}, c$9_sec_init));
            frame.setlocal("save_state", new PyFunction(frame.f_globals, new PyObject[] {s$124}, c$10_save_state));
            return frame.getf_locals();
        }
        
        private static PyObject handle$13(PyFrame frame) {
            // Temporary Variables
            PyException t$0$PyException;
            PyObject t$0$PyObject, t$1$PyObject, t$2$PyObject, t$3$PyObject;
            
            // Code
            try {
                frame.setlocal(6, frame.getglobal("server").__getattr__("sec").invoke("auth_protocol", frame.getlocal(0).__getattr__("request")));
                if (frame.getlocal(6).__not__().__nonzero__()) {
                    return Py.None;
                }
                frame.setlocal(9, frame.getglobal("msg_to_params").__call__(frame.getlocal(0).__getattr__("request").invoke("read")));
                frame.setlocal(11, frame.getlocal(9).__getitem__(s$11).__getitem__(s$13));
                frame.setlocal(10, frame.getlocal(9).__getitem__(s$125));
                frame.setlocal(4, s$19);
                if (((t$0$PyObject = ((t$1$PyObject = ((t$2$PyObject = frame.getlocal(10)._eq(s$114)).__nonzero__() ? t$2$PyObject : frame.getlocal(10)._eq(s$115))).__nonzero__() ? t$1$PyObject : frame.getlocal(10)._eq(s$116))).__nonzero__() ? t$0$PyObject : frame.getlocal(10)._eq(s$117)).__nonzero__()) {
                    frame.setlocal(4, frame.getglobal("obtain_authority").__call__(frame.getlocal(11)));
                }
                else if (((t$0$PyObject = ((t$1$PyObject = frame.getlocal(10)._eq(s$118)).__nonzero__() ? t$1$PyObject : frame.getlocal(10)._eq(s$119))).__nonzero__() ? t$0$PyObject : frame.getlocal(10)._eq(s$120)).__nonzero__()) {
                    frame.setlocal(4, frame.getlocal(11));
                }
                frame.setlocal(12, s$19);
                if (((t$0$PyObject = ((t$1$PyObject = ((t$2$PyObject = ((t$3$PyObject = frame.getlocal(10)._eq(s$114)).__nonzero__() ? t$3$PyObject : frame.getlocal(10)._eq(s$115))).__nonzero__() ? t$2$PyObject : frame.getlocal(10)._eq(s$116))).__nonzero__() ? t$1$PyObject : frame.getlocal(10)._eq(s$117))).__nonzero__() ? t$0$PyObject : frame.getlocal(10)._eq(s$118)).__nonzero__()) {
                    frame.setlocal(1, frame.getlocal(9).__getitem__(s$11).__getitem__(s$10));
                    if (((t$0$PyObject = ((t$1$PyObject = frame.getlocal(1)._eq(s$37)).__nonzero__() ? t$1$PyObject : frame.getlocal(1)._eq(s$65))).__nonzero__() ? t$0$PyObject : frame.getlocal(1)._eq(s$15)).__nonzero__()) {
                        frame.setlocal(12, s$37);
                    }
                    else {
                        frame.setlocal(12, s$38);
                    }
                }
                else if (frame.getlocal(10)._eq(s$119).__nonzero__()) {
                    if (frame.getlocal(9).__getitem__(s$11).__getitem__(s$90).invoke("split", s$24).__getitem__(i$9)._eq(s$20).__nonzero__()) {
                        frame.setlocal(12, s$37);
                    }
                    else {
                        frame.setlocal(12, s$38);
                    }
                }
                else if (frame.getlocal(10)._eq(s$120).__nonzero__()) {
                    frame.setlocal(12, frame.getlocal(9).__getitem__(s$11).__getitem__(s$91));
                }
                frame.setlocal(8, frame.getglobal("None"));
                if (frame.getlocal(12)._eq(s$37).__nonzero__()) {
                    frame.setlocal(8, frame.getglobal("server").__getattr__("sr_tree"));
                }
                else {
                    frame.setlocal(8, frame.getglobal("server").__getattr__("cr_tree"));
                }
                frame.setlocal(7, frame.getglobal("determine_dbinfo").__call__(frame.getlocal(4), frame.getlocal(8)));
                frame.setlocal(15, frame.getglobal("None"));
                if (frame.getlocal(10)._eq(s$120).__nonzero__()) {
                    frame.setlocal(15, frame.getlocal(8).invoke("determine_keyinfo", new PyObject[] {frame.getlocal(4), frame.getglobal("server"), s$122}));
                }
                else if (frame.getlocal(10)._eq(s$119).__nonzero__()) {
                    frame.setlocal(15, frame.getlocal(8).invoke("determine_keyinfo", new PyObject[] {frame.getlocal(4), frame.getglobal("server"), s$123}));
                }
                if (frame.getlocal(7)._eq(frame.getglobal("None")).__nonzero__()) {
                    frame.getlocal(0).__getattr__("request").invoke("write", s$126);
                    return Py.None;
                }
                if (frame.getglobal("server").__getattr__("functionList").invoke("has_key", frame.getlocal(9).__getitem__(s$125)).__not__().__nonzero__()) {
                    frame.getlocal(0).__getattr__("request").invoke("write", s$127);
                    return Py.None;
                }
                if (frame.getglobal("server").__getattr__("sec").invoke("check_authorization", new PyObject[] {frame.getlocal(6).__getattr__("acc"), frame.getlocal(6).__getattr__("cred"), frame.getlocal(9)}).__not__().__nonzero__()) {
                    frame.getlocal(0).__getattr__("request").invoke("write", s$128);
                    return Py.None;
                }
                frame.setlocal(2, frame.getglobal("server").__getattr__("functionList").__getitem__(frame.getlocal(9).__getitem__(s$125)));
                frame.setlocal(14, new PyDictionary(new PyObject[] {s$11, frame.getlocal(9).__getitem__(s$11), s$27, frame.getlocal(9).__getitem__(s$27)}));
                frame.setlocal(5, frame.getglobal("None"));
                if (frame.getlocal(2)._eq(frame.getglobal("server").__getattr__("getAccounting")).__nonzero__()) {
                    frame.setlocal(5, frame.getlocal(2).__call__(new PyObject[] {frame.getlocal(14), frame.getlocal(7), frame.getlocal(15), frame.getlocal(6).__getattr__("cert")}));
                }
                else if (frame.getlocal(2)._eq(frame.getglobal("server").__getattr__("getCredential")).__nonzero__()) {
                    frame.setlocal(3, new PyList(new PyObject[] {frame.getlocal(6).__getattr__("acc").invoke("get_hrn"), frame.getglobal("crypto").invoke("load_certificate", frame.getglobal("crypto").__getattr__("FILETYPE_PEM"), frame.getlocal(6).__getattr__("cert").invoke("as_pem"))}));
                    frame.setlocal(5, frame.getlocal(2).__call__(new PyObject[] {frame.getlocal(14), frame.getlocal(7), frame.getlocal(15), frame.getlocal(3)}));
                }
                else if (((t$0$PyObject = ((t$1$PyObject = frame.getlocal(2)._eq(frame.getglobal("server").__getattr__("register"))).__nonzero__() ? t$1$PyObject : frame.getlocal(2)._eq(frame.getglobal("server").__getattr__("update")))).__nonzero__() ? t$0$PyObject : frame.getlocal(2)._eq(frame.getglobal("server").__getattr__("remove"))).__nonzero__()) {
                    frame.setlocal(5, frame.getglobal("str").__call__(new PyDictionary(new PyObject[] {s$129, frame.getlocal(2).__call__(frame.getlocal(14), frame.getlocal(7))})));
                }
                else {
                    frame.setlocal(5, frame.getlocal(2).__call__(frame.getlocal(14), frame.getlocal(7)));
                    if (frame.getlocal(5).__not__().__nonzero__()) {
                        frame.getlocal(0).__getattr__("request").invoke("write", frame.getglobal("str").__call__(new PyDictionary(new PyObject[] {s$129, s$130})));
                    }
                }
                frame.getlocal(0).__getattr__("request").invoke("write", frame.getlocal(5));
                return Py.None;
            }
            catch (Throwable x$0) {
                t$0$PyException = Py.setException(x$0, frame);
                if (Py.matchException(t$0$PyException, frame.getglobal("Exception"))) {
                    frame.setlocal(13, t$0$PyException.value);
                    Py.println(s$131._add(frame.getglobal("str").__call__(frame.getlocal(13))));
                    return Py.None;
                }
                else throw t$0$PyException;
            }
        }
        
        private static PyObject handle_connection$14(PyFrame frame) {
            frame.setlocal("handle", new PyFunction(frame.f_globals, new PyObject[] {}, c$12_handle));
            return frame.getf_locals();
        }
        
        private static PyObject main$15(PyFrame frame) {
            frame.getglobal("server").invoke("save_state");
            frame.getglobal("server").invoke("serve_forever");
            return Py.None;
        }
        
        private static PyObject main$16(PyFrame frame) {
            frame.setglobal("__file__", s$133);
            
            PyObject[] imp_accu;
            // Code
            frame.setlocal("LISTEN_HOST", s$0);
            frame.setlocal("LISTEN_PORT", i$1);
            frame.setlocal("SR_FILE", s$2);
            frame.setlocal("CR_FILE", s$3);
            frame.setlocal("AUTH_HOST", s$0);
            frame.setlocal("AUTH_PORT", i$1);
            frame.setlocal("SocketServer", org.python.core.imp.importOne("SocketServer", frame));
            frame.setlocal("socket", org.python.core.imp.importOne("socket", frame));
            frame.setlocal("os", org.python.core.imp.importOne("os", frame));
            frame.setlocal("sys", org.python.core.imp.importOne("sys", frame));
            imp_accu = org.python.core.imp.importFrom("M2Crypto", new String[] {"SSL"}, frame);
            frame.setlocal("SSL", imp_accu[0]);
            imp_accu = null;
            imp_accu = org.python.core.imp.importFrom("M2Crypto.SSL", new String[] {"SSLError"}, frame);
            frame.setlocal("SSLError", imp_accu[0]);
            imp_accu = null;
            imp_accu = org.python.core.imp.importFrom("M2Crypto", new String[] {"X509"}, frame);
            frame.setlocal("X509", imp_accu[0]);
            imp_accu = null;
            imp_accu = org.python.core.imp.importFrom("pg", new String[] {"DB"}, frame);
            frame.setlocal("DB", imp_accu[0]);
            imp_accu = null;
            frame.getname("sys").__getattr__("path").__getattr__("append").__call__(s$4);
            frame.getname("sys").__getattr__("path").__getattr__("append").__call__(s$5);
            frame.getname("sys").__getattr__("path").__getattr__("append").__call__(s$6);
            frame.getname("sys").__getattr__("path").__getattr__("append").__call__(s$7);
            org.python.core.imp.importAll("util", frame);
            org.python.core.imp.importAll("tree", frame);
            org.python.core.imp.importAll("excep", frame);
            org.python.core.imp.importAll("sec", frame);
            org.python.core.imp.importAll("db", frame);
            org.python.core.imp.importAll("pl_to_geni", frame);
            frame.setlocal("time", org.python.core.imp.importOne("time", frame));
            frame.setlocal("datetime", org.python.core.imp.importOne("datetime", frame));
            frame.setlocal("calendar", org.python.core.imp.importOne("calendar", frame));
            imp_accu = org.python.core.imp.importFrom("PLC.Shell", new String[] {"Shell"}, frame);
            frame.setlocal("Shell", imp_accu[0]);
            imp_accu = null;
            frame.setlocal("shell", frame.getname("Shell").__call__(new PyObject[] {frame.getname("globals").__call__()}, new String[] {"globals"}));
            frame.setlocal("GENIServer", Py.makeClass("GENIServer", new PyObject[] {frame.getname("SSL").__getattr__("SSLServer")}, c$11_GENIServer, null));
            frame.setlocal("handle_connection", Py.makeClass("handle_connection", new PyObject[] {frame.getname("SocketServer").__getattr__("BaseRequestHandler")}, c$13_handle_connection, null));
            frame.setlocal("server", frame.getname("GENIServer").__call__(new PyTuple(new PyObject[] {frame.getname("LISTEN_HOST"), frame.getname("LISTEN_PORT")}), frame.getname("handle_connection")));
            frame.setlocal("main", new PyFunction(frame.f_globals, new PyObject[] {}, c$14_main));
            if (frame.getname("__name__")._eq(s$132).__nonzero__()) {
                frame.getname("main").__call__();
            }
            return Py.None;
        }
        
    }
    public static void moduleDictInit(PyObject dict) {
        dict.__setitem__("__name__", new PyString("server"));
        Py.runCode(new _PyInner().getMain(), dict, dict);
    }
    
    public static void main(String[] args) throws java.lang.Exception {
        String[] newargs = new String[args.length+1];
        newargs[0] = "server";
        System.arraycopy(args, 0, newargs, 1, args.length);
        Py.runMain(server._PyInner.class, newargs, server.jpy$packages, server.jpy$mainProperties, "", new String[] {"string", "random", "util", "traceback", "sre_compile", "atexit", "sre", "sre_constants", "StringIO", "javaos", "socket", "yapm", "calendar", "repr", "copy_reg", "SocketServer", "server", "re", "linecache", "javapath", "UserDict", "copy", "threading", "stat", "PathVFS", "sre_parse"});
    }
    
}
