/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package com.googlecode.meats;

import java.util.Enumeration;
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

    public static String getSerialFormats() {
        PIM pim = PIM.getInstance();
        String[] formats = pim.supportedSerialFormats(PIM.CONTACT_LIST);
        return "\n" + StringUtils.join(formats, "\n");
    }

    public static String getContactLists() {
        String[] lists = PIM.getInstance().listPIMLists(PIM.CONTACT_LIST);
        return "\n" + StringUtils.join(lists);
    }
}
