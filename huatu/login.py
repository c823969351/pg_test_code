# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 400)
        Form.setMinimumSize(QtCore.QSize(500, 400))
        Form.setMaximumSize(QtCore.QSize(800, 700))
        self.x = QtWidgets.QLabel(Form)
        self.x.setGeometry(QtCore.QRect(20, 60, 61, 20))
        self.x.setObjectName("x")
        self.y = QtWidgets.QLabel(Form)
        self.y.setGeometry(QtCore.QRect(20, 100, 61, 21))
        self.y.setObjectName("y")
        self.x_line = QtWidgets.QLineEdit(Form)
        self.x_line.setGeometry(QtCore.QRect(80, 60, 111, 21))
        self.x_line.setObjectName("x_line")
        self.y_line = QtWidgets.QLineEdit(Form)
        self.y_line.setGeometry(QtCore.QRect(80, 100, 113, 20))
        self.y_line.setObjectName("y_line")
        self.drew = QtWidgets.QPushButton(Form)
        self.drew.setGeometry(QtCore.QRect(100, 140, 71, 31))
        self.drew.setObjectName("drew")
        self.exit = QtWidgets.QPushButton(Form)
        self.exit.setGeometry(QtCore.QRect(100, 200, 71, 31))
        self.exit.setObjectName("exit")
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(210, 40, 256, 192))
        self.textBrowser.setObjectName("textBrowser")
        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        icon = QtGui.QIcon
        Form.setWindowTitle(_translate("Draw", "Draw"))
        self.x.setText(_translate("Form", "    X"))
        self.y.setText(_translate("Form", "    Y"))
        self.drew.setText(_translate("Form", "生成"))
        self.exit.setText(_translate("Form", "退出"))
