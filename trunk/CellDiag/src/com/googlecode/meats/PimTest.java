/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package com.googlecode.meats;

/**
 *
 * @author olaija
 */
public class PimTest {

    public static boolean run() {
        try {
            Class.forName("javax.microedition.pim.ContactList");
        } catch(ClassNotFoundException e) {
            return false;
        }
        return true;
    }
}
