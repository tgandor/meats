/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package com.googlecode.meats;

import com.googlecode.meats.mappers.IntStr;
import java.util.Enumeration;
import java.util.Vector;
import javax.microedition.pim.Contact;
import javax.microedition.pim.ContactList;
import javax.microedition.pim.PIMException;
import javax.microedition.pim.PIMItem;
import javax.microedition.pim.PIM;
import org.apache.commons.lang.StringUtils;

/**
 * Helper class for accessing properties of present PIM implementation.
 * @author olaija
 */
public class PimDiag {

    public static int valueFormat = 0;

    private static String par(int n)
    {
        switch(valueFormat)
        {
            case 0:
                return " ("+n+")";
            default:
                return "";
        }
    }

    private static String getDatatypeLabel(int datatype)
    {
        switch(datatype) {
            case PIMItem.DATE:
                return "DATE";
            case PIMItem.STRING:
                return "STRING";
            case PIMItem.STRING_ARRAY:
                return "STRING_ARRAY";
            case PIMItem.BOOLEAN:
                return "BOOLEAN";
            case PIMItem.BINARY:
                return "BINARY";
            case PIMItem.INT:
                return "INT";
            default:
                return "?";
        }
    }
    
    private static String getFieldSymbol(int field)
    {
        switch(field) {
            case Contact.ADDR:
                return "ADDR";
            case Contact.BIRTHDAY:
                return "BIRTHDAY";
            case Contact.CLASS:
                return "CLASS";
            case Contact.EMAIL:
                return "EMAIL";
            case Contact.FORMATTED_ADDR:
                return "FORMATTED_ADDR";
            case Contact.FORMATTED_NAME:
                return "FORMATTED_NAME";
            case Contact.NAME:
                return "NAME";
            case Contact.NICKNAME:
                return "NICKNAME";
            case Contact.NOTE:
                return "NOTE";
            case Contact.ORG:
                return "ORG";
            case Contact.PHOTO:
                return "PHOTO";
            case Contact.PHOTO_URL:
                return "PHOTO_URL";
            case Contact.PUBLIC_KEY:
                return "PUBLIC_KEY";
            case Contact.PUBLIC_KEY_STRING:
                return "PUBLIC_KEY_STRING";
            case Contact.REVISION:
                return "REVISION";
            case Contact.TEL:
                return "TEL";
            case Contact.TITLE:
                return "TITLE";
            case Contact.UID:
                return "UID";
            case Contact.URL:
                return "URL";                
            default: 
                return "?";
        }
    }

    public static String getSerialFormats() {
        PIM pim = PIM.getInstance();
        String[] formats = pim.supportedSerialFormats(PIM.CONTACT_LIST);
        return "\n" + StringUtils.join(formats, "\n");
    }

    public static String getContactLists() {
        String[] lists = PIM.getInstance().listPIMLists(PIM.CONTACT_LIST);
        return "\n" + StringUtils.join(lists, "\n");
    }

    public static String getCategories() {
        try { 
            ContactList contacts = (ContactList) PIM.getInstance().openPIMList(PIM.CONTACT_LIST, PIM.READ_ONLY);
            String[] categories = contacts.getCategories();
            if (categories.length == 0)
                return "\n(no categories)";
            return "\n" + StringUtils.join(categories, "\n");
        }
        catch ( PIMException pe ) {
            return "\nerror retrieving:\n"+pe.getClass().getName()+"\n"+
                    pe.getMessage();
        }
    }

    public static String getSupportedFieldAttr() throws PIMException {
        final ContactList contacts = (ContactList) PIM.getInstance().openPIMList(PIM.CONTACT_LIST, PIM.READ_ONLY);
        int[] fields = contacts.getSupportedFields();
        ArrayUtils.sort(fields);
        Vector labels = new Vector();
        for(int i=0; i<fields.length; ++i) {
            int dataType = contacts.getFieldDataType(fields[i]);
            labels.addElement(ArrayUtils.pad(i+1, 2)+". "+
                    fields[i] +" : "+
                    getFieldSymbol(fields[i]) + " : " +
                    getDatatypeLabel(dataType));
            
            int[] attrs = contacts.getSupportedAttributes(fields[i]);
            ArrayUtils.sort(attrs);
            if ( attrs.length > 1 )
                labels.addElement("Attribs: " + StringUtils.join(Mapper.map(attrs, new IntStr() {
                public String map(int val) {
                    return contacts.getAttributeLabel(val) + par(val);
                }
            }), ", "));
            

            if ( dataType == PIMItem.STRING_ARRAY )
            {
                int[] elements = contacts.getSupportedArrayElements(fields[i]);
                for(int j=0; j<elements.length; ++j)
                    labels.addElement("["+j+"] " + contacts.getArrayElementLabel(fields[i], elements[j]));
            }
        }
        return "\n" + StringUtils.join(labels.elements(), '\n');
    }

    public static String getSupportedFields()
    {
        try {
            return getSupportedFieldAttr();
        } catch (PIMException pe) {
            return "\nerror retrieving:\n"+pe.getClass().getName()+"\n"+
                    pe.getMessage();
        }
    }

}
