/*
 * DisplayHandle.java
 *
 * Created on March 29, 2008, 2:42 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package javaapplication1;

import java.io.*;
import javax.swing.JPanel;
import java.awt.*;
import javax.swing.*;

/**
 *
 * @author soners
 */
public class DisplayHandle {
    
    /** Creates a new instance of DisplayHandle */
    public DisplayHandle(BufferedWriter outCommand) {
        this.outCommand = outCommand;
        createCompListUser();
        createCompListSlice();
        createCompListNode();
        createCompListSite();
    }
    
    private void createCompListNode(){
        compList_node = new GuiComponent[33];
        GuiComponent[] compList = compList_node;
        String[] tmplist1 = {"readable","pl"};
        String[] tmplist2 = {"writable","pl"};
        String[] tmplist3 = {"readable","geni"};
        String[] tmplist4 = {"writable","geni"};
        compList[0] = new GuiComponent("node_id", tmplist1, "text", "Node Id", "");
        compList[1] = new GuiComponent("last_updated", tmplist1, "text", "Last Updated", "");
        compList[2] = new GuiComponent("boot_state", tmplist2, "combo", "Boot state", "boot, dbg, inst, new, rcnf, rins");
        compList[3] = new GuiComponent("site_id", tmplist1, "num", "Site Id", "");
        compList[4] = new GuiComponent("pcu_ids", tmplist2, "num", "PCU Ids", "");
        compList[5] = new GuiComponent("session", tmplist1, "text", "Session", "");
        compList[6] = new GuiComponent("key", tmplist2, "key", "Key", "");
        compList[7] = new GuiComponent("conf_file_ids", tmplist2, "text", "Conf file Ids", "");
        compList[8] = new GuiComponent("ssh_rsa_key", tmplist1, "text", "SSH RSA Key", "");
        compList[9] = new GuiComponent("ssh_rsa_key_write", tmplist2, "key", "SSH RSA Key", "");
        compList[10] = new GuiComponent("uuid", tmplist1, "text", "UUID", "");
        compList[11] = new GuiComponent("nodegroup_ids", tmplist2, "num", "Node Group Ids", "");
        compList[12] = new GuiComponent("slice_ids_whitelist", tmplist2, "text", "Slice Ids Whitelist", "");
        compList[13] = new GuiComponent("last_contact", tmplist2, "text", "Last Contact", "");
        compList[14] = new GuiComponent("nodenetwork_ids", tmplist2, "text", "Node Network Ids", "");
        compList[15] = new GuiComponent("peer_node_id", tmplist2, "num", "Peer Node Id", "");
        compList[16] = new GuiComponent("hostname", tmplist2, "text", "Hostname", "randomsite.edu");
        compList[17] = new GuiComponent("slice_ids", tmplist1, "num", "Slice Ids", "");
        compList[18] = new GuiComponent("boot_nonce", tmplist2, "text", "Boot Nonce", "");
        compList[19] = new GuiComponent("version", tmplist2, "text", "Version", "PlanetLab BootCD 3.1");
        compList[20] = new GuiComponent("date_created", tmplist1, "text", "Date Created", "");
        compList[21] = new GuiComponent("model", tmplist2, "text", "Model", "Dell OptiPlex GX280");
        compList[22] = new GuiComponent("peer_id", tmplist1, "num", "Peer Id", "");
        compList[23] = new GuiComponent("ports", tmplist2, "text", "Ports", "");
        compList[24] = new GuiComponent("description", tmplist4, "text", "Description", "New node for testing purposes");
        compList[25] = new GuiComponent("rights", tmplist4, "text", "Rights", "");
        compList[26] = new GuiComponent("pubkey", tmplist3, "text", "GENI Public key", "");
        compList[27] = new GuiComponent("pubkey_write", tmplist4, "key", "GENI Public key", "");
        compList[28] = new GuiComponent("wrapperurl", tmplist4, "text", "Wrapper URL", "local");
        compList[29] = new GuiComponent("disabled", tmplist3, "bool", "Disabled", "Yes, No");
        compList[30] = new GuiComponent("userlist", tmplist4, "text", "User List", "");            
        compList[31] = new GuiComponent("pointer", tmplist3, "num", "PL Pointer", "");
        compList[32] = new GuiComponent("g_uuid", tmplist3, "text", "GENI UUID", "");
    
    }
    
    private void createCompListUser(){        
        compList_user = new GuiComponent[28];
        GuiComponent[] compList = compList_user;
        String[] tmplist1 = {"readable","pl"};
        String[] tmplist2 = {"writable","pl"};
        String[] tmplist3 = {"readable","geni"};
        String[] tmplist4 = {"writable","geni"};
        compList[0] = new GuiComponent("person_id", tmplist1, "num", "Person Id", "");        
        compList[1] = new GuiComponent("bio", tmplist2, "text", "Bio", "");
        compList[2] = new GuiComponent("first_name", tmplist2, "text", "First Name", "");
        compList[3] = new GuiComponent("last_name", tmplist2, "text", "Last Name", "");
        compList[4] = new GuiComponent("last_updated", tmplist1, "text", "Last Updated", "");
        compList[5] = new GuiComponent("key_ids", tmplist2, "num", "Key Ids", "");
        compList[6] = new GuiComponent("phone", tmplist2, "text", "Phone", "");
        compList[7] = new GuiComponent("peer_person_id", tmplist2, "num", "Peer Person Id", "");
        compList[8] = new GuiComponent("role_ids", tmplist2, "num", "Role Ids", "");
        compList[9] = new GuiComponent("site_ids", tmplist1, "num", "Site Ids", "");        
        compList[10] = new GuiComponent("uuid", tmplist1, "text", "UUID", "");
        compList[11] = new GuiComponent("roles", tmplist2, "num", "Roles", "");
        compList[12] = new GuiComponent("title", tmplist2, "text", "Title", "");
        compList[13] = new GuiComponent("url", tmplist2, "text", "Url", "someuser.dom.edu");
        compList[14] = new GuiComponent("enabled", tmplist2, "bool", "Enabled", "Yes, No");
        compList[15] = new GuiComponent("slice_ids", tmplist2, "num", "Slice Ids", "");
        compList[16] = new GuiComponent("date_created", tmplist1, "text", "Date Created", "");
        compList[17] = new GuiComponent("peer_id", tmplist2, "num", "Peer Id", "");
        compList[18] = new GuiComponent("email", tmplist2, "text", "Email", "someuser@domain.edu");
        compList[19] = new GuiComponent("description", tmplist4, "text", "Description", "test user");
        compList[20] = new GuiComponent("rights", tmplist2, "text", "Rights", "");
        compList[21] = new GuiComponent("pubkey", tmplist3, "text", "GENI Public key", "");
        compList[22] = new GuiComponent("pubkey_write", tmplist4, "key", "GENI Public key", "");
        compList[23] = new GuiComponent("wrapperurl", tmplist4, "text", "Wrapper URL", "local");
        compList[24] = new GuiComponent("disabled", tmplist3, "bool", "Disabled", "Yes, No");
        compList[25] = new GuiComponent("userlist", tmplist4, "text", "User List", "");            
        compList[26] = new GuiComponent("pointer", tmplist3, "text", "PL Pointer", "");
        compList[27] = new GuiComponent("g_uuid", tmplist3, "text", "GENI UUID", "");
        
    }
    
    private void createCompListSlice(){
        compList_slice = new GuiComponent[24];
        GuiComponent[] compList = compList_slice;
        String[] tmplist1 = {"readable","pl"};
        String[] tmplist2 = {"writable","pl"};
        String[] tmplist3 = {"readable","geni"};
        String[] tmplist4 = {"writable","geni"};
        compList[0] = new GuiComponent("slice_id", tmplist1, "num", "Slice Id", "");        
        compList[1] = new GuiComponent("description", tmplist2, "text", "Description", ""); 
        compList[2] = new GuiComponent("node_ids", tmplist1, "num", "Node Ids", "");
        compList[3] = new GuiComponent("expires", tmplist2, "text", "Expires", "");
        compList[4] = new GuiComponent("site_id", tmplist1, "num", "Site Id", "");
        compList[5] = new GuiComponent("uuid", tmplist1, "text", "UUID", "");
        compList[6] = new GuiComponent("creator_person_id", tmplist2, "text", "Creator Person Id", "");
        compList[7] = new GuiComponent("instantiation", tmplist2, "combo", "Instantiation", "delegated, not-instantiated, plc-instantiated");
        compList[8] = new GuiComponent("name", tmplist2, "text", "Name", "");
        compList[9] = new GuiComponent("created", tmplist1, "text", "Created", "");
        compList[10] = new GuiComponent("url", tmplist2, "text", "Url", "");
        compList[11] = new GuiComponent("max_nodes", tmplist2, "num", "Max Nodes", "10");
        compList[12] = new GuiComponent("person_ids", tmplist2, "num", "Person Ids", "");
        compList[13] = new GuiComponent("slice_attribute_ids", tmplist2, "text", "Slice Attribute Ids", "");
        compList[14] = new GuiComponent("peer_id", tmplist1, "num", "Peer Id", "");
        compList[15] = new GuiComponent("description", tmplist4, "text", "Description", "test slice");
        compList[16] = new GuiComponent("rights", tmplist2, "text", "Rights", "");
        compList[17] = new GuiComponent("pubkey", tmplist3, "text", "GENI Public key", "");
        compList[18] = new GuiComponent("pubkey_write", tmplist4, "key", "GENI Public key", "");
        compList[19] = new GuiComponent("wrapperurl", tmplist4, "text", "Wrapper URL", "local");
        compList[20] = new GuiComponent("disabled", tmplist3, "bool", "Disabled", "Yes, No");
        compList[21] = new GuiComponent("userlist", tmplist4, "text", "User List", "");            
        compList[22] = new GuiComponent("pointer", tmplist3, "num", "PL Pointer", "");
        compList[23] = new GuiComponent("g_uuid", tmplist3, "text", "GENI UUID", "");               
        
    }
    
    private void createCompListSite(){
        compList_site = new GuiComponent[31];
        GuiComponent[] compList = compList_site;
        String[] tmplist1 = {"readable","pl"};
        String[] tmplist2 = {"writable","pl"};
        String[] tmplist3 = {"readable","geni"};
        String[] tmplist4 = {"writable","geni"};
        
        compList[0] = new GuiComponent("last_updated", tmplist1, "text", "Last Updated", "");
        compList[1] = new GuiComponent("node_ids", tmplist2, "num", "Node Ids", "");
        compList[2] = new GuiComponent("site_id", tmplist1, "num", "Site Id", "");
        compList[3] = new GuiComponent("pcu_ids", tmplist2, "num", "PCU Ids", "");
        compList[4] = new GuiComponent("max_slices", tmplist2, "num", "Max Slices", "");
        compList[5] = new GuiComponent("ext_consortium_id", tmplist2, "text", "Ext Consortium Id", "");
        compList[6] = new GuiComponent("max_slivers", tmplist2, "num", "Max Slivers", "5");
        compList[7] = new GuiComponent("is_public", tmplist2, "bool", "Public", "Yes, No");
        compList[8] = new GuiComponent("peer_site_id", tmplist1, "num", "Peer Site Id", "");
        compList[9] = new GuiComponent("abbreviated_name", tmplist2, "text", "Abbreviated Name", "");
        compList[10] = new GuiComponent("name", tmplist2, "text", "Name", "");
        compList[11] = new GuiComponent("address_ids", tmplist2, "num", "Address Ids", "");
        compList[12] = new GuiComponent("uuid", tmplist1, "text", "UUID", "");
        compList[13] = new GuiComponent("url", tmplist2, "text", "Url", "");
        compList[14] = new GuiComponent("person_ids", tmplist2, "num", "Person Ids", "");
        compList[15] = new GuiComponent("enabled", tmplist2, "bool", "Enabled", "Yes, No");
        compList[16] = new GuiComponent("longitude", tmplist2, "num", "Longitude", "34.3");
        compList[17] = new GuiComponent("latitude", tmplist2, "num", "Latitude", "45.4");
        compList[18] = new GuiComponent("slice_ids", tmplist2, "num", "Slice Ids", "");
        compList[19] = new GuiComponent("login_base", tmplist2, "text", "Login Base", "");
        compList[20] = new GuiComponent("date_created", tmplist1, "text", "Date Created", "");
        compList[21] = new GuiComponent("peer_id", tmplist1, "num", "Peer Id", "");
        compList[22] = new GuiComponent("description", tmplist4, "text", "Description", "test slice");
        compList[23] = new GuiComponent("rights", tmplist2, "text", "Rights", "");
        compList[24] = new GuiComponent("pubkey", tmplist3, "text", "GENI Public key", "");
        compList[25] = new GuiComponent("pubkey_write", tmplist4, "key", "GENI Public key", "");
        compList[26] = new GuiComponent("wrapperurl", tmplist4, "text", "Wrapper URL", "local");
        compList[27] = new GuiComponent("disabled", tmplist3, "bool", "Disabled", "Yes, No");
        compList[28] = new GuiComponent("userlist", tmplist4, "text", "User List", "");            
        compList[29] = new GuiComponent("pointer", tmplist3, "num", "PL Pointer", "");
        compList[30] = new GuiComponent("g_uuid", tmplist3, "text", "GENI UUID", "");                     
    }
    
    //input is in format: {"'field1_name':value1", "'field2_name':value2", ...}
    public void FillComponentList(String recordType, String[] dict){
        GuiComponent[] complist = null;
        if (recordType.equals("user")){
            complist = compList_user;
        }
        else if (recordType.equals("slice")){
            complist = compList_slice;
        }
        else if (recordType.equals("node")){
            complist = compList_node;
        }
        else if (recordType.equals("SA/MA")){
            complist = compList_site;
        }
        
        for (int i=0; i<dict.length; i++){
            String[] line = dict[i].split("':");
            String comp_name = line[0].split("'")[1];
            String comp_value = "";
            if (line.length > 1)
                comp_value = line[1];
            if (comp_value.equals("None"))
                    comp_value = "";
            int j;
            for(j = 0; j<complist.length; j++){
                if (complist[j].getName().equals(comp_name)){
                    break;
                }
            }
            if (j == complist.length)
                continue;
            else{
                String type = complist[j].getType();
                if (type.equals("text") || type.equals("num"))
                    complist[j].setValue(comp_value);
                else if (type.equals("bool"))
                    if (comp_value.equals("True"))
                        complist[j].setValue("Yes, No");
                    else
                        complist[j].setValue("No, Yes");
                else if (type.equals("combo")){
                    String[] curVal = complist[j].getValue().split(", ");
                    String nextVal = comp_value;
                    for(int k=0; k<curVal.length; k++)
                        if (curVal[k] != comp_value)
                            nextVal += (", "+curVal[k]);
                    complist[j].setValue(nextVal);
                }
                else if (type.equals("key")){
                    complist[j].setValue(comp_value);                
                }
            }
        }    
    }
    
    private void keyChooserActionPerformed(JTextField t, java.awt.event.ActionEvent evt) {                                              
// TODO add your handling code here:
        
        javax.swing.JFileChooser fc =  (javax.swing.JFileChooser)evt.getSource();
        java.io.File f = fc.getSelectedFile();
        
        if(keySelectFrame!=null)
                keySelectFrame.dispose();
        
        if (f != null){
            String fname = f.getAbsolutePath();            

            try{
                //extract the pubkey from the specified file into temp file
                outCommand.write("./certutil.py "+fname+" > tmp_key_file.txt\n");            
                outCommand.flush();

                //get key from temp file 
                String result = "";
                File file = new File("tmp_key_file.txt");
                int i = 0;
                while(!file.exists() && i<5){
                    i++;
                    try {
                        Thread.currentThread().sleep(200);
                    } catch (InterruptedException ex) {
                        ex.printStackTrace();
                    }
                }
                try {
                    Thread.currentThread().sleep(100);
                } catch (InterruptedException ex) {
                    ex.printStackTrace();
                }        
                if (file.exists()){                
                    BufferedReader in = new BufferedReader(new FileReader("tmp_key_file.txt")); 
                    String tmp = in.readLine();
                    while(tmp!=null && tmp.length() > 0){
                        result += tmp+"\n";
                        tmp = in.readLine();
                    }                
                    in.close();

                    outCommand.write("rm tmp_key_file.txt\n");            
                    outCommand.flush();                               
                }
                //write the result in the textfield
                t.setText(result);
              }catch (Exception ex) {
                        ex.printStackTrace();
                } 
        }
            
    }        
    
    public void displayComponentList(String recordType, JPanel panel1, JPanel panel2){
        
        GuiComponent[] complist = null;
        if (recordType.equals("user")){
            complist = compList_user;
        }
        else if (recordType.equals("slice")){
            complist = compList_slice;
        }
        else if (recordType.equals("node")){
            complist = compList_node;
        }
        else if (recordType.equals("SA/MA")){
            complist = compList_site;
        }        
            
        panel1.removeAll();
        panel1.setLayout(new SpringLayout());      

        int count1 = 0;
        for (int i=0;i<complist.length;i++){
            if (complist[i].getProperty()[0].equals("readable") && complist[i].getProperty()[1].equals("geni")){
                String type = complist[i].getType();
                if (type.equals("text") || type.equals("num")){
                    JLabel l = new JLabel(complist[i].getLabel(), JLabel.TRAILING);
                    l.setName(complist[i].getName());
                    panel1.add(l);
                    JTextField t = new JTextField();
                    t.setText(complist[i].getValue());
                    t.setEditable(false);
                    l.setLabelFor(t);
                    panel1.add(t);
                    count1++;
                }
            }
        }
        int count2 = 0;
        for (int i=0;i<complist.length;i++){
            if (complist[i].getProperty()[0].equals("readable") && complist[i].getProperty()[1].equals("pl")){
                String type = complist[i].getType();
                if (type.equals("text") || type.equals("num")){
                    JLabel l = new JLabel(complist[i].getLabel(), JLabel.TRAILING);
                    l.setName(complist[i].getName());
                    panel1.add(l);
                    JTextField t = new JTextField();
                    t.setText(complist[i].getValue());
                    t.setEditable(false);
                    l.setLabelFor(t);
                    panel1.add(t);
                    count2++;
                }
            }
        }
        int parts = 2*(count1+count2);
        while(parts != (parts/6)*6){
            JLabel l = new JLabel("", JLabel.TRAILING);
            panel1.add(l);
            parts++;
        }
         //Lay out the panel.
        SpringUtilities.makeCompactGrid(panel1,
                                        parts/6, 6, //rows, cols
                                        6, 6,        //initX, initY
                                        6, 6);       //xPad, yPad
        panel1.revalidate();
        panel1.repaint();

    
        //fill the second(writable) panel
        panel2.removeAll();
        panel2.setLayout(new SpringLayout());      

        count1 = 0;
        for (int i=0;i<complist.length;i++){
            if (complist[i].getProperty()[0].equals("writable") && complist[i].getProperty()[1].equals("geni")){
                JLabel l = new JLabel(complist[i].getLabel(), JLabel.TRAILING);
                final String name = complist[i].getName();
                l.setName(name);
                panel2.add(l);
                String type = complist[i].getType();
                if (type.equals("text") || type.equals("num")){                    
                    JTextField t = new JTextField();
                    t.setText(complist[i].getValue());                   
                    l.setLabelFor(t);
                    panel2.add(t);
                    count1++;
                }
                else if (type.equals("combo") || type.equals("bool")){
                    JComboBox cb = new JComboBox(complist[i].getValue().split(", "));
                    l.setLabelFor(cb);
                    panel2.add(cb);
                    count1++;
                }
                else if (type.equals("key")){ 
                    final JTextField t = new JTextField();
                    t.setText(complist[i].getValue());    
                    t.setEditable(false);
                    l.setLabelFor(t);
                    panel2.add(t);                    
                    
                    t.addMouseListener(new java.awt.event.MouseAdapter() {
                        public void mousePressed(java.awt.event.MouseEvent evt) {
                            //Create and set up the window.
                            if(keySelectFrame!=null)
                                  keySelectFrame.dispose();
                            keySelectFrame = new JFrame("Key Select");
                            keySelectFrame.setSize(600,400);
                            keySelectFrame.setLocation(200,100);

                            //Set up the content pane.
                            Container contentPane = keySelectFrame.getContentPane();
                            SpringLayout layout = new SpringLayout();
                            contentPane.setLayout(layout);        

                            JFileChooser fc = new JFileChooser();
                            fc.addActionListener(new java.awt.event.ActionListener() {
                                public void actionPerformed(java.awt.event.ActionEvent evt) {
                                    keyChooserActionPerformed(t, evt);
                                }
                            });

                            contentPane.add(fc);

                            //Display the window.
                            keySelectFrame.pack();
                            keySelectFrame.setVisible(true); 
                        }
                    });
                    count1++;
                } 
            }
        }
        count2 = 0;
        for (int i=0;i<complist.length;i++){
            if (complist[i].getProperty()[0].equals("writable") && complist[i].getProperty()[1].equals("pl")){
                JLabel l = new JLabel(complist[i].getLabel(), JLabel.TRAILING);
                l.setName(complist[i].getName());
                panel2.add(l);
                String type = complist[i].getType();
                if (type.equals("text") || type.equals("num")){                    
                    JTextField t = new JTextField();
                    t.setText(complist[i].getValue());
                    l.setLabelFor(t);
                    panel2.add(t);
                    count2++;
                }
                else if (type.equals("combo") || type.equals("bool")){
                    JComboBox cb = new JComboBox(complist[i].getValue().split(", "));
                    l.setLabelFor(cb);
                    panel2.add(cb);
                    count1++;
                }
                else if (type.equals("key")){                    
                    JTextField t = new JTextField();
                    t.setText(complist[i].getValue());                   
                    l.setLabelFor(t);
                    panel2.add(t);
                    count1++;
                } 
            }
        }
        parts = 2*(count1+count2);
        while(parts != (parts/6)*6){
            JLabel l = new JLabel("", JLabel.TRAILING);
            panel2.add(l);
            parts++;
        }
         //Lay out the panel.
        SpringUtilities.makeCompactGrid(panel2,
                                        parts/6, 6, //rows, cols
                                        6, 6,        //initX, initY
                                        6, 6);       //xPad, yPad

        panel2.revalidate();
        panel2.repaint();

    }
    
    //construct a clientstub message out of the given panel
    public String PanelToString(String type, JPanel panel){
        GuiComponent[] targetCompList = null;
        String g_params = "";
        String p_params = "";
        
        if (type.equals("user"))
            targetCompList = compList_user;
        else if (type.equals("slice"))
            targetCompList = compList_slice;
        else if (type.equals("node"))
            targetCompList = compList_node;
        else if (type.equals("SA/MA"))
            targetCompList = compList_site;
        
        //serialize the components on the component list
        Component carr[] = panel.getComponents();
        for(int i = 0; i<carr.length; i++){
            Component nextcomp = carr[i];                     
            String comp_name = nextcomp.getName();            
            int j;
            for(j = 0; j<targetCompList.length; j++){
                String cur_name = targetCompList[j].getName();
                if (cur_name.equals(comp_name)){
                    break;
                }
            }
            if (j == targetCompList.length)
                continue;
            else{
                String comp_type = targetCompList[j].getType();
                String comp_content = "";
                if (comp_type.equals("text") || comp_type.equals("num")){
                    JTextField tf = (JTextField)carr[i+1];
                    String tf_content = tf.getText();
                    if (tf_content.length() == 0)
                        continue;
                    else if(comp_type.equals("text"))
                        comp_content = "'"+tf_content+"'";
                    else
                        comp_content = tf_content;
                }
                else if (comp_type.equals("bool")){
                    JComboBox cb = (JComboBox)carr[i+1];
                    String cb_content = (String) cb.getSelectedItem();
                    if (cb_content.equals("Yes"))
                        comp_content = "True";
                    else
                        comp_content = "False";                
                }
                else if (comp_type.equals("combo")){
                    JComboBox cb = (JComboBox)carr[i+1];
                    String cb_content = (String) cb.getSelectedItem();
                    comp_content = "'"+cb_content+"'";                
                }
                else if (comp_type.equals("key")){
                    JTextField tf = (JTextField)carr[i+1];
                    String tf_content = tf.getText();                    
                    
                    if (tf_content.length() == 0)
                        continue;
                    else
                        comp_content = "'"+tf_content+"'";                                        
                }
                //add to dictionary string
                if (comp_name.equals("key_write"))
                    comp_name = "key";
                else if (comp_name.equals("pubkey_write"))
                    comp_name = "pubkey";
                if (targetCompList[j].getProperty()[1].equals("geni")){
                    if (g_params.length() == 0)
                        g_params += ("'"+comp_name+"':"+comp_content);
                    else
                        g_params += (", '"+comp_name+"':"+comp_content);
                }
                else{
                    if (p_params.length() == 0)
                        p_params += ("'"+comp_name+"':"+comp_content);
                    else
                        p_params += (", '"+comp_name+"':"+comp_content);                
                }                    
            }
        }        
        return "'g_params':{"+g_params+"}, 'p_params':{"+p_params+"}";
    }
    
    private BufferedWriter outCommand = null;
    private JFrame keySelectFrame = null;
    private GuiComponent[] compList_slice;
    private GuiComponent[] compList_user;
    private GuiComponent[] compList_node;
    private GuiComponent[] compList_site;
    
}
