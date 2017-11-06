# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 360)
        Dialog.setMinimumSize(QtCore.QSize(500, 360))
        Dialog.setMaximumSize(QtCore.QSize(500, 360))
        Dialog.setWindowTitle("")
        Dialog.setStyleSheet("QDialog {\n"
" background-color: rgb(255, 255, 255);\n"
"}")
        #Dialog.setSizeGripEnabled(False)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(150, 20, 201, 61))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(190, 150, 111, 51))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("QPushButton:pressed {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,   stop:0 rgba(60, 186, 162, 255), stop:1 rgba(98, 211, 162, 255))\n"
"}\n"
"QPushButton {\n"
"     background-color: #3cbaa2; border: 0px solid black;\n"
"     border-radius: 7px;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    background-color: rgb(170, 170, 127)\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(21, 234, 461, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setText("")
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 290, 461, 41))
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setText("")
        self.label_3.setTextFormat(QtCore.Qt.AutoText)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(190, 90, 111, 41))
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("Dialog", "想被哪个小宝宝甜呀~"))
        self.pushButton.setText(_translate("Dialog", "原谅她"))

