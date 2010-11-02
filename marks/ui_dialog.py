# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'h:\Dokumenty\Pobieranie\generator.ui'
#
# Created: Fri Jun 11 05:41:03 2010
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(587, 283)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(9, 9, 56, 42))
        self.label.setObjectName("label")
        self.temat = QtGui.QLineEdit(Dialog)
        self.temat.setGeometry(QtCore.QRect(71, 20, 133, 20))
        self.temat.setObjectName("temat")
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(230, 10, 51, 42))
        self.label_4.setObjectName("label_4")
        self.radioButton = QtGui.QRadioButton(Dialog)
        self.radioButton.setGeometry(QtCore.QRect(522, 9, 56, 18))
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtGui.QRadioButton(Dialog)
        self.radioButton_2.setGeometry(QtCore.QRect(522, 33, 56, 18))
        self.radioButton_2.setObjectName("radioButton_2")
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(9, 57, 126, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(200, 60, 57, 20))
        self.label_3.setObjectName("label_3")
        self.spozn = QtGui.QSpinBox(Dialog)
        self.spozn.setGeometry(QtCore.QRect(273, 57, 56, 20))
        self.spozn.setMaximum(10)
        self.spozn.setObjectName("spozn")
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(380, 60, 56, 20))
        self.label_6.setObjectName("label_6")
        self.punkty = QtGui.QSpinBox(Dialog)
        self.punkty.setGeometry(QtCore.QRect(430, 60, 57, 20))
        self.punkty.setMaximum(10)
        self.punkty.setProperty("value", QtCore.QVariant(10))
        self.punkty.setObjectName("punkty")
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(9, 109, 56, 16))
        self.label_5.setObjectName("label_5")
        self.ocena = QtGui.QPlainTextEdit(Dialog)
        self.ocena.setGeometry(QtCore.QRect(9, 129, 569, 114))
        self.ocena.setObjectName("ocena")
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(9, 249, 444, 25))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.student = QtGui.QLineEdit(Dialog)
        self.student.setGeometry(QtCore.QRect(280, 20, 181, 20))
        self.student.setObjectName("student")
        self.raport = QtGui.QSpinBox(Dialog)
        self.raport.setGeometry(QtCore.QRect(80, 60, 64, 20))
        self.raport.setMinimum(1)
        self.raport.setMaximum(6)
        self.raport.setObjectName("raport")
        self.label.setBuddy(self.temat)
        self.label_4.setBuddy(self.student)
        self.label_2.setBuddy(self.raport)
        self.label_3.setBuddy(self.spozn)
        self.label_6.setBuddy(self.punkty)
        self.label_5.setBuddy(self.ocena)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.temat, self.student)
        Dialog.setTabOrder(self.student, self.radioButton)
        Dialog.setTabOrder(self.radioButton, self.radioButton_2)
        Dialog.setTabOrder(self.radioButton_2, self.raport)
        Dialog.setTabOrder(self.raport, self.spozn)
        Dialog.setTabOrder(self.spozn, self.punkty)
        Dialog.setTabOrder(self.punkty, self.ocena)
        Dialog.setTabOrder(self.ocena, self.buttonBox)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Temat:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "Student:", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton.setText(QtGui.QApplication.translate("Dialog", "JwUM", None, QtGui.QApplication.UnicodeUTF8))
        self.radioButton_2.setText(QtGui.QApplication.translate("Dialog", "JaPitI", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Raport", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Spóźnienie:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dialog", "Punkty", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog", "Opis:", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    print sys.argv
    raw_input()
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

