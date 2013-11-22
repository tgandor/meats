#!/usr/bin/env python

import locale
import sys
import codecs
from PyQt4 import QtCore, QtGui

from ui_dialog import Ui_Dialog

class Dialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
    def accept(self):
        self.make_file()
        
    def reject(self):
        # self.make_file()
        QtGui.QDialog.reject(self)
        
    def make_file(self):
        przedm, pen = ('jum', 'Czas oddania') if self.ui.radioButton.isChecked() else ('jpi', 'Time penalty')
        report = self.ui.raport.value()
        punkty = self.ui.punkty.value()
        student = self.ui.student.text()
        #print dir(self.ui.ocena.document().toPlainText())
        fname = '%s_r%d_%s_%dpkt.txt' % (przedm, report, student, punkty)
        print fname
        komunikat = """%s

%s: -%d pkt

%s""" % (
            self.ui.temat.text(),
            pen,
            self.ui.spozn.value(),
            self.ui.ocena.document().toPlainText()
    )
        print komunikat
        codecs.open(fname, 'wt', locale.getdefaultlocale()[1]).write(komunikat)        
    @QtCore.pyqtSignature("int")
    def on_spozn_valueChanged(self, value):
        self.ui.punkty.setMaximum(10-int(value))
        self.ui.punkty.setValue(10-int(value))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    calculator = Dialog()
    calculator.show()
    sys.exit(app.exec_())
