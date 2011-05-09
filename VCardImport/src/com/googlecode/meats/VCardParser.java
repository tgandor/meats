/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package com.googlecode.meats;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.UnsupportedEncodingException;
import javax.microedition.io.Connector;
import javax.microedition.io.file.FileConnection;

import javax.microedition.pim.PIM;
import javax.microedition.pim.Contact;
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
        return (Contact []) pim.fromSerialFormat(is, null);
    }
}
