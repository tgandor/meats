package com.googlecode.meats;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.util.Calendar;
import java.util.Date;
import java.util.Enumeration;
import java.util.Vector;
import javax.microedition.io.Connector;
import javax.microedition.io.file.FileConnection;
import javax.microedition.io.file.FileSystemRegistry;
import javax.microedition.pim.Contact;
import javax.microedition.pim.ContactList;
import javax.microedition.pim.PIM;
import javax.microedition.pim.PIMException;

/**
 * A class for exporting contacts to file
 * @author olaija
 */
public class VCardExporter {
    /*
     * @param atMost limit of contacts to return
     * @return vCard string for the contact(s)
     */
    public static String dumpSome(int atMost)
    {
        try {
            PIM pim = PIM.getInstance();
            ContactList cl = (ContactList) pim.openPIMList(PIM.CONTACT_LIST, PIM.READ_ONLY);
            Enumeration items = cl.items();
            int processed = 0;
            StringBuffer sb = new StringBuffer("\n");
            while ( items.hasMoreElements() && atMost != 0) {
                Contact c = (Contact) items.nextElement();
                ByteArrayOutputStream bo = new ByteArrayOutputStream();
                pim.toSerialFormat(c, bo, null, "VCARD/2.1");
                --atMost;
                ++processed;
                sb.append(bo.toString());
                sb.append("-------\n");
            }
            cl.close();
            sb.append("Total: "+processed);
            return sb.toString();
        }
        catch (PIMException pe) {
            return "Export failed:\n" + pe.getMessage();
        }
        catch (UnsupportedEncodingException e) {
            return "Problem with encoding:\n" + e.getMessage();
        }
    }

    public static String dumpAll()
    {
        return dumpSome(-1);
    }
    
    public static String[] findWritableDirectories()
    {
        Enumeration roots = FileSystemRegistry.listRoots();
        Vector results = new Vector();
        Fifo queue = new Fifo(roots);
        while(!queue.isEmpty()) {
            String root = (String) queue.dequeue();
            try {
                FileConnection fc = (FileConnection) Connector.open("file:///"+root);
                if ( fc.canWrite() )
                    results.addElement(root);     
                else {
                    // results.addElement(root+" not writable.");
                    Enumeration dir = fc.list();
                    while(dir.hasMoreElements()) {
                        String entry = (String) dir.nextElement();
                        if ( entry.endsWith("/") )
                            queue.enqueue(root + entry);
                    }
                }
            }
            catch(Exception ioe) {
                results.addElement(root+" failed: "+ioe.getMessage());
            }
        }
        String[] result = new String[results.size()];
        results.copyInto(result);
        return result;
    }
    
    public static String[] findVCards() 
    {
        Vector results = new Vector();
        Enumeration roots = FileSystemRegistry.listRoots();
        Fifo queue = new Fifo(roots);
        while(!queue.isEmpty()) {
            String root = (String) queue.dequeue();
            try {
                FileConnection fc = (FileConnection) Connector.open("file:///"+root);
                Enumeration dir = fc.list();
                while(dir.hasMoreElements()) {
                    String entry = (String) dir.nextElement();
                    if ( entry.endsWith("/") )
                        queue.enqueue(root + entry);
                    else if ( entry.toLowerCase().endsWith(".vcf") )
                        results.addElement(root + entry);
                }
            }
            catch(Exception ioe) {
                results.addElement(root + " failed: " + ioe.getMessage());
            }
        }
        String[] result = new String[results.size()];
        results.copyInto(result);
        return result;
    }
    
    public static String getFilenameSuggestion()
    {
        String platform = System.getProperty("microedition.platform");
        int slash = platform.indexOf("/");
        if (  slash != -1 ) 
            platform = platform.substring(slash+1, platform.length());
        Calendar cal = Calendar.getInstance();  
        cal.setTime(new Date());
        return platform + "_" + cal.get(Calendar.YEAR) + 
                ArrayUtils.pad(cal.get(Calendar.MONTH)+1, 2) + 
                ArrayUtils.pad(cal.get(Calendar.DAY_OF_MONTH), 2) + "_" + 
                ArrayUtils.pad(cal.get(Calendar.HOUR_OF_DAY), 2) + 
                ArrayUtils.pad(cal.get(Calendar.MINUTE),2 ) + ".vcf";
    }
    
    public static String exportContacts(String filename)
    {
        try {
            int processed = 0;
            FileConnection fc = (FileConnection) Connector.open("file:///"+filename, Connector.READ_WRITE);
            if ( !fc.exists() )
                fc.create();    
            OutputStream os = fc.openOutputStream();
            PIM pim = PIM.getInstance();
            ContactList cl = (ContactList) pim.openPIMList(PIM.CONTACT_LIST, PIM.READ_ONLY);
            Enumeration items = cl.items();
            while ( items.hasMoreElements() ) {
                Contact c = (Contact) items.nextElement();
                pim.toSerialFormat(c, os, null, "VCARD/2.1");
                ++processed;
            }
            cl.close();
            os.close();
            fc.close();
            return "Processed " + processed + " contacts.";       
        } catch ( IOException ioe ) {
            return "IO Error: " + ioe.getMessage();
        } catch ( PIMException pe ) {
            return "PIM Error: " + pe.getMessage();
        }
    }
}
