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

    private boolean showDetails = false;
    
    private Ticker notification = null;
    
//<editor-fold defaultstate="collapsed" desc=" Generated Fields ">//GEN-BEGIN:|fields|0|
private Command exitCommand;
private Command okCommand;
private Command cancelCommand;
private Command itemCommand;
private Command okCommandDiag;
private Command exitCommand1;
private Command itemCommand1;
private Command backCommand;
private Command backCommand2;
private Command backCommand1;
private Command backCommand3;
private Command okCommand1;
private Command cancelCommand1;
private Command itemCommand2;
private Command backCommand4;
private Form welcome;
private StringItem stringItem;
private FileBrowser fileBrowser;
private Alert alert;
private Form formDiag;
private StringItem stringItem4;
private StringItem stringItem3;
private StringItem stringItem2;
private StringItem stringItem1;
private StringItem stringItem6;
private List mainMenu;
private Form vCard;
private StringItem stringItem5;
private List writableDirs;
private TextBox exportFilename;
private List vCardsFound;
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
 * Initializes the application.
 * It is called only once when the MIDlet is started. The method is called before the <code>startMIDlet</code> method.
 */
private void initialize () {//GEN-END:|0-initialize|0|0-preInitialize
        // write pre-initialize user code here
//GEN-LINE:|0-initialize|1|0-postInitialize
        // write post-initialize user code here
}//GEN-BEGIN:|0-initialize|2|
//</editor-fold>//GEN-END:|0-initialize|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Method: startMIDlet ">//GEN-BEGIN:|3-startMIDlet|0|3-preAction
/**
 * Performs an action assigned to the Mobile Device - MIDlet Started point.
 */
public void startMIDlet () {//GEN-END:|3-startMIDlet|0|3-preAction
        // write pre-action user code here
switchDisplayable (null, getMainMenu ());//GEN-LINE:|3-startMIDlet|1|3-postAction
        // write post-action user code here
}//GEN-BEGIN:|3-startMIDlet|2|
//</editor-fold>//GEN-END:|3-startMIDlet|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Method: resumeMIDlet ">//GEN-BEGIN:|4-resumeMIDlet|0|4-preAction
/**
 * Performs an action assigned to the Mobile Device - MIDlet Resumed point.
 */
public void resumeMIDlet () {//GEN-END:|4-resumeMIDlet|0|4-preAction
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
public void switchDisplayable (Alert alert, Displayable nextDisplayable) {//GEN-END:|5-switchDisplayable|0|5-preSwitch
        // write pre-switch user code here
Display display = getDisplay ();//GEN-BEGIN:|5-switchDisplayable|1|5-postSwitch
if (alert == null) {
display.setCurrent (nextDisplayable);
} else {
display.setCurrent (alert, nextDisplayable);
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
public void commandAction (Command command, Displayable displayable) {//GEN-END:|7-commandAction|0|7-preCommandAction
        // write pre-action user code here
if (displayable == exportFilename) {//GEN-BEGIN:|7-commandAction|1|110-preAction
if (command == cancelCommand1) {//GEN-END:|7-commandAction|1|110-preAction
                // write pre-action user code here
switchDisplayable (null, getMainMenu ());//GEN-LINE:|7-commandAction|2|110-postAction
                // write post-action user code here
} else if (command == okCommand1) {//GEN-LINE:|7-commandAction|3|112-preAction
                int numDir = writableDirs.getSelectedIndex();
                String message = "No directory selected";
                if ( numDir != -1 ) {
                    message = VCardExporter.exportContacts(writableDirs.getString(numDir)
                            +exportFilename.getString());
                }
switchDisplayable (null, getMainMenu ());//GEN-LINE:|7-commandAction|4|112-postAction
                showNotification(message);
}//GEN-BEGIN:|7-commandAction|5|24-preAction
} else if (displayable == fileBrowser) {
if (command == FileBrowser.SELECT_FILE_COMMAND) {//GEN-END:|7-commandAction|5|24-preAction
                getAlert().setTitle("Success?");
switchDisplayable (getAlert (), getMainMenu ());//GEN-LINE:|7-commandAction|6|24-postAction
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
} else if (command == cancelCommand) {//GEN-LINE:|7-commandAction|7|51-preAction
                // write pre-action user code here
switchDisplayable (null, getMainMenu ());//GEN-LINE:|7-commandAction|8|51-postAction
                // write post-action user code here
}//GEN-BEGIN:|7-commandAction|9|89-preAction
} else if (displayable == formDiag) {
if (command == backCommand1) {//GEN-END:|7-commandAction|9|89-preAction
                // write pre-action user code here
switchDisplayable (null, getMainMenu ());//GEN-LINE:|7-commandAction|10|89-postAction
                // write post-action user code here
} else if (command == itemCommand1) {//GEN-LINE:|7-commandAction|11|87-preAction
                // write pre-action user code here
//GEN-LINE:|7-commandAction|12|87-postAction
                toggleDetails();
}//GEN-BEGIN:|7-commandAction|13|66-preAction
} else if (displayable == mainMenu) {
if (command == List.SELECT_COMMAND) {//GEN-END:|7-commandAction|13|66-preAction
 // write pre-action user code here
mainMenuAction ();//GEN-LINE:|7-commandAction|14|66-postAction
 // write post-action user code here
} else if (command == exitCommand1) {//GEN-LINE:|7-commandAction|15|69-preAction
 // write pre-action user code here
exitMIDlet ();//GEN-LINE:|7-commandAction|16|69-postAction
 // write post-action user code here
}//GEN-BEGIN:|7-commandAction|17|93-preAction
} else if (displayable == vCard) {
if (command == backCommand2) {//GEN-END:|7-commandAction|17|93-preAction
                // write pre-action user code here
switchDisplayable (null, getMainMenu ());//GEN-LINE:|7-commandAction|18|93-postAction
                // write post-action user code here
}//GEN-BEGIN:|7-commandAction|19|116-preAction
} else if (displayable == vCardsFound) {
if (command == List.SELECT_COMMAND) {//GEN-END:|7-commandAction|19|116-preAction
 // write pre-action user code here
vCardsFoundAction ();//GEN-LINE:|7-commandAction|20|116-postAction
 // write post-action user code here
} else if (command == backCommand4) {//GEN-LINE:|7-commandAction|21|119-preAction
 // write pre-action user code here
switchDisplayable (null, getMainMenu ());//GEN-LINE:|7-commandAction|22|119-postAction
 showNotification(null);
}//GEN-BEGIN:|7-commandAction|23|83-preAction
} else if (displayable == welcome) {
if (command == backCommand) {//GEN-END:|7-commandAction|23|83-preAction
 // write pre-action user code here
switchDisplayable (null, getMainMenu ());//GEN-LINE:|7-commandAction|24|83-postAction
 // write post-action user code here
}//GEN-BEGIN:|7-commandAction|25|100-preAction
} else if (displayable == writableDirs) {
if (command == List.SELECT_COMMAND) {//GEN-END:|7-commandAction|25|100-preAction
                // write pre-action user code here
writableDirsAction ();//GEN-LINE:|7-commandAction|26|100-postAction
                // write post-action user code here
} else if (command == backCommand3) {//GEN-LINE:|7-commandAction|27|103-preAction
                // write pre-action user code here
switchDisplayable (null, getMainMenu ());//GEN-LINE:|7-commandAction|28|103-postAction
                // write post-action user code here
} else if (command == itemCommand2) {//GEN-LINE:|7-commandAction|29|107-preAction
                // write pre-action user code here
switchDisplayable (null, getExportFilename ());//GEN-LINE:|7-commandAction|30|107-postAction
                // write post-action user code here
}//GEN-BEGIN:|7-commandAction|31|7-postCommandAction
}//GEN-END:|7-commandAction|31|7-postCommandAction
        // write post-action user code here
}//GEN-BEGIN:|7-commandAction|32|
//</editor-fold>//GEN-END:|7-commandAction|32|


//<editor-fold defaultstate="collapsed" desc=" Generated Getter: exitCommand ">//GEN-BEGIN:|18-getter|0|18-preInit
/**
 * Returns an initiliazed instance of exitCommand component.
 * @return the initialized component instance
 */
public Command getExitCommand () {
if (exitCommand == null) {//GEN-END:|18-getter|0|18-preInit
            // write pre-init user code here
exitCommand = new Command ("Exit", Command.EXIT, 0);//GEN-LINE:|18-getter|1|18-postInit
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
public Form getWelcome () {
if (welcome == null) {//GEN-END:|14-getter|0|14-preInit
            // write pre-init user code here
welcome = new Form ("Welcome", new Item[] { getStringItem () });//GEN-BEGIN:|14-getter|1|14-postInit
welcome.addCommand (getBackCommand ());
welcome.setCommandListener (this);//GEN-END:|14-getter|1|14-postInit
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
public StringItem getStringItem () {
if (stringItem == null) {//GEN-END:|16-getter|0|16-preInit
            // write pre-init user code here
stringItem = new StringItem ("Menu options", "\nInfo Diag \n- displays supported fields\n\nBrowse\n- (lame) runs NB\'s contact browser\n\nExport\n- (placeholder) displays first few contacts\' vCard\n\nOpen\n- (unstable) imports a chosen vCard file\n");//GEN-LINE:|16-getter|1|16-postInit
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
public Command getOkCommand () {
if (okCommand == null) {//GEN-END:|28-getter|0|28-preInit
            // write pre-init user code here
okCommand = new Command ("Ok", Command.OK, 0);//GEN-LINE:|28-getter|1|28-postInit
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
public FileBrowser getFileBrowser () {
if (fileBrowser == null) {//GEN-END:|22-getter|0|22-preInit
            // write pre-init user code here
fileBrowser = new FileBrowser (getDisplay ());//GEN-BEGIN:|22-getter|1|22-postInit
fileBrowser.setTitle ("fileBrowser");
fileBrowser.setCommandListener (this);
fileBrowser.addCommand (FileBrowser.SELECT_FILE_COMMAND);
fileBrowser.addCommand (getCancelCommand ());//GEN-END:|22-getter|1|22-postInit
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
public Alert getAlert () {
if (alert == null) {//GEN-END:|48-getter|0|48-preInit
            // write pre-init user code here
alert = new Alert ("Read line:", "Please wait - processing", null, null);//GEN-BEGIN:|48-getter|1|48-postInit
alert.setTimeout (Alert.FOREVER);//GEN-END:|48-getter|1|48-postInit
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
public Command getCancelCommand () {
if (cancelCommand == null) {//GEN-END:|50-getter|0|50-preInit
            // write pre-init user code here
cancelCommand = new Command ("Cancel", Command.CANCEL, 0);//GEN-LINE:|50-getter|1|50-postInit
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
public Command getItemCommand () {
if (itemCommand == null) {//GEN-END:|53-getter|0|53-preInit
            // write pre-init user code here
itemCommand = new Command ("Info", Command.ITEM, 0);//GEN-LINE:|53-getter|1|53-postInit
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
public Command getOkCommandDiag () {
if (okCommandDiag == null) {//GEN-END:|57-getter|0|57-preInit
            // write pre-init user code here
okCommandDiag = new Command ("Ok", Command.OK, 0);//GEN-LINE:|57-getter|1|57-postInit
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
public Form getFormDiag () {
if (formDiag == null) {//GEN-END:|55-getter|0|55-preInit
            // write pre-init user code here
formDiag = new Form ("PIM API diags", new Item[] { getStringItem6 (), getStringItem1 (), getStringItem4 (), getStringItem3 (), getStringItem2 () });//GEN-BEGIN:|55-getter|1|55-postInit
formDiag.addCommand (getItemCommand1 ());
formDiag.addCommand (getBackCommand1 ());
formDiag.setCommandListener (this);//GEN-END:|55-getter|1|55-postInit
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
public StringItem getStringItem1 () {
if (stringItem1 == null) {//GEN-END:|60-getter|0|60-preInit
            // write pre-init user code here
stringItem1 = new StringItem ("Contact List Formats", PimDiag.getSerialFormats());//GEN-LINE:|60-getter|1|60-postInit
            // write post-init user code here
}//GEN-BEGIN:|60-getter|2|
return stringItem1;
}
//</editor-fold>//GEN-END:|60-getter|2|



//<editor-fold defaultstate="collapsed" desc=" Generated Getter: stringItem3 ">//GEN-BEGIN:|62-getter|0|62-preInit
/**
 * Returns an initiliazed instance of stringItem3 component.
 * @return the initialized component instance
 */
public StringItem getStringItem3 () {
if (stringItem3 == null) {//GEN-END:|62-getter|0|62-preInit
            // write pre-init user code here
stringItem3 = new StringItem ("Contact categories", PimDiag.getCategories());//GEN-LINE:|62-getter|1|62-postInit
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
public StringItem getStringItem4 () {
if (stringItem4 == null) {//GEN-END:|63-getter|0|63-preInit
 // write pre-init user code here
stringItem4 = new StringItem ("Contact Lists", PimDiag.getContactLists());//GEN-LINE:|63-getter|1|63-postInit
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
public Command getExitCommand1 () {
if (exitCommand1 == null) {//GEN-END:|68-getter|0|68-preInit
 // write pre-init user code here
exitCommand1 = new Command ("Exit", Command.EXIT, 0);//GEN-LINE:|68-getter|1|68-postInit
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
public Command getBackCommand () {
if (backCommand == null) {//GEN-END:|82-getter|0|82-preInit
 // write pre-init user code here
backCommand = new Command ("Back", Command.BACK, 0);//GEN-LINE:|82-getter|1|82-postInit
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
public List getMainMenu () {
if (mainMenu == null) {//GEN-END:|64-getter|0|64-preInit
 // write pre-init user code here
mainMenu = new List ("Menu", Choice.IMPLICIT);//GEN-BEGIN:|64-getter|1|64-postInit
mainMenu.append ("Diag Info", null);
mainMenu.append ("Browse", null);
mainMenu.append ("Open", null);
mainMenu.append ("Export", null);
mainMenu.append ("Help", null);
mainMenu.addCommand (getExitCommand1 ());
mainMenu.setCommandListener (this);
mainMenu.setFitPolicy (Choice.TEXT_WRAP_DEFAULT);
mainMenu.setSelectedFlags (new boolean[] { false, false, false, false, false });//GEN-END:|64-getter|1|64-postInit
 // write post-init user code here
}//GEN-BEGIN:|64-getter|2|
return mainMenu;
}
//</editor-fold>//GEN-END:|64-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Method: mainMenuAction ">//GEN-BEGIN:|64-action|0|64-preAction
/**
 * Performs an action assigned to the selected list element in the mainMenu component.
 */
public void mainMenuAction () {//GEN-END:|64-action|0|64-preAction
 // enter pre-action user code here
String __selectedString = getMainMenu ().getString (getMainMenu ().getSelectedIndex ());//GEN-BEGIN:|64-action|1|76-preAction
if (__selectedString != null) {
if (__selectedString.equals ("Diag Info")) {//GEN-END:|64-action|1|76-preAction
 // write pre-action user code here
switchDisplayable (null, getFormDiag ());//GEN-LINE:|64-action|2|76-postAction
 // write post-action user code here
} else if (__selectedString.equals ("Browse")) {//GEN-LINE:|64-action|3|72-preAction
 // write pre-action user code here
switchDisplayable (null, getVCard ());//GEN-LINE:|64-action|4|72-postAction
 // write post-action user code here
} else if (__selectedString.equals ("Open")) {//GEN-LINE:|64-action|5|73-preAction
 // write pre-action user code here
switchDisplayable (null, getVCardsFound ());//GEN-LINE:|64-action|6|73-postAction
 loadVcards();
} else if (__selectedString.equals ("Export")) {//GEN-LINE:|64-action|7|74-preAction
 // write pre-action user code here
switchDisplayable (null, getWritableDirs ());//GEN-LINE:|64-action|8|74-postAction
 // write post-action user code here
} else if (__selectedString.equals ("Help")) {//GEN-LINE:|64-action|9|75-preAction
 // write pre-action user code here
switchDisplayable (null, getWelcome ());//GEN-LINE:|64-action|10|75-postAction
 // write post-action user code here
}//GEN-BEGIN:|64-action|11|64-postAction
}//GEN-END:|64-action|11|64-postAction
 // enter post-action user code here
}//GEN-BEGIN:|64-action|12|
//</editor-fold>//GEN-END:|64-action|12|



//<editor-fold defaultstate="collapsed" desc=" Generated Getter: stringItem2 ">//GEN-BEGIN:|61-getter|0|61-preInit
/**
 * Returns an initiliazed instance of stringItem2 component.
 * @return the initialized component instance
 */
public StringItem getStringItem2 () {
if (stringItem2 == null) {//GEN-END:|61-getter|0|61-preInit
            // write pre-init user code here
stringItem2 = new StringItem ("Supported fields", PimDiag.getSupportedFields(false));//GEN-LINE:|61-getter|1|61-postInit
            // write post-init user code here
}//GEN-BEGIN:|61-getter|2|
return stringItem2;
}
//</editor-fold>//GEN-END:|61-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: itemCommand1 ">//GEN-BEGIN:|86-getter|0|86-preInit
/**
 * Returns an initiliazed instance of itemCommand1 component.
 * @return the initialized component instance
 */
public Command getItemCommand1 () {
if (itemCommand1 == null) {//GEN-END:|86-getter|0|86-preInit
        // write pre-init user code here
itemCommand1 = new Command ("Details", Command.ITEM, 0);//GEN-LINE:|86-getter|1|86-postInit
        // write post-init user code here
}//GEN-BEGIN:|86-getter|2|
return itemCommand1;
}
//</editor-fold>//GEN-END:|86-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: backCommand1 ">//GEN-BEGIN:|88-getter|0|88-preInit
/**
 * Returns an initiliazed instance of backCommand1 component.
 * @return the initialized component instance
 */
public Command getBackCommand1 () {
if (backCommand1 == null) {//GEN-END:|88-getter|0|88-preInit
        // write pre-init user code here
backCommand1 = new Command ("Back", Command.BACK, 0);//GEN-LINE:|88-getter|1|88-postInit
        // write post-init user code here
}//GEN-BEGIN:|88-getter|2|
return backCommand1;
}
//</editor-fold>//GEN-END:|88-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: backCommand2 ">//GEN-BEGIN:|92-getter|0|92-preInit
/**
 * Returns an initiliazed instance of backCommand2 component.
 * @return the initialized component instance
 */
public Command getBackCommand2 () {
if (backCommand2 == null) {//GEN-END:|92-getter|0|92-preInit
        // write pre-init user code here
backCommand2 = new Command ("Back", Command.BACK, 0);//GEN-LINE:|92-getter|1|92-postInit
        // write post-init user code here
}//GEN-BEGIN:|92-getter|2|
return backCommand2;
}
//</editor-fold>//GEN-END:|92-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: vCard ">//GEN-BEGIN:|91-getter|0|91-preInit
/**
 * Returns an initiliazed instance of vCard component.
 * @return the initialized component instance
 */
public Form getVCard () {
if (vCard == null) {//GEN-END:|91-getter|0|91-preInit
        // write pre-init user code here
vCard = new Form ("Exported", new Item[] { getStringItem5 () });//GEN-BEGIN:|91-getter|1|91-postInit
vCard.addCommand (getBackCommand2 ());
vCard.setCommandListener (this);//GEN-END:|91-getter|1|91-postInit
        // write post-init user code here
}//GEN-BEGIN:|91-getter|2|
return vCard;
}
//</editor-fold>//GEN-END:|91-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: stringItem5 ">//GEN-BEGIN:|95-getter|0|95-preInit
/**
 * Returns an initiliazed instance of stringItem5 component.
 * @return the initialized component instance
 */
public StringItem getStringItem5 () {
if (stringItem5 == null) {//GEN-END:|95-getter|0|95-preInit
        // write pre-init user code here
stringItem5 = new StringItem ("vCard", VCardExporter.dumpSome(5));//GEN-LINE:|95-getter|1|95-postInit
        // write post-init user code here
}//GEN-BEGIN:|95-getter|2|
return stringItem5;
}
//</editor-fold>//GEN-END:|95-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: stringItem6 ">//GEN-BEGIN:|97-getter|0|97-preInit
/**
 * Returns an initiliazed instance of stringItem6 component.
 * @return the initialized component instance
 */
public StringItem getStringItem6 () {
if (stringItem6 == null) {//GEN-END:|97-getter|0|97-preInit
 // write pre-init user code here
stringItem6 = new StringItem ("Writable directories", "\n"+org.apache.commons.lang.StringUtils.join(VCardExporter.findWritableDirectories(), "\n"));//GEN-LINE:|97-getter|1|97-postInit
 // write post-init user code here
}//GEN-BEGIN:|97-getter|2|
return stringItem6;
}
//</editor-fold>//GEN-END:|97-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: backCommand3 ">//GEN-BEGIN:|102-getter|0|102-preInit
/**
 * Returns an initiliazed instance of backCommand3 component.
 * @return the initialized component instance
 */
public Command getBackCommand3 () {
if (backCommand3 == null) {//GEN-END:|102-getter|0|102-preInit
            // write pre-init user code here
backCommand3 = new Command ("Back", Command.BACK, 0);//GEN-LINE:|102-getter|1|102-postInit
            // write post-init user code here
}//GEN-BEGIN:|102-getter|2|
return backCommand3;
}
//</editor-fold>//GEN-END:|102-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: writableDirs ">//GEN-BEGIN:|99-getter|0|99-preInit
/**
 * Returns an initiliazed instance of writableDirs component.
 * @return the initialized component instance
 */
public List getWritableDirs () {
if (writableDirs == null) {//GEN-END:|99-getter|0|99-preInit
            // write pre-init user code here
writableDirs = new List ("Writable Paths", Choice.IMPLICIT);//GEN-BEGIN:|99-getter|1|99-postInit
writableDirs.addCommand (getBackCommand3 ());
writableDirs.addCommand (getItemCommand2 ());
writableDirs.setCommandListener (this);
writableDirs.setFitPolicy (Choice.TEXT_WRAP_DEFAULT);//GEN-END:|99-getter|1|99-postInit
            String[] dirs = VCardExporter.findWritableDirectories();
            for(int i=0; i<dirs.length; ++i)
                writableDirs.append(dirs[i], null);
}//GEN-BEGIN:|99-getter|2|
return writableDirs;
}
//</editor-fold>//GEN-END:|99-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Method: writableDirsAction ">//GEN-BEGIN:|99-action|0|99-preAction
/**
 * Performs an action assigned to the selected list element in the writableDirs component.
 */
public void writableDirsAction () {//GEN-END:|99-action|0|99-preAction
        // enter pre-action user code here
String __selectedString = getWritableDirs ().getString (getWritableDirs ().getSelectedIndex ());//GEN-LINE:|99-action|1|99-postAction
        // enter post-action user code here
}//GEN-BEGIN:|99-action|2|
//</editor-fold>//GEN-END:|99-action|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: itemCommand2 ">//GEN-BEGIN:|106-getter|0|106-preInit
/**
 * Returns an initiliazed instance of itemCommand2 component.
 * @return the initialized component instance
 */
public Command getItemCommand2 () {
if (itemCommand2 == null) {//GEN-END:|106-getter|0|106-preInit
            // write pre-init user code here
itemCommand2 = new Command ("Select", Command.ITEM, 0);//GEN-LINE:|106-getter|1|106-postInit
            // write post-init user code here
}//GEN-BEGIN:|106-getter|2|
return itemCommand2;
}
//</editor-fold>//GEN-END:|106-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: cancelCommand1 ">//GEN-BEGIN:|109-getter|0|109-preInit
/**
 * Returns an initiliazed instance of cancelCommand1 component.
 * @return the initialized component instance
 */
public Command getCancelCommand1 () {
if (cancelCommand1 == null) {//GEN-END:|109-getter|0|109-preInit
            // write pre-init user code here
cancelCommand1 = new Command ("Cancel", Command.CANCEL, 0);//GEN-LINE:|109-getter|1|109-postInit
            // write post-init user code here
}//GEN-BEGIN:|109-getter|2|
return cancelCommand1;
}
//</editor-fold>//GEN-END:|109-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: okCommand1 ">//GEN-BEGIN:|111-getter|0|111-preInit
/**
 * Returns an initiliazed instance of okCommand1 component.
 * @return the initialized component instance
 */
public Command getOkCommand1 () {
if (okCommand1 == null) {//GEN-END:|111-getter|0|111-preInit
            // write pre-init user code here
okCommand1 = new Command ("Ok", Command.OK, 0);//GEN-LINE:|111-getter|1|111-postInit
            // write post-init user code here
}//GEN-BEGIN:|111-getter|2|
return okCommand1;
}
//</editor-fold>//GEN-END:|111-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: exportFilename ">//GEN-BEGIN:|105-getter|0|105-preInit
/**
 * Returns an initiliazed instance of exportFilename component.
 * @return the initialized component instance
 */
public TextBox getExportFilename () {
if (exportFilename == null) {//GEN-END:|105-getter|0|105-preInit
            // write pre-init user code here
exportFilename = new TextBox ("textBox", VCardExporter.getFilenameSuggestion(), 100, TextField.ANY);//GEN-BEGIN:|105-getter|1|105-postInit
exportFilename.addCommand (getCancelCommand1 ());
exportFilename.addCommand (getOkCommand1 ());
exportFilename.setCommandListener (this);//GEN-END:|105-getter|1|105-postInit
            // write post-init user code here
}//GEN-BEGIN:|105-getter|2|
return exportFilename;
}
//</editor-fold>//GEN-END:|105-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: backCommand4 ">//GEN-BEGIN:|118-getter|0|118-preInit
/**
 * Returns an initiliazed instance of backCommand4 component.
 * @return the initialized component instance
 */
public Command getBackCommand4 () {
if (backCommand4 == null) {//GEN-END:|118-getter|0|118-preInit
 // write pre-init user code here
backCommand4 = new Command ("Back", Command.BACK, 0);//GEN-LINE:|118-getter|1|118-postInit
 // write post-init user code here
}//GEN-BEGIN:|118-getter|2|
return backCommand4;
}
//</editor-fold>//GEN-END:|118-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Getter: vCardsFound ">//GEN-BEGIN:|115-getter|0|115-preInit
/**
 * Returns an initiliazed instance of vCardsFound component.
 * @return the initialized component instance
 */
public List getVCardsFound () {
if (vCardsFound == null) {//GEN-END:|115-getter|0|115-preInit
 // write pre-init user code here
vCardsFound = new List ("Available vCards", Choice.IMPLICIT);//GEN-BEGIN:|115-getter|1|115-postInit
vCardsFound.addCommand (getBackCommand4 ());
vCardsFound.setCommandListener (this);//GEN-END:|115-getter|1|115-postInit
 // vCards load on transition
}//GEN-BEGIN:|115-getter|2|
return vCardsFound;
}
//</editor-fold>//GEN-END:|115-getter|2|

//<editor-fold defaultstate="collapsed" desc=" Generated Method: vCardsFoundAction ">//GEN-BEGIN:|115-action|0|115-preAction
/**
 * Performs an action assigned to the selected list element in the vCardsFound component.
 */
public void vCardsFoundAction () {//GEN-END:|115-action|0|115-preAction
 // enter pre-action user code here
String __selectedString = getVCardsFound ().getString (getVCardsFound ().getSelectedIndex ());//GEN-LINE:|115-action|1|115-postAction
 // enter post-action user code here
}//GEN-BEGIN:|115-action|2|
//</editor-fold>//GEN-END:|115-action|2|

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

    private void toggleDetails()
    {
        showDetails = !showDetails;
        getStringItem2().setText(PimDiag.getSupportedFields(showDetails));
    }
    
    private void loadVcards()
    {
        showNotification("Scanning filesystems for vCards...");
        vCardsFound.deleteAll();
        String[] vCards = VCardExporter.findVCards();
        for(int i=0; i<vCards.length; ++i)
            vCardsFound.append(vCards[i], null);
        if ( vCards.length == 0 )
            showNotification("No vCards found in filesystems.");
        else
            showNotification("Some: "+vCards.length+", vCards found.");       
    }
    
    private void showNotification(String msg)
    {
        if ( msg != null )
        {
            if ( notification == null )
                notification = new Ticker(msg);
            else
                notification.setString(msg);
            getDisplay().getCurrent().setTicker(notification);
        }
        else 
        {
            getDisplay().getCurrent().setTicker(null);
        }
    }

}
