/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package com.googlecode.meats;

import com.sun.midp.io.Properties;
import javax.microedition.midlet.*;
import javax.microedition.lcdui.*;
import org.netbeans.microedition.lcdui.SimpleTableModel;
import org.netbeans.microedition.lcdui.TableItem;

/**
 * @author olaija
 */
public class CellDiag extends MIDlet implements CommandListener {

    /**
     * Make a string with bytes and kilobytes
     * @param bytes number to use in the string
     * @return a string of the form N B, N/1024.0 KB
     */
    private static String formatBytes(long bytes) {
        return "" + bytes/1024 + "." + bytes*10/1024%10 + " KB";
    }

    /**
     * Format a percentage string from two longs
     * @param part the part which is to determine
     * @param total the whole (100%)
     * @return a string of the format "%.2f %%"
     */
    private static String percentage(long part, long total) {
        return "\n" + part * 100 / total + "."
                + part * 1000 / total % 10
                + part * 10000 / total % 10 + " %";
    }

    private void refreshMemory() {
        long free = Runtime.getRuntime().freeMemory();
        getFreeStringItem().setText(formatBytes(free));
        getPercentFreeStringItem().setText(percentage(free, total));
        getUsedStringItem().setText(formatBytes(total-free));
    }

    private boolean midletPaused = false;

    private long total;

    //<editor-fold defaultstate="collapsed" desc=" Generated Fields ">//GEN-BEGIN:|fields|0|
    private Command exitCommand;
    private Command exitCommand1;
    private Command itemCommand;
    private Command backCommand;
    private Command itemCommand1;
    private Command exitCommand2;
    private Command backCommand1;
    private Form ram;
    private StringItem freeStringItem;
    private StringItem usedStringItem;
    private StringItem stringItem1;
    private StringItem percentFreeStringItem;
    private List list;
    private Alert alert;
    private Form features;
    private TableItem tableItem;
    private StringItem stringItem4;
    private Alert pimAlert;
    private SimpleTableModel tableModel1;
    //</editor-fold>//GEN-END:|fields|0|

    /**
     * The HelloMIDlet constructor.
     */
    public CellDiag() {
        total = Runtime.getRuntime().totalMemory();
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
        switchDisplayable(null, getList());//GEN-LINE:|3-startMIDlet|1|3-postAction
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
        if (displayable == features) {//GEN-BEGIN:|7-commandAction|1|54-preAction
            if (command == backCommand1) {//GEN-END:|7-commandAction|1|54-preAction
                // write pre-action user code here
                switchDisplayable(null, getList());//GEN-LINE:|7-commandAction|2|54-postAction
                // write post-action user code here
            }//GEN-BEGIN:|7-commandAction|3|27-preAction
        } else if (displayable == list) {
            if (command == List.SELECT_COMMAND) {//GEN-END:|7-commandAction|3|27-preAction
                // write pre-action user code here
                listAction();//GEN-LINE:|7-commandAction|4|27-postAction
                // write post-action user code here
            } else if (command == exitCommand1) {//GEN-LINE:|7-commandAction|5|30-preAction
                // write pre-action user code here
                exitMIDlet();//GEN-LINE:|7-commandAction|6|30-postAction
                // write post-action user code here
            }//GEN-BEGIN:|7-commandAction|7|35-preAction
        } else if (displayable == ram) {
            if (command == backCommand) {//GEN-END:|7-commandAction|7|35-preAction
                // write pre-action user code here
                switchDisplayable(null, getList());//GEN-LINE:|7-commandAction|8|35-postAction
                // write post-action user code here
            }//GEN-BEGIN:|7-commandAction|9|7-postCommandAction
        }//GEN-END:|7-commandAction|9|7-postCommandAction
        // write post-action user code here
    }//GEN-BEGIN:|7-commandAction|10|
    //</editor-fold>//GEN-END:|7-commandAction|10|




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

    //<editor-fold defaultstate="collapsed" desc=" Generated Getter: ram ">//GEN-BEGIN:|14-getter|0|14-preInit
    /**
     * Returns an initiliazed instance of ram component.
     * @return the initialized component instance
     */
    public Form getRam() {
        if (ram == null) {//GEN-END:|14-getter|0|14-preInit
            // write pre-init user code here
            ram = new Form("RAM available to Java", new Item[] { getFreeStringItem(), getUsedStringItem(), getStringItem1(), getPercentFreeStringItem() });//GEN-BEGIN:|14-getter|1|14-postInit
            ram.addCommand(getBackCommand());
            ram.setCommandListener(this);//GEN-END:|14-getter|1|14-postInit
            // write post-init user code here
        }//GEN-BEGIN:|14-getter|2|
        return ram;
    }
    //</editor-fold>//GEN-END:|14-getter|2|
    //</editor-fold>

    //<editor-fold defaultstate="collapsed" desc=" Generated Getter: freeStringItem ">//GEN-BEGIN:|16-getter|0|16-preInit
    /**
     * Returns an initiliazed instance of freeStringItem component.
     * @return the initialized component instance
     */
    public StringItem getFreeStringItem() {
        if (freeStringItem == null) {//GEN-END:|16-getter|0|16-preInit
            // write pre-init user code here
            freeStringItem = new StringItem("Free Memory:", formatBytes(Runtime.getRuntime().freeMemory()));//GEN-BEGIN:|16-getter|1|16-postInit
            freeStringItem.setLayout(ImageItem.LAYOUT_DEFAULT | ImageItem.LAYOUT_NEWLINE_BEFORE);//GEN-END:|16-getter|1|16-postInit
            // write post-init user code here
        }//GEN-BEGIN:|16-getter|2|
        return freeStringItem;
    }
    //</editor-fold>//GEN-END:|16-getter|2|

    //<editor-fold defaultstate="collapsed" desc=" Generated Getter: stringItem1 ">//GEN-BEGIN:|22-getter|0|22-preInit
    /**
     * Returns an initiliazed instance of stringItem1 component.
     * @return the initialized component instance
     */
    public StringItem getStringItem1() {
        if (stringItem1 == null) {//GEN-END:|22-getter|0|22-preInit
            // write pre-init user code here
            stringItem1 = new StringItem("Total Memory:", formatBytes(Runtime.getRuntime().totalMemory()));//GEN-LINE:|22-getter|1|22-postInit
            // write post-init user code here
        }//GEN-BEGIN:|22-getter|2|
        return stringItem1;
    }
    //</editor-fold>//GEN-END:|22-getter|2|
    //</editor-fold>

    //<editor-fold defaultstate="collapsed" desc=" Generated Getter: usedStringItem ">//GEN-BEGIN:|23-getter|0|23-preInit
    /**
     * Returns an initiliazed instance of usedStringItem component.
     * @return the initialized component instance
     */
    public StringItem getUsedStringItem() {
        if (usedStringItem == null) {//GEN-END:|23-getter|0|23-preInit
            // write pre-init user code here
            usedStringItem = new StringItem("Used Memory:", formatBytes(//GEN-BEGIN:|23-getter|1|23-postInit
                    Runtime.getRuntime().totalMemory()
                    - Runtime.getRuntime().freeMemory()
                    ));//GEN-END:|23-getter|1|23-postInit
            // write post-init user code here
        }//GEN-BEGIN:|23-getter|2|
        return usedStringItem;
    }
    //</editor-fold>//GEN-END:|23-getter|2|
    //</editor-fold>

    //<editor-fold defaultstate="collapsed" desc=" Generated Getter: percentFreeStringItem ">//GEN-BEGIN:|24-getter|0|24-preInit
    /**
     * Returns an initiliazed instance of percentFreeStringItem component.
     * @return the initialized component instance
     */
    public StringItem getPercentFreeStringItem() {
        if (percentFreeStringItem == null) {//GEN-END:|24-getter|0|24-preInit
            // write pre-init user code here
            percentFreeStringItem = new StringItem("Percent Free:", percentage(Runtime.getRuntime().freeMemory(),//GEN-BEGIN:|24-getter|1|24-postInit
                    Runtime.getRuntime().totalMemory()));//GEN-END:|24-getter|1|24-postInit
            // write post-init user code here
        }//GEN-BEGIN:|24-getter|2|
        return percentFreeStringItem;
    }
    //</editor-fold>//GEN-END:|24-getter|2|

    //<editor-fold defaultstate="collapsed" desc=" Generated Getter: exitCommand1 ">//GEN-BEGIN:|29-getter|0|29-preInit
    /**
     * Returns an initiliazed instance of exitCommand1 component.
     * @return the initialized component instance
     */
    public Command getExitCommand1() {
        if (exitCommand1 == null) {//GEN-END:|29-getter|0|29-preInit
            // write pre-init user code here
            exitCommand1 = new Command("Exit", Command.EXIT, 0);//GEN-LINE:|29-getter|1|29-postInit
            // write post-init user code here
        }//GEN-BEGIN:|29-getter|2|
        return exitCommand1;
    }
    //</editor-fold>//GEN-END:|29-getter|2|

    //<editor-fold defaultstate="collapsed" desc=" Generated Getter: itemCommand ">//GEN-BEGIN:|31-getter|0|31-preInit
    /**
     * Returns an initiliazed instance of itemCommand component.
     * @return the initialized component instance
     */
    public Command getItemCommand() {
        if (itemCommand == null) {//GEN-END:|31-getter|0|31-preInit
            // write pre-init user code here
            itemCommand = new Command("Item", Command.ITEM, 0);//GEN-LINE:|31-getter|1|31-postInit
            // write post-init user code here
        }//GEN-BEGIN:|31-getter|2|
        return itemCommand;
    }
    //</editor-fold>//GEN-END:|31-getter|2|

    //<editor-fold defaultstate="collapsed" desc=" Generated Getter: list ">//GEN-BEGIN:|25-getter|0|25-preInit
    /**
     * Returns an initiliazed instance of list component.
     * @return the initialized component instance
     */
    public List getList() {
        if (list == null) {//GEN-END:|25-getter|0|25-preInit
            // write pre-init user code here
            list = new List("Welcome to CellDiag", Choice.IMPLICIT);//GEN-BEGIN:|25-getter|1|25-postInit
            list.append("Memory (RAM)", null);
            list.append("Features (JSRs)", null);
            list.append("Help", null);
            list.append("About", null);
            list.append("Exit", null);
            list.addCommand(getExitCommand1());
            list.setCommandListener(this);
            list.setSelectedFlags(new boolean[] { false, false, false, false, false });//GEN-END:|25-getter|1|25-postInit
            // write post-init user code here
        }//GEN-BEGIN:|25-getter|2|
        return list;
    }
    //</editor-fold>//GEN-END:|25-getter|2|

    //<editor-fold defaultstate="collapsed" desc=" Generated Method: listAction ">//GEN-BEGIN:|25-action|0|25-preAction
    /**
     * Performs an action assigned to the selected list element in the list component.
     */
    public void listAction() {//GEN-END:|25-action|0|25-preAction
        // enter pre-action user code here
        String __selectedString = getList().getString(getList().getSelectedIndex());//GEN-BEGIN:|25-action|1|37-preAction
        if (__selectedString != null) {
            if (__selectedString.equals("Memory (RAM)")) {//GEN-END:|25-action|1|37-preAction
                // write pre-action user code here
                switchDisplayable(null, getRam());//GEN-LINE:|25-action|2|37-postAction
                refreshMemory();
            } else if (__selectedString.equals("Features (JSRs)")) {//GEN-LINE:|25-action|3|49-preAction
                // write pre-action user code here
                switchDisplayable(null, getFeatures());//GEN-LINE:|25-action|4|49-postAction
                // write post-action user code here
            } else if (__selectedString.equals("Help")) {//GEN-LINE:|25-action|5|42-preAction
                // write pre-action user code here
                switchDisplayable(getPimAlert(), getList());//GEN-LINE:|25-action|6|42-postAction
                // write post-action user code here
            } else if (__selectedString.equals("About")) {//GEN-LINE:|25-action|7|44-preAction
                // write pre-action user code here
                switchDisplayable(getAlert(), getList());//GEN-LINE:|25-action|8|44-postAction
                // write post-action user code here
            } else if (__selectedString.equals("Exit")) {//GEN-LINE:|25-action|9|43-preAction
                // write pre-action user code here
                exitMIDlet();//GEN-LINE:|25-action|10|43-postAction
                // write post-action user code here
            }//GEN-BEGIN:|25-action|11|25-postAction
        }//GEN-END:|25-action|11|25-postAction
        // enter post-action user code here
    }//GEN-BEGIN:|25-action|12|
    //</editor-fold>//GEN-END:|25-action|12|

    //<editor-fold defaultstate="collapsed" desc=" Generated Getter: backCommand ">//GEN-BEGIN:|34-getter|0|34-preInit
    /**
     * Returns an initiliazed instance of backCommand component.
     * @return the initialized component instance
     */
    public Command getBackCommand() {
        if (backCommand == null) {//GEN-END:|34-getter|0|34-preInit
            // write pre-init user code here
            backCommand = new Command("Back", Command.BACK, 0);//GEN-LINE:|34-getter|1|34-postInit
            // write post-init user code here
        }//GEN-BEGIN:|34-getter|2|
        return backCommand;
    }
    //</editor-fold>//GEN-END:|34-getter|2|

    //<editor-fold defaultstate="collapsed" desc=" Generated Getter: itemCommand1 ">//GEN-BEGIN:|39-getter|0|39-preInit
    /**
     * Returns an initiliazed instance of itemCommand1 component.
     * @return the initialized component instance
     */
    public Command getItemCommand1() {
        if (itemCommand1 == null) {//GEN-END:|39-getter|0|39-preInit
            // write pre-init user code here
            itemCommand1 = new Command("Choose", Command.ITEM, 0);//GEN-LINE:|39-getter|1|39-postInit
            // write post-init user code here
        }//GEN-BEGIN:|39-getter|2|
        return itemCommand1;
    }
    //</editor-fold>//GEN-END:|39-getter|2|

    //<editor-fold defaultstate="collapsed" desc=" Generated Getter: alert ">//GEN-BEGIN:|46-getter|0|46-preInit
    /**
     * Returns an initiliazed instance of alert component.
     * @return the initialized component instance
     */
    public Alert getAlert() {
        if (alert == null) {//GEN-END:|46-getter|0|46-preInit
            // write pre-init user code here
            alert = new Alert("About CellDiag", "CellDiag\nJava Mobile Phone info and benchmark application.\n\nAuthor: Tomasz Gandor <tomasz.gandor@gmail.com>\n", null, null);//GEN-BEGIN:|46-getter|1|46-postInit
            alert.setTimeout(Alert.FOREVER);//GEN-END:|46-getter|1|46-postInit
            // write post-init user code here
        }//GEN-BEGIN:|46-getter|2|
        return alert;
    }
    //</editor-fold>//GEN-END:|46-getter|2|

    //<editor-fold defaultstate="collapsed" desc=" Generated Getter: features ">//GEN-BEGIN:|51-getter|0|51-preInit
    /**
     * Returns an initiliazed instance of features component.
     * @return the initialized component instance
     */
    public Form getFeatures() {
        if (features == null) {//GEN-END:|51-getter|0|51-preInit
            // write pre-init user code here
            features = new Form("features", new Item[] { getTableItem(), getStringItem4() });//GEN-BEGIN:|51-getter|1|51-postInit
            features.addCommand(getBackCommand1());
            features.setCommandListener(this);//GEN-END:|51-getter|1|51-postInit
            // write post-init user code here
        }//GEN-BEGIN:|51-getter|2|
        return features;
    }
    //</editor-fold>//GEN-END:|51-getter|2|



    //<editor-fold defaultstate="collapsed" desc=" Generated Getter: backCommand1 ">//GEN-BEGIN:|53-getter|0|53-preInit
    /**
     * Returns an initiliazed instance of backCommand1 component.
     * @return the initialized component instance
     */
    public Command getBackCommand1() {
        if (backCommand1 == null) {//GEN-END:|53-getter|0|53-preInit
            // write pre-init user code here
            backCommand1 = new Command("Back", Command.BACK, 0);//GEN-LINE:|53-getter|1|53-postInit
            // write post-init user code here
        }//GEN-BEGIN:|53-getter|2|
        return backCommand1;
    }
    //</editor-fold>//GEN-END:|53-getter|2|

    //<editor-fold defaultstate="collapsed" desc=" Generated Getter: exitCommand2 ">//GEN-BEGIN:|55-getter|0|55-preInit
    /**
     * Returns an initiliazed instance of exitCommand2 component.
     * @return the initialized component instance
     */
    public Command getExitCommand2() {
        if (exitCommand2 == null) {//GEN-END:|55-getter|0|55-preInit
            // write pre-init user code here
            exitCommand2 = new Command("Exit", Command.EXIT, 0);//GEN-LINE:|55-getter|1|55-postInit
            // write post-init user code here
        }//GEN-BEGIN:|55-getter|2|
        return exitCommand2;
    }
    //</editor-fold>//GEN-END:|55-getter|2|



    //<editor-fold defaultstate="collapsed" desc=" Generated Getter: pimAlert ">//GEN-BEGIN:|61-getter|0|61-preInit
    /**
     * Returns an initiliazed instance of pimAlert component.
     * @return the initialized component instance
     */
    public Alert getPimAlert() {
        if (pimAlert == null) {//GEN-END:|61-getter|0|61-preInit
            // write pre-init user code here
            pimAlert = new Alert("Pim API loaded?", "no further help... sorry.", null, null);//GEN-BEGIN:|61-getter|1|61-postInit
            pimAlert.setTimeout(Alert.FOREVER);//GEN-END:|61-getter|1|61-postInit
            // write post-init user code here
        }//GEN-BEGIN:|61-getter|2|
        return pimAlert;
    }
    //</editor-fold>//GEN-END:|61-getter|2|

    //<editor-fold defaultstate="collapsed" desc=" Generated Getter: tableItem ">//GEN-BEGIN:|63-getter|0|63-preInit
    /**
     * Returns an initiliazed instance of tableItem component.
     * @return the initialized component instance
     */
    public TableItem getTableItem() {
        if (tableItem == null) {//GEN-END:|63-getter|0|63-preInit
            // write pre-init user code here
            tableItem = new TableItem(getDisplay(), "System properties");//GEN-BEGIN:|63-getter|1|63-postInit
            tableItem.setModel(new PropertiesTableModel());//GEN-END:|63-getter|1|63-postInit
            // write post-init user code here
        }//GEN-BEGIN:|63-getter|2|
        return tableItem;
    }
    //</editor-fold>//GEN-END:|63-getter|2|

    //<editor-fold defaultstate="collapsed" desc=" Generated Getter: tableModel1 ">//GEN-BEGIN:|64-getter|0|64-preInit
    /**
     * Returns an initiliazed instance of tableModel1 component.
     * @return the initialized component instance
     */
    public SimpleTableModel getTableModel1() {
        if (tableModel1 == null) {//GEN-END:|64-getter|0|64-preInit
            // write pre-init user code here
            tableModel1 = new SimpleTableModel(new java.lang.String[][] {//GEN-BEGIN:|64-getter|1|64-postInit
                new java.lang.String[] { "", "" }}, new java.lang.String[] { "Property", "Value" });//GEN-END:|64-getter|1|64-postInit
            // write post-init user code here
        }//GEN-BEGIN:|64-getter|2|
        return tableModel1;
    }
    //</editor-fold>//GEN-END:|64-getter|2|

    //<editor-fold defaultstate="collapsed" desc=" Generated Getter: stringItem4 ">//GEN-BEGIN:|66-getter|0|66-preInit
    /**
     * Returns an initiliazed instance of stringItem4 component.
     * @return the initialized component instance
     */
    public StringItem getStringItem4() {
        if (stringItem4 == null) {//GEN-END:|66-getter|0|66-preInit
            // write pre-init user code here
            stringItem4 = new StringItem("System platform", System.getProperty("microedition.platform"));//GEN-LINE:|66-getter|1|66-postInit
            // write post-init user code here
        }//GEN-BEGIN:|66-getter|2|
        return stringItem4;
    }
    //</editor-fold>//GEN-END:|66-getter|2|

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
