/*
 * PanelFiller.java
 *
 * Created on March 29, 2008, 10:45 PM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package javaapplication1;

import java.io.*;
import javax.swing.*;
import javax.swing.JOptionPane;

/**
 *
 * @author soners
 */
public class PanelFiller {
    
    /** Creates a new instance of PanelFiller */
    public PanelFiller(JPanel[] panelList, JLabel statusLabel) {
        panel1 = panelList[0];
        panel2 = panelList[1];
        panel3 = panelList[2];
        panel4 = panelList[3];
        panel5 = panelList[4];
        this.statusLabel = statusLabel;               
        
        try{
            rtime = Runtime.getRuntime();
            child = rtime.exec("/bin/bash");
            outCommand = new BufferedWriter(new OutputStreamWriter(child.getOutputStream()));
        }catch (Exception e){
            JOptionPane.showMessageDialog(null, "The program cannot start bash.\n");
            return;
        }
        
        displayHandle = new DisplayHandle(outCommand);
    }
    
    public void handleOperation(String opname){
        
        JPanel curpanel = null;
        String type = record.getType();
        if (type.equals("user"))
            curpanel = panel2;
        else if (type.equals("slice"))
            curpanel = panel3;
        else if (type.equals("node"))
            curpanel = panel4;
        else if (type.equals("SA")){
            curpanel = panel5;
            type = "SA/MA";
        }
        else if (type.equals("MA")){
            curpanel = panel5;
            type = "SA/MA";
        }
               
        if (opname.equals("register")){
            String params = displayHandle.PanelToString(type, curpanel);
            String rest = params.substring(12);
            if (rest.charAt(0)=='}')
                params = "'g_params':{'hrn':'"+record.getHrn()+"', 'type':'"+record.getType()+"'"+rest;
            else
                params = "'g_params':{'hrn':'"+record.getHrn()+"', 'type':'"+record.getType()+"', "+rest;
            String message = "{'opname':'"+opname+"', "+params+"}";
            String result = SendToClientStub(message);
            String[] res_arr = result.split("\n");
            String send_str = "";
            for (int i=0; i<res_arr.length; i++)
                send_str += res_arr[i];
            statusLabel.setText(send_str);            
        }
        else if (opname.equals("remove")){
            String gparams = "{'hrn':'"+record.getHrn()+"', 'type':'"+record.getType()+"'}";
            String pparams = "{}";
            String message = "{'opname':'"+opname+"', 'g_params':"+gparams+", 'p_params':"+pparams+"}";
            String result = SendToClientStub(message);
            String[] res_arr = result.split("\n");
            String send_str = "";
            for (int i=0; i<res_arr.length; i++)
                send_str += res_arr[i];
            statusLabel.setText(send_str);        
        }
        else if (opname.equals("update")){
            String params = displayHandle.PanelToString(type, curpanel);
            String rest = params.substring(12);
            if (rest.charAt(0)=='}')
                params = "'g_params':{'hrn':'"+record.getHrn()+"', 'type':'"+record.getType()+"'"+rest;
            else
                params = "'g_params':{'hrn':'"+record.getHrn()+"', 'type':'"+record.getType()+"', "+rest;
            String message = "{'opname':'"+opname+"', "+params+"}";
            String result = SendToClientStub(message);
            String[] res_arr = result.split("\n");
            String send_str = "";
            for (int i=0; i<res_arr.length; i++)
                send_str += res_arr[i];
            statusLabel.setText(send_str);        
        }
        else if (opname.equals("lookup")){
            String gparams = "{'hrn':'"+record.getHrn()+"', 'type':'"+record.getType()+"'}";
            String pparams = "{}";
            String message = "{'opname':'"+opname+"', 'g_params':"+gparams+", 'p_params':"+pparams+"}";
            String result = SendToClientStub(message);
            String[] res_arr = result.split("\n");
            String[] send_arr = null;
            
            
            if (res_arr!=null && res_arr.length > 0){
                
                String status_str = "";
                for (int i=0; i<res_arr.length; i++){
                    if (!res_arr[i].equals("{'geni':{"))
                        status_str += res_arr[i];
                    else
                        break;
                }
                statusLabel.setText(status_str);

                //determine send_arr
                int i;
                for(i=0; i<res_arr.length && !res_arr[i].equals("{'geni':{"); i++)
                    ;
                if (i<res_arr.length && res_arr[i].equals("{'geni':{")){
                    i++;            
                    send_arr = new String[res_arr.length-i-3];
                    int p = 0;
                    while(!res_arr[i].equals("}")){
                        send_arr[p++] = res_arr[i];
                        i++;
                    }
                    i = i+2;
                    while(!res_arr[i].equals("}}")){
                        send_arr[p++] = res_arr[i];
                        i++;
                    }
                    displayHandle.FillComponentList(type, send_arr);
                    if (type.equals("user"))
                        displayHandle.displayComponentList("user",panel1, panel2);
                    else if (type.equals("slice"))
                        displayHandle.displayComponentList("slice",panel1, panel3);
                    else if (type.equals("node"))
                        displayHandle.displayComponentList("node",panel1, panel4);
                    else if (type.equals("SA/MA"))
                        displayHandle.displayComponentList("SA/MA",panel1, panel5);                
                }
            }            
        }
    }
    
    private String SendToClientStub(String message){
        
        //do the call to the python client
        String curdir = System.getProperty("user.dir");
        String client_folder = user.getDirectory();      
        String result = "";
        
        try{
            //cd to the client folder            
            outCommand.write("cd "+client_folder+"\n");         
            outCommand.flush();

            FileWriter fstream = new FileWriter(client_folder+"/tmp_input.txt");
            BufferedWriter out = new BufferedWriter(fstream);
            out.write(user.getHrn()+" "+user.getType()+"\n");
            out.write(message);
            //Close the output stream
            out.close();            
            outCommand.write("./clientstub.py\n");            
            outCommand.flush();
            
            //get the result of the call from the python client          
            File file = new File(client_folder+"/tmp_output.txt");
            int i = 0;
            while(!file.exists() && i<5){
                i++;
                try {
                    Thread.currentThread().sleep(200);
                } catch (InterruptedException ex) {
                    ex.printStackTrace();
                    result = "Problem occured in client stub.\n";                
                    return result;
                }
            }

            try {
                Thread.currentThread().sleep(200);
            } catch (InterruptedException ex) {
                ex.printStackTrace();
                result = "Problem occured in client stub.\n";
                return result;
            }        
    
            BufferedReader in = new BufferedReader(new FileReader(client_folder+"/tmp_output.txt")); 
            result = "";
            String tmp = in.readLine();
            while(tmp!=null && tmp.length() > 0){
                result += tmp+"\n";
                tmp = in.readLine();
            }                
            in.close();
            
            outCommand.write("rm tmp_input.txt tmp_output.txt\n");            
            outCommand.write("cd "+curdir+"\n");   
            outCommand.flush();
        }catch (Exception e){//Catch exception if any            
            System.err.println("Error: " + e.getMessage());
            result = "Problem occured in client stub.\n";
            return result;
        }
        return result;
    }
    
    public void initializePanels(){
        displayHandle.displayComponentList("user",panel1, panel2);
        displayHandle.displayComponentList("slice",panel1, panel3);
        displayHandle.displayComponentList("node",panel1, panel4);
        displayHandle.displayComponentList("SA/MA",panel1, panel5);        
    }
    
    public void setUser(User user){
        this.user = user;    
    }
    public void setRecord(RecordInfo record){
        this.record = record;    
    }
            
    private User user;
    private RecordInfo record;
    private javax.swing.JPanel panel1;
    private javax.swing.JPanel panel2;
    private javax.swing.JPanel panel3;
    private javax.swing.JPanel panel4;
    private javax.swing.JPanel panel5;
    private javax.swing.JLabel statusLabel;
    
    private BufferedWriter outCommand;
    private Runtime rtime;
    private Process child;
    
    private DisplayHandle displayHandle;
    
}


