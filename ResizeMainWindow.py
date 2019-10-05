from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class ResizeMainWindow(QMainWindow):
	resizeSignal = pyqtSignal()
	wheelSignal = pyqtSignal()
	keySignal = pyqtSignal()
	dragSignal = pyqtSignal()

	wheelAngleDeltaY = 0
	isCtrlPressed = False
	isInDragMode = False

	def resizeEvent(self,event):
		self.resizeSignal.emit()

	def wheelEvent(self, wEvent):
		self.wheelAngleDeltaY = wEvent.angleDelta().y()
		self.wheelSignal.emit()

	def keyPressEvent(self, kEvent):
		if(kEvent.key()==Qt.Key_Control):
			self.isCtrlPressed = True
			self.setCursor(Qt.CrossCursor)
			self.isInDragMode = False
			self.dragSignal.emit()
		# QMessageBox.information(self,"aaa",str(kEvent.key()))
		self.keySignal.emit()

	def keyReleaseEvent(self, kEvent):
		if(kEvent.key()==Qt.Key_Control):
			self.isCtrlPressed = False
			self.setCursor(Qt.ArrowCursor)
			self.isInDragMode = False
			self.dragSignal.emit()
		
		self.keySignal.emit()
	
	def mousePressEvent(self, mEvent):        
		if(not self.isCtrlPressed):
			self.setCursor(Qt.OpenHandCursor)
			self.isInDragMode = True
			self.dragSignal.emit()      

	def mouseReleaseEvent(self, mEvent):
		self.setCursor(Qt.ArrowCursor)
		self.isInDragMode = False
		self.dragSignal.emit()
                    
	def mouseMoveEvent(self, mEvent):
		if(not self.isCtrlPressed):
			self.setCursor(Qt.OpenHandCursor)
			self.isInDragMode = True
			self.dragSignal.emit()
