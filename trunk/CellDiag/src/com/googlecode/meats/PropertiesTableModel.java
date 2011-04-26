/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */
package com.googlecode.meats;

import org.netbeans.microedition.lcdui.SimpleTableModel;

/**
 * This is a table model of common MIDP java.lang.System
 * properties.
 *
 * @author olaija
 */
public class PropertiesTableModel extends SimpleTableModel {

    public PropertiesTableModel() {
        super(new String[][]{
                    new String[]{"30", "microedition.platform", "null"},
                    new String[]{"30", "microedition.encoding", "ISO8859_1"},
                    new String[]{"30", "microedition.configuration", "CLDC-1.0"},
                    new String[]{"30", "microedition.profiles", "null"},
                    new String[]{"37", "microedition.locale", "null"},
                    new String[]{"37", "microedition.profiles", "MIDP-1.0"},
                    new String[]{"75", "microedition.io.file.FileConnection.version", "1.0"},
                    new String[]{"75", "file.separator", "(impl-dep)"},
                    new String[]{"75", "microedition.pim.version", "1.0"},
                    new String[]{"118", "microedition.locale", "null"},
                    new String[]{"118", "microedition.profiles", "MIDP-2.0"},
                    new String[]{"118", "microedition.commports", "(impl-dep)"},
                    new String[]{"118", "microedition.hostname", "(impl-dep)"},
                    new String[]{"120", "wireless.messaging.sms.smsc", "(impl-dep)"},
                    new String[]{"139", "microedition.platform", "(impl-dep)"},
                    new String[]{"139", "microedition.encoding", "ISO8859-1"},
                    new String[]{"139", "microedition.configuration", "CLDC-1.1"},
                    new String[]{"139", "microedition.profiles", "(impl-dep)"},
                    new String[]{"177", "microedition.smartcardslots", "(impl-dep)"},
                    new String[]{"179", "microedition.location.version", "1.0"},
                    new String[]{"180", "microedition.sip.version", "1.0"},
                    new String[]{"184", "microedition.m3g.version", "1.0"},
                    new String[]{"185", "microedition.jtwi.version", "1.0"},
                    new String[]{"195", "microedition.locale", "(impl-dep)"},
                    new String[]{"195", "microedition.profiles", "IMP-1.0"},
                    new String[]{"205", "wireless.messaging.sms.smsc", "(impl-dep)"},
                    new String[]{"205", "wireless.messaging.mms.mmsc", "(impl-dep)"},
                    new String[]{"211", "CHAPI-Version", "1.0"}
                },
                new String[]{"JSR", "Property", "Value"});
    }

    public Object getValue(int col, int row) {
        if ( col == 2 )
            return System.getProperty((String)super.getValue(1, row));
        return super.getValue(col, row);
    }
}
