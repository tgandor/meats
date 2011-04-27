/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package com.googlecode.meats;

import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import javax.microedition.io.Connector;
import javax.microedition.io.file.FileConnection;

/**
 *
 * @author olaija
 */
public class VCardParser {
    private String fileURL;
    private FileConnection fc;
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
                sb.append(c);
            }
        } catch (IOException ioe) {
        }
        return sb.toString();
    }
    
    public VCardParser(String url) {
        fileURL = url;
        try {
            fc = (FileConnection) Connector.open(fileURL);
            rr = new InputStreamReader(fc.openInputStream());
        } catch (IOException ex) {
        }
    }
}
