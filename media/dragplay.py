import sys
from subprocess import Popen
from PyQt4 import QtCore, QtGui
from ui_dragplay import Ui_DropArea
    
class DropArea(QtGui.QDialog):
    
    def __init__(self):
        super(DropArea, self).__init__()
        self.ui = Ui_DropArea()
        self.ui.setupUi(self)
        
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()
        
    def dropEvent(self, e):
        if e.mimeData().hasUrls():
            firstURL = e.mimeData().urls()[0].toString()
            self.ui.resultInfo.setText(firstURL)
            print firstURL
            Popen(['mplayer', firstURL])
        else:
            self.ui.resultInfo.setText("No URLs found!")
        # print e.mimeData().formats().join(",\n")
        # print e.mimeData().text()
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = DropArea()
    window.show()
    sys.exit(app.exec_())



