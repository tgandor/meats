package com.googlecode.meats;

import java.io.UnsupportedEncodingException;
import javax.microedition.midlet.*;
import javax.microedition.lcdui.*;
import javax.microedition.pim.PIM;
import javax.microedition.pim.PIMException;
import org.netbeans.microedition.lcdui.WaitScreen;
import org.netbeans.microedition.lcdui.pda.FileBrowser;
import org.netbeans.microedition.lcdui.pda.FileBrowser;
import org.netbeans.microedition.lcdui.pda.PIMBrowser;
import org.netbeans.microedition.util.SimpleCancellableTask;

/**
 * @author olaija
 */
public class VCardImport extends MIDlet implements CommandListener {

    private boolean midletPaused = false;

    private VCardParser lastParser = null;
    
    //<editor-fold defaultstate="collapsed" desc=" Generated Fields ">//GEN-BEGIN:|fields|0|
    private Command exitCommand;
    private Command okCommand;
    private Command cancelCommand;
    private Command itemCommand;
    private Command okCommandDiag;
    private Command exitCommand1;
    private Command backCommand;
    private Form welcome;
    private StringItem stringItem;
    private FileBrowser fileBrowser;
    private Alert alert;
    private Form formDiag;
    private StringItem stringItem4;
    private StringItem stringItem3;
    private StringItem stringItem2;
    private StringItem stringItem1;
    private PIMBrowser pimBrowser;
    private List mainMenu;
    //</editor-fold>//GEN-END:|fields|0|

    /**
     * The VCardImport constructor.
     */
    public VCardImport() {
    }

    //<editor-fold defaultstate="collapsed" desc=" Generated Methods ">//GEN-BEGIN:|methods|0|
    //</editor-fold>//GEN-END:|methods|0|

    //<editor-fold defaultstate="collapsed" desc=" Generated Method: initialize ">//GEN-BEGIN:|0-initialize|0|0-preInitialize
    /**
     * Initilizes the application.
     * It is called only once when the MIDlet is started. The method is called before the <code>startMIDlet</code> method.
     */
    private void initialize() {//GEN-END:|0-initialize|0|0-preInitialize
        // write pre-initialize user code here
//GEN-LINE:|0-initialize|1|0-postInitialize
        // write post-initialize user code here
    }//GEN-BEGIN:|0-initialize|2|
    //</editor-fold>//GEN-END:|0-initialize|2|

    //<editor-fold defaultstate="collapsed" desc=" Generated Method: startMIDlet ">//GEN-BEGIN:|3-startMIDlet|0|3-preAction
    /**
     * Performs an action assigned to the Mobile Device - MIDlet Started point.
     */
    public void startMIDlet() {//GEN-END:|3-startMIDlet|0|3-preAction
        // write pre-action user code here
        switchDisplayable(null, getMainMenu());//GEN-LINE:|3-startMIDlet|1|3-postAction
        // write post-action user code here
    }//GEN-BEGIN:|3-startMIDlet|2|
    //</editor-fold>//GEN-END:|3-startMIDlet|2|

    //<editor-fold defaultstate="collapsed" desc=" Generated Method: resumeMIDlet ">//GEN-BEGIN:|4-resumeMIDlet|0|4-preAction
    /**
     * Performs an action assigned to the Mobile Device - MIDlet Resumed point.
     */
    public void resumeMIDlet() {//GEN-END:|4-resumeMIDlet|0|4-preAction
        // write pre-action user code here
//GEN-LINE:|4-resumeMIDlet|1|4-postAction
        // write post-action user code here
    }//GEN-BEGIN:|4-resumeMIDlet|2|
    //</editor-fold>//GEN-END:|4-resumeMIDlet|2|

    //<editor-fold defaultstate="collapsed" desc=" Generated Method: switchDisplayable ">//GEN-BEGIN:|5-switchDisplayable|0|5-preSwitch
    /**
     * Switches a current displayable in a display. The <code>display</code> instance is taken from <code>getDisplay</code> method. This method is used by all actions in the design for switching displayable.
     * @param alert the Alert which is temporarily set to the display; if <code>null</code>, then <code>nextDisplayable</code> is set immediately
     * @param nextDisplayable the Displayable to be set
     */
    public void switchDisplayable(Alert alert, Displayable nextDisplayable) {//GEN-END:|5-switchDisplayable|0|5-preSwitch
        // write pre-switch user code here
        Display display = getDisplay();//GEN-BEGIN:|5-switchDisplayable|1|5-postSwitch
        if (alert == null) {
            display.setCurrent(nextDisplayable);
        } else {
            display.setCurrent(alert, nextDisplayable);
        }//GEN-END:|5-switchDisplayable|1|5-postSwitch
        // write post-switch user code here
    }//GEN-BEGIN:|5-switchDisplayable|2|
    //</editor-fold>//GEN-END:|5-switchDisplayable|2|

    //<editor-fold defaultstate="collapsed" desc=" Generated Method: commandAction for Displayables ">//GEN-BEGIN:|7-commandAction|0|7-preCommandAction
    /**
     * Called by a system to indicated that a command has been invoked on a particular displayable.
     * @param command the Command that was invoked
     * @param displayable the Displayable where the command was invoked
     */
    public void commandAction(Command command, Displayable displayable) {//GEN-END:|7-commandAction|0|7-preCommandAction
        // write pre-action user code here
        if (displayable == fileBrowser) {//GEN-BEGIN:|7-commandAction|1|24-preAction
            if (command == FileBrowser.SELECT_FILE_COMMAND) {//GEN-END:|7-commandAction|1|24-preAction
                getAlert().setTitle("Success?");
                switchDisplayable(getAlert(), getMainMenu());//GEN-LINE:|7-commandAction|2|24-postAction
                lastParser = new VCardParser(fileBrowser.getSelectedFileURL());
                try {
                    // lastParser.importContacts();
                    lastParser.getContacts();
                    getAlert().setTitle("Success: "+lastParser.getNumRead());
                    // getStringItem().setText("Success: "+lastParser.getNumRead());
                } catch (PIMException pe) {
                    getAlert().setTitle("PIM Error");
                    // getStringItem().setText("PIM Error occurred");
                } catch (UnsupportedEncodingException ue) {
                    getAlert().setTitle("Encoding Error");
                    //getStringItem().setText("Encoding Error occurred");
                }
                getAlert().setString("Imported "+ lastParser.getNumImported()
                        + " out of " + lastParser.getNumRead() + " ");
            } else if (command == cancelCommand) {//GEN-LINE:|7-commandAction|3|51-preAction
                // write pre-action user code here
                switchDisplayable(null, getMainMenu());//GEN-LINE:|7-commandAction|4|51-postAction
                // write post-action user code here
            }//GEN-BEGIN:|7-commandAction|5|58-preAction
        } else if (displayable == formDiag) {
            if (command == okCommandDiag) {//GEN-END:|7-commandAction|5|58-preAction
                // write pre-action user code here
                switchDisplayable(null, getMainMenu());//GEN-LINE:|7-commandAction|6|58-postAction
                // write post-action user code here
            }//GEN-BEGIN:|7-commandAction|7|66-preAction
        } else if (displayable == mainMenu) {
            if (command == List.SELECT_COMMAND) {//GEN-END:|7-commandAction|7|66-preAction
 // write pre-action user code here
                mainMenuAction();//GEN-LINE:|7-commandAction|8|66-postAction
 // write post-action user code here
            } else if (command == exitCommand1) {//GEN-LINE:|7-commandAction|9|69-preAction
 // write pre-action user code here
                exitMIDlet();//GEN-LINE:|7-commandAction|10|69-postAction
 // write post-action user code here
            }//GEN-BEGIN:|7-commandAction|11|71-preAction
        } else if (displayable == pimBrowser) {
            if (command == PIMBrowser.SELECT_PIM_ITEM) {//GEN-END:|7-commandAction|11|71-preAction
 // write pre-action user code here
                switchDisplayable(null, getMainMenu());//GEN-LINE:|7-commandAction|12|71-postAction
 // write post-action user code here
            }//GEN-BEGIN:|7-commandAction|13|83-preAction
        } else if (displayable == welcome) {
            if (command == backCommand) {//GEN-END:|7-commandAction|13|83-preAction
 // write pre-action user code here
                switchDisplayable(null, getMainMenu());//GEN-LINE:|7-commandAction|14|83-postAction
 // write post-action user code here
            }//GEN-BEGIN:|7-commandAction|15|7-postCommandAction
        }//GEN-END:|7-commandAction|15|7-postCommandAction
        // write post-action user code here
    }//GEN-BEGIN:|7-commandAction|16|
    //</editor-fold>//GEN-END:|7-commandAction|16|


    //<editor-fold defaultstate="collapsed" desc=" Generated Getter: exitCommand ">//GEN-BEGIN:|18-getter|0|18-preInit
    /**
     * Returns an initiliazed instance of exitCommand component.
     * @return the initialized component instance
     */
    public Command getExitCommand() {
        if (exitCommand == null) {//GEN-END:|18-getter|0|18-preInit
            // write pre-init user code here
            exitCommand = new Command("Exit", Command.EXIT, 0);//GEN-LINE:|18-getter|1|18-postInit
            // write post-init user code here
        }//GEN-BEGIN:|18-getter|2|
        return exitCommand;
    }
    //</editor-fold>//GEN-END:|18-getter|2|

    //<editor-fold defaultstate="collapsed" desc=" Generated Getter: welcome ">//GEN-BEGIN:|14-getter|0|14-preInit
    /**
     * Returns an initiliazed instance of welcome component.
     * @return the initialized component instance
     */
    public Form getWelcome() {
        if (welcome == null) {//GEN-END:|14-getter|0|14-preInit
            // write pre-init user code here
            welcome = new Form("Welcome", new Item[] { getStringItem() });//GEN-BEGIN:|14-getter|1|14-postInit
            welcome.addCommand(getBackCommand());
            welcome.setCommandListener(this);//GEN-END:|14-getter|1|14-postInit
            // write post-init user code here
        }//GEN-BEGIN:|14-getter|2|
        return welcome;
    }
    //</editor-fold>//GEN-END:|14-getter|2|

    //<editor-fold defaultstate="collapsed" desc=" Generated Getter: stringItem ">//GEN-BEGIN:|16-getter|0|16-preInit
    /**
     * Returns an initiliazed instance of stringItem component.
     * @return the initialized component instance
     */
    public StringItem getStringItem() {
        if (stringItem == null) {//GEN-END:|16-getter|0|16-preInit
            // write pre-init user code here
            stringItem = new StringItem("Info", "\nPress OK to pick a file and read its first line. \nThe import of vcf is not yet fully supported ;).");//GEN-LINE:|16-getter|1|16-postInit
            // write post-init user code here
        }//GEN-BEGIN:|16-getter|2|
        return stringItem;
    }
    //</editor-fold>//GEN-END:|16-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: okCommand ">//GEN-BEGIN:|28-getter|0|28-preInit
/**
 * Returns an initiliazed instance of okCommand component.
 * @return the initialized component instance
 */
public Command getOkCommand() {
    if (okCommand == null) {//GEN-END:|28-getter|0|28-preInit
            // write pre-init user code here
        okCommand = new Command("Ok", Command.OK, 0);//GEN-LINE:|28-getter|1|28-postInit
            // write post-init user code here
    }//GEN-BEGIN:|28-getter|2|
    return okCommand;
}
//</editor-fold>//GEN-END:|28-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: fileBrowser ">//GEN-BEGIN:|22-getter|0|22-preInit
/**
 * Returns an initiliazed instance of fileBrowser component.
 * @return the initialized component instance
 */
public FileBrowser getFileBrowser() {
    if (fileBrowser == null) {//GEN-END:|22-getter|0|22-preInit
            // write pre-init user code here
        fileBrowser = new FileBrowser(getDisplay());//GEN-BEGIN:|22-getter|1|22-postInit
        fileBrowser.setTitle("fileBrowser");
        fileBrowser.setCommandListener(this);
        fileBrowser.addCommand(FileBrowser.SELECT_FILE_COMMAND);
        fileBrowser.addCommand(getCancelCommand());//GEN-END:|22-getter|1|22-postInit
            // write post-init user code here
    }//GEN-BEGIN:|22-getter|2|
    return fileBrowser;
}
//</editor-fold>//GEN-END:|22-getter|2|



//<editor-fold defaultstate="collapsed" desc=" Generated Getter: alert ">//GEN-BEGIN:|48-getter|0|48-preInit
/**
 * Returns an initiliazed instance of alert component.
 * @return the initialized component instance
 */
public Alert getAlert() {
    if (alert == null) {//GEN-END:|48-getter|0|48-preInit
            // write pre-init user code here
        alert = new Alert("Read line:", "Please wait - processing", null, null);//GEN-BEGIN:|48-getter|1|48-postInit
        alert.setTimeout(Alert.FOREVER);//GEN-END:|48-getter|1|48-postInit
            // write post-init user code here
    }//GEN-BEGIN:|48-getter|2|
    return alert;
}
//</editor-fold>//GEN-END:|48-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: cancelCommand ">//GEN-BEGIN:|50-getter|0|50-preInit
/**
 * Returns an initiliazed instance of cancelCommand component.
 * @return the initialized component instance
 */
public Command getCancelCommand() {
    if (cancelCommand == null) {//GEN-END:|50-getter|0|50-preInit
            // write pre-init user code here
        cancelCommand = new Command("Cancel", Command.CANCEL, 0);//GEN-LINE:|50-getter|1|50-postInit
            // write post-init user code here
    }//GEN-BEGIN:|50-getter|2|
    return cancelCommand;
}
//</editor-fold>//GEN-END:|50-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: itemCommand ">//GEN-BEGIN:|53-getter|0|53-preInit
/**
 * Returns an initiliazed instance of itemCommand component.
 * @return the initialized component instance
 */
public Command getItemCommand() {
    if (itemCommand == null) {//GEN-END:|53-getter|0|53-preInit
            // write pre-init user code here
        itemCommand = new Command("Info", Command.ITEM, 0);//GEN-LINE:|53-getter|1|53-postInit
            // write post-init user code here
    }//GEN-BEGIN:|53-getter|2|
    return itemCommand;
}
//</editor-fold>//GEN-END:|53-getter|2|
    //</editor-fold>

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: okCommandDiag ">//GEN-BEGIN:|57-getter|0|57-preInit
/**
 * Returns an initiliazed instance of okCommandDiag component.
 * @return the initialized component instance
 */
public Command getOkCommandDiag() {
    if (okCommandDiag == null) {//GEN-END:|57-getter|0|57-preInit
            // write pre-init user code here
        okCommandDiag = new Command("Ok", Command.OK, 0);//GEN-LINE:|57-getter|1|57-postInit
            // write post-init user code here
    }//GEN-BEGIN:|57-getter|2|
    return okCommandDiag;
}
//</editor-fold>//GEN-END:|57-getter|2|
    //</editor-fold>

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: formDiag ">//GEN-BEGIN:|55-getter|0|55-preInit
/**
 * Returns an initiliazed instance of formDiag component.
 * @return the initialized component instance
 */
public Form getFormDiag() {
    if (formDiag == null) {//GEN-END:|55-getter|0|55-preInit
            // write pre-init user code here
        formDiag = new Form("PIM API diags", new Item[] { getStringItem1(), getStringItem4(), getStringItem3(), getStringItem2() });//GEN-BEGIN:|55-getter|1|55-postInit
        formDiag.addCommand(getOkCommandDiag());
        formDiag.setCommandListener(this);//GEN-END:|55-getter|1|55-postInit
            // write post-init user code here
    }//GEN-BEGIN:|55-getter|2|
    return formDiag;
}
//</editor-fold>//GEN-END:|55-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: stringItem1 ">//GEN-BEGIN:|60-getter|0|60-preInit
/**
 * Returns an initiliazed instance of stringItem1 component.
 * @return the initialized component instance
 */
public StringItem getStringItem1() {
    if (stringItem1 == null) {//GEN-END:|60-getter|0|60-preInit
            // write pre-init user code here
        stringItem1 = new StringItem("Contact List Formats", PimDiag.getSerialFormats());//GEN-LINE:|60-getter|1|60-postInit
            // write post-init user code here
    }//GEN-BEGIN:|60-getter|2|
    return stringItem1;
}
//</editor-fold>//GEN-END:|60-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: stringItem2 ">//GEN-BEGIN:|61-getter|0|61-preInit
/**
 * Returns an initiliazed instance of stringItem2 component.
 * @return the initialized component instance
 */
public StringItem getStringItem2() {
    if (stringItem2 == null) {//GEN-END:|61-getter|0|61-preInit
            // write pre-init user code here
        stringItem2 = new StringItem("Supported fields", PimDiag.getSupportedFields());//GEN-LINE:|61-getter|1|61-postInit
            // write post-init user code here
    }//GEN-BEGIN:|61-getter|2|
    return stringItem2;
}
//</editor-fold>//GEN-END:|61-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: stringItem3 ">//GEN-BEGIN:|62-getter|0|62-preInit
/**
 * Returns an initiliazed instance of stringItem3 component.
 * @return the initialized component instance
 */
public StringItem getStringItem3() {
    if (stringItem3 == null) {//GEN-END:|62-getter|0|62-preInit
            // write pre-init user code here
        stringItem3 = new StringItem("Contact categories", PimDiag.getCategories());//GEN-LINE:|62-getter|1|62-postInit
            // write post-init user code here
    }//GEN-BEGIN:|62-getter|2|
    return stringItem3;
}
//</editor-fold>//GEN-END:|62-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: stringItem4 ">//GEN-BEGIN:|63-getter|0|63-preInit
/**
 * Returns an initiliazed instance of stringItem4 component.
 * @return the initialized component instance
 */
public StringItem getStringItem4() {
    if (stringItem4 == null) {//GEN-END:|63-getter|0|63-preInit
 // write pre-init user code here
        stringItem4 = new StringItem("Contact Lists", PimDiag.getContactLists());//GEN-LINE:|63-getter|1|63-postInit
 // write post-init user code here
    }//GEN-BEGIN:|63-getter|2|
    return stringItem4;
}
//</editor-fold>//GEN-END:|63-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: exitCommand1 ">//GEN-BEGIN:|68-getter|0|68-preInit
/**
 * Returns an initiliazed instance of exitCommand1 component.
 * @return the initialized component instance
 */
public Command getExitCommand1() {
    if (exitCommand1 == null) {//GEN-END:|68-getter|0|68-preInit
 // write pre-init user code here
        exitCommand1 = new Command("Exit", Command.EXIT, 0);//GEN-LINE:|68-getter|1|68-postInit
 // write post-init user code here
    }//GEN-BEGIN:|68-getter|2|
    return exitCommand1;
}
//</editor-fold>//GEN-END:|68-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: backCommand ">//GEN-BEGIN:|82-getter|0|82-preInit
/**
 * Returns an initiliazed instance of backCommand component.
 * @return the initialized component instance
 */
public Command getBackCommand() {
    if (backCommand == null) {//GEN-END:|82-getter|0|82-preInit
 // write pre-init user code here
        backCommand = new Command("Back", Command.BACK, 0);//GEN-LINE:|82-getter|1|82-postInit
 // write post-init user code here
    }//GEN-BEGIN:|82-getter|2|
    return backCommand;
}
//</editor-fold>//GEN-END:|82-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: mainMenu ">//GEN-BEGIN:|64-getter|0|64-preInit
/**
 * Returns an initiliazed instance of mainMenu component.
 * @return the initialized component instance
 */
public List getMainMenu() {
    if (mainMenu == null) {//GEN-END:|64-getter|0|64-preInit
 // write pre-init user code here
        mainMenu = new List("Menu", Choice.IMPLICIT);//GEN-BEGIN:|64-getter|1|64-postInit
        mainMenu.append("Browse", null);
        mainMenu.append("Open", null);
        mainMenu.append("Export", null);
        mainMenu.append("Help", null);
        mainMenu.append("Info", null);
        mainMenu.addCommand(getExitCommand1());
        mainMenu.setCommandListener(this);
        mainMenu.setFitPolicy(Choice.TEXT_WRAP_DEFAULT);
        mainMenu.setSelectedFlags(new boolean[] { false, false, false, false, false });//GEN-END:|64-getter|1|64-postInit
 // write post-init user code here
    }//GEN-BEGIN:|64-getter|2|
    return mainMenu;
}
//</editor-fold>//GEN-END:|64-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Method: mainMenuAction ">//GEN-BEGIN:|64-action|0|64-preAction
/**
 * Performs an action assigned to the selected list element in the mainMenu component.
 */
public void mainMenuAction() {//GEN-END:|64-action|0|64-preAction
 // enter pre-action user code here
    String __selectedString = getMainMenu().getString(getMainMenu().getSelectedIndex());//GEN-BEGIN:|64-action|1|72-preAction
    if (__selectedString != null) {
        if (__selectedString.equals("Browse")) {//GEN-END:|64-action|1|72-preAction
 // write pre-action user code here
            switchDisplayable(null, getPimBrowser());//GEN-LINE:|64-action|2|72-postAction
 // write post-action user code here
        } else if (__selectedString.equals("Open")) {//GEN-LINE:|64-action|3|73-preAction
 // write pre-action user code here
            switchDisplayable(null, getFileBrowser());//GEN-LINE:|64-action|4|73-postAction
 // write post-action user code here
        } else if (__selectedString.equals("Export")) {//GEN-LINE:|64-action|5|74-preAction
 // write pre-action user code here
//GEN-LINE:|64-action|6|74-postAction
 // write post-action user code here
        } else if (__selectedString.equals("Help")) {//GEN-LINE:|64-action|7|75-preAction
 // write pre-action user code here
            switchDisplayable(null, getWelcome());//GEN-LINE:|64-action|8|75-postAction
 // write post-action user code here
        } else if (__selectedString.equals("Info")) {//GEN-LINE:|64-action|9|76-preAction
 // write pre-action user code here
            switchDisplayable(null, getFormDiag());//GEN-LINE:|64-action|10|76-postAction
 // write post-action user code here
        }//GEN-BEGIN:|64-action|11|64-postAction
    }//GEN-END:|64-action|11|64-postAction
 // enter post-action user code here
}//GEN-BEGIN:|64-action|12|
//</editor-fold>//GEN-END:|64-action|12|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: pimBrowser ">//GEN-BEGIN:|70-getter|0|70-preInit
/**
 * Returns an initiliazed instance of pimBrowser component.
 * @return the initialized component instance
 */
public PIMBrowser getPimBrowser() {
    if (pimBrowser == null) {//GEN-END:|70-getter|0|70-preInit
 // write pre-init user code here
        pimBrowser = new PIMBrowser(getDisplay(), PIM.CONTACT_LIST);//GEN-BEGIN:|70-getter|1|70-postInit
        pimBrowser.setTitle("pimBrowser");
        pimBrowser.addCommand(PIMBrowser.SELECT_PIM_ITEM);
        pimBrowser.setCommandListener(this);//GEN-END:|70-getter|1|70-postInit
 // write post-init user code here
    }//GEN-BEGIN:|70-getter|2|
    return pimBrowser;
}
//</editor-fold>//GEN-END:|70-getter|2|

    /**
     * Returns a display instance.
     * @return the display instance.
     */
    public Display getDisplay () {
        return Display.getDisplay(this);
    }

    /**
     * Exits MIDlet.
     */
    public void exitMIDlet() {
        switchDisplayable (null, null);
        destroyApp(true);
        notifyDestroyed();
    }

    /**
     * Called when MIDlet is started.
     * Checks whether the MIDlet have been already started and initialize/starts or resumes the MIDlet.
     */
    public void startApp() {
        if (midletPaused) {
            resumeMIDlet ();
        } else {
            initialize ();
            startMIDlet ();
        }
        midletPaused = false;
    }

    /**
     * Called when MIDlet is paused.
     */
    public void pauseApp() {
        midletPaused = true;
    }

    /**
     * Called to signal the MIDlet to terminate.
     * @param unconditional if true, then the MIDlet has to be unconditionally terminated and all resources has to be released.
     */
    public void destroyApp(boolean unconditional) {
    }

}
