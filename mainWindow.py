# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PaintView import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 470)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.ImageView = PaintView(self.centralwidget)
        self.ImageView.setGeometry(QtCore.QRect(20, 50, 360, 360))
        self.ImageView.setObjectName("ImageView")
        self.AnnotationView = QtWidgets.QGraphicsView(self.centralwidget)
        self.AnnotationView.setGeometry(QtCore.QRect(420, 50, 360, 360))
        self.AnnotationView.setObjectName("AnnotationView")
        self.PenWidthSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.PenWidthSpinBox.setGeometry(QtCore.QRect(90, 10, 61, 22))
        self.PenWidthSpinBox.setObjectName("PenWidthSpinBox")
        self.PenWidthSpinBox.setValue(5)
        self.PenWidthSpinBox.setMinimum(1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 11, 54, 20))
        self.label.setObjectName("label")
        self.MaskComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.MaskComboBox.setGeometry(QtCore.QRect(260, 10, 61, 22))
        self.MaskComboBox.setObjectName("MaskComboBox")
        self.MaskComboBox.addItem("0%")
        self.MaskComboBox.addItem("25%")
        self.MaskComboBox.addItem("50%")
        self.MaskComboBox.addItem("75%")
        self.MaskComboBox.addItem("100%")
        self.MaskComboBox.setCurrentIndex(2)   
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(180, 10, 71, 20))
        self.label_2.setObjectName("label_2")

        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(480, 10, 61, 22))
        self.checkBox.setCheckState(Qt.Checked)
        self.checkBox.setObjectName("checkBox")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(500, 10, 71, 20))
        self.label_3.setObjectName("label_3")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_image = QtWidgets.QAction(MainWindow)
        self.action_image.setObjectName("action_image")
        self.action_2 = QtWidgets.QAction(MainWindow)
        self.action_2.setObjectName("action_2")
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.menu.addAction(self.action_image)
        self.menu.addSeparator()
        self.menu.addAction(self.action_2)
        self.menu.addAction(self.action_3)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "笔刷大小:"))
        self.label_2.setText(_translate("MainWindow", "mask透明度:"))
        self.label_3.setText(_translate("MainWindow", "视角跟随"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.action_image.setText(_translate("MainWindow", "打开 image和mask"))
        self.action_2.setText(_translate("MainWindow", "存储 Annotation"))
        self.action_3.setText(_translate("MainWindow", "存储 透明png"))
