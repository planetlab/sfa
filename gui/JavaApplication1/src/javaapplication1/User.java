/*
 * User.java
 *
 * Created on March 29, 2008, 11:36 PM
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
public class User {
    
    /** Creates a new instance of User */
    public User() {
    }
    
    public void setCurrentUser(String hrn, String type, String directory){
        this.hrn = hrn;
        this.type = type;
        this.directory = directory;        
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

    /**
     * Holds value of property directory.
     */
    private String directory;

    /**
     * Getter for property directory.
     * @return Value of property directory.
     */
    public String getDirectory() {
        return this.directory;
    }

    /**
     * Setter for property directory.
     * @param directory New value of property directory.
     */
    public void setDirectory(String directory) {
        this.directory = directory;
    }
    
}
