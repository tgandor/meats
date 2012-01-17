/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package com.googlecode.meats;

import java.io.*;
import java.util.Enumeration;
import java.util.Hashtable;
import java.util.Vector;
import javax.microedition.io.Connector;
import javax.microedition.io.file.FileConnection;
import javax.microedition.pim.Contact;
import javax.microedition.pim.ContactList;
import javax.microedition.pim.PIM;
import javax.microedition.pim.PIMException;

/**
 * This class 
 * @author olaija
 */
public class VCardParser {
    private String fileURL;
    private FileConnection fc;
    private InputStream is;
    private Reader rr;

    private int numImported = 0;
    private int numAttempted = 0;
    private int numRead = 0;

    public String readline() {
        StringBuffer sb = new StringBuffer();
        int i;
        char c;
        try {
            while ( true ) {
                i = rr.read();
                if (i == -1)
                    break;
                c = (char) i;
                if (c == '\n')
                    break;
                // carrige return suppression
                if ( c == '\r' )
                    continue;
                    // sb.append("\\r");
                else
                    sb.append(c);
            }
        } catch (IOException ioe) {
            return null;
        }
        if ( i == -1 && sb.length() == 0)
            return null;
        return sb.toString();
    }
    
    public VCardParser(String url) {
        fileURL = url;
        try {
            fc = (FileConnection) Connector.open(fileURL);
            is = fc.openInputStream();
            rr = new InputStreamReader(is);
        } catch (IOException ex) {
        }
    }

    public Contact[] getContacts() throws PIMException, UnsupportedEncodingException {
        PIM pim = PIM.getInstance();
        Vector v = new Vector();
        try {
            while ( true ) {
                Contact[] portion = (Contact[]) pim.fromSerialFormat(is, null);
                for(int i = 0; i < portion.length; ++i) {
                    v.addElement(portion[i]);
                    ++numRead;
                }
            }
        } catch (PIMException e) {}
        Contact[] contacts = new Contact[v.size()];
        v.copyInto(contacts);
        return contacts;
    }

    public void importContacts() throws PIMException, UnsupportedEncodingException {
        ContactList contacts = (ContactList) PIM.getInstance().openPIMList(PIM.CONTACT_LIST, PIM.READ_WRITE);
        Contact[] imported = getContacts();
        for(int i = 0; i < imported.length; ++i) {
            ++numAttempted;
            Contact newOne = contacts.importContact(imported[i]);
            Enumeration duplicates = contacts.items(newOne);
            if ( !duplicates.hasMoreElements() ) {
                newOne.commit();
                ++numImported;
            }
        }
        contacts.close();
    }
    
    private Hashtable getContactDict(int field)
    {
        Hashtable result = new Hashtable();
        try {
            ContactList contacts = (ContactList) PIM.getInstance().openPIMList(PIM.CONTACT_LIST, PIM.READ_ONLY);
            if ( contacts.isSupportedField(field) )
                return result;
            Enumeration all = contacts.items();
            while(all.hasMoreElements())
            {
                Contact c = (Contact)all.nextElement();
                for(int i=0; i<c.countValues(field); ++i)
                    result.put(c.getString(field, i), c);
            }
        } catch (PIMException ex) {
            ex.printStackTrace();
        }
        return result;
    }

    /**
     * @return the numImported
     */
    public int getNumImported() {
        return numImported;
    }

    /**
     * @return the numAttempted
     */
    public int getNumAttempted() {
        return numAttempted;
    }

    /**
     * @return the numRead
     */
    public int getNumRead() {
        return numRead;
    }
    
}
