/*
 * RecordInfo.java
 *
 * Created on March 30, 2008, 12:07 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package javaapplication1;
import javax.swing.*;

/**
 *
 * @author soners
 */
public class RecordInfo {
    
    /** Creates a new instance of RecordInfo */
    public RecordInfo() {
    }
    
    public void setCurrentRecord(String hrn, String type){
        this.hrn = hrn;
        this.type = type;        
    }


    /**
     * Holds value of property hrn.
     */
    private String hrn;

    /**
     * Getter for property hrn.
     * @return Value of property hrn.
     */
    public String getHrn() {
        return this.hrn;
    }

    /**
     * Setter for property hrn.
     * @param hrn New value of property hrn.
     */
    public void setHrn(String hrn) {
        this.hrn = hrn;
    }

    /**
     * Holds value of property type.
     */
    private String type;

    /**
     * Getter for property type.
     * @return Value of property type.
     */
    public String getType() {
        return this.type;
    }

    /**
     * Setter for property type.
     * @param type New value of property type.
     */
    public void setType(String type) {
        this.type = type;
    }
    
}
