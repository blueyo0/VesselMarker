# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'picUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(763, 307)
        self.imageView = QtWidgets.QGraphicsView(Dialog)
        self.imageView.setGeometry(QtCore.QRect(10, 10, 321, 281))
        self.imageView.setObjectName("imageView")
        self.maskView = QtWidgets.QGraphicsView(Dialog)
        self.maskView.setGeometry(QtCore.QRect(420, 10, 321, 281))
        self.maskView.setObjectName("maskView")
        self.zoomInButton = QtWidgets.QPushButton(Dialog)
        self.zoomInButton.setGeometry(QtCore.QRect(340, 10, 75, 61))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(36)
        self.zoomInButton.setFont(font)
        self.zoomInButton.setObjectName("zoomInButton")
        self.zoomOutButton = QtWidgets.QPushButton(Dialog)
        self.zoomOutButton.setGeometry(QtCore.QRect(340, 230, 75, 61))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(36)
        self.zoomOutButton.setFont(font)
        self.zoomOutButton.setObjectName("zoomOutButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.zoomInButton.setText(_translate("Dialog", "+"))
        self.zoomOutButton.setText(_translate("Dialog", "-"))
