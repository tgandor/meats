/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package com.googlecode.meats;

import javax.microedition.lcdui.StringItem;

/**
 *
 * @author olaija
 */
public class StringSetter implements Runnable {

    private StringItem strItem;

    private StringGetter strGetter;

    public StringSetter(StringItem si, StringGetter sg) {
        strItem = si;
        strGetter = sg;
    }

    public void run() {
        if (strItem != null) {
            strItem.setText(strGetter.get());
        }
    }

}
