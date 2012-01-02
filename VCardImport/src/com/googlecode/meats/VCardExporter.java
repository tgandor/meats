package com.googlecode.meats;

import java.io.ByteArrayOutputStream;
import java.io.UnsupportedEncodingException;
import java.util.Enumeration;
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
     * @return vCard string for (currently) first contact
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
}
