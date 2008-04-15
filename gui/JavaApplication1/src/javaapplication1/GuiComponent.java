/*
 * GuiComponent.java
 *
 * Created on March 29, 2008, 2:45 AM
 *
 * To change this template, choose Tools | Template Manager
 * and open the template in the editor.
 */

package javaapplication1;

/**
 *
 * @author soners
 */
public class GuiComponent {
    
    /** Creates a new instance of GuiComponent */
    public GuiComponent(String name, String[] property, String type, String label, String defaultVal) {
        this.name = name;
        this.property = property;
        this.type = type;
        this.label = label;
        this.value = defaultVal;
        
    }
    private String[] property;
    private String type;
    private String label;
    private String value;

    /**
     * Holds value of property name.
     */
    private String name;

    /**
     * Getter for property name.
     * @return Value of property name.
     */
    public String getName() {
        return this.name;
    }

    /**
     * Setter for property name.
     * @param name New value of property name.
     */
    public void setName(String name) {
        this.name = name;
    }

    /**
     * Getter for property property.
     * @return Value of property property.
     */
    public String[] getProperty() {
        return this.property;
    }

    /**
     * Setter for property property.
     * @param property New value of property property.
     */
    public void setProperty(String[] property) {
        this.property = property;
    }

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
     * Getter for property label.
     * @return Value of property label.
     */
    public String getLabel() {
        return this.label;
    }

    /**
     * Setter for property label.
     * @param label New value of property label.
     */
    public void setLabel(String label) {
        this.label = label;
    }

    /**
     * Getter for property value.
     * 
     * @return Value of property value.
     */
    public String getValue() {
        return this.value;
    }

    /**
     * Setter for property value.
     * 
     * @param value New value of property value.
     */
    public void setValue(String defaultVal) {
        this.value = defaultVal;
    }

}
