/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package com.googlecode.meats;

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
                return "strange";
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

    public static String getCategories() throws PIMException {
        ContactList contacts = (ContactList) PIM.getInstance().openPIMList(PIM.CONTACT_LIST, PIM.READ_ONLY);
        String[] categories = contacts.getCategories();
        if (categories.length == 0)
            return "\n(no categories)";
        return "\n" + StringUtils.join(categories, "\n");
    }

    public static String getSupportedFields() throws PIMException {
        ContactList contacts = (ContactList) PIM.getInstance().openPIMList(PIM.CONTACT_LIST, PIM.READ_ONLY);
        int[] fields = contacts.getSupportedFields();
        String[] labels = new String[fields.length];
        for(int i=0; i<fields.length; ++i)
            labels[i] = contacts.getFieldLabel(fields[i]);
        return "\n" + StringUtils.join(labels, "\n");
    }

    public static String getSupportedFieldAttr() throws PIMException {
        ContactList contacts = (ContactList) PIM.getInstance().openPIMList(PIM.CONTACT_LIST, PIM.READ_ONLY);
        int[] fields = contacts.getSupportedFields();
        Vector labels = new Vector();
        for(int i=0; i<fields.length; ++i) {
            String field = contacts.getFieldLabel(fields[i]);
            int dataType = contacts.getFieldDataType(fields[i]);
            labels.addElement(field+" : "+getDatatypeLabel(dataType)+par(dataType));

            int[] attrs = contacts.getSupportedAttributes(fields[i]);
            for(int j=1; j<attrs.length; ++j)
                labels.addElement("atr:" + contacts.getAttributeLabel(attrs[j]) + par(attrs[j]));

            if ( dataType == PIMItem.STRING_ARRAY )
            {
                int[] elements = contacts.getSupportedArrayElements(fields[i]);
                for(int j=0; j<elements.length; ++j)
                    labels.addElement("["+j+"] " + contacts.getArrayElementLabel(fields[i], elements[j]));
            }
        }
        return "\n" + StringUtils.join(labels.elements(), '\n');
    }

}
