// Adapted from: https://webapps.stackexchange.com/a/119646

function myFunction() {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var s = ss.getActiveSheet();
    var c = s.getActiveCell();
    var fldr = DriveApp.getFolderById("<folder id here>");
    var files = fldr.getFiles();
    var names = [], f, str;
    while (files.hasNext()) {
        f = files.next();
        str = f.getUrl();
        names.push([str]);
    }
    s.getRange(c.getRow(), c.getColumn(), names.length).setValues(names);
}
