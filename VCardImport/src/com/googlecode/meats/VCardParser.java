package com.googlecode.meats;

import java.io.IOException;
import java.io.InputStream;
import java.io.UnsupportedEncodingException;
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
 * Used for getting contacts out of a vCard file
 * @author olaija
 */
public class VCardParser {
    private String fileURL = null;
    private FileConnection fc = null;
    private InputStream is = null;

    private int numImported = 0;
    private int numAttempted = 0;
    private int numRead = 0;
   
    public VCardParser(String url) {
        fileURL = url;
        try {
            fc = (FileConnection) Connector.open(fileURL);
            is = fc.openInputStream();
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
