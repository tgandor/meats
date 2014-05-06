# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dragplay.ui'
#
# Created: Sun Aug 14 22:16:55 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DropArea(object):
    def setupUi(self, DropArea):
        DropArea.setObjectName(_fromUtf8("DropArea"))
        DropArea.resize(400, 300)
        DropArea.setAcceptDrops(True)
        self.infoLabel = QtGui.QLabel(DropArea)
        self.infoLabel.setGeometry(QtCore.QRect(20, 10, 361, 16))
        self.infoLabel.setObjectName(_fromUtf8("infoLabel"))
        self.resultInfo = QtGui.QLabel(DropArea)
        self.resultInfo.setGeometry(QtCore.QRect(10, 270, 381, 16))
        self.resultInfo.setObjectName(_fromUtf8("resultInfo"))

        self.retranslateUi(DropArea)
        QtCore.QMetaObject.connectSlotsByName(DropArea)

    def retranslateUi(self, DropArea):
        DropArea.setWindowTitle(QtGui.QApplication.translate("DropArea", "DragDrop Player", None, QtGui.QApplication.UnicodeUTF8))
        self.infoLabel.setText(QtGui.QApplication.translate("DropArea", "Drag and drop something onto this area...", None, QtGui.QApplication.UnicodeUTF8))
        self.resultInfo.setText(QtGui.QApplication.translate("DropArea", "No previous object.", None, QtGui.QApplication.UnicodeUTF8))

