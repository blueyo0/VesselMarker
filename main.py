# -*- coding: utf-8 -*-

import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PaintView import *
from mainWindow import *
from ResizeMainWindow import *


if __name__ == '__main__':
	app = QApplication(sys.argv)
	myWin = ResizeMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(myWin)

#----------------------------[ Slots ]--------------------------------#
	def updatePenWidth():
		ui.ImageView.setPenWidth(
			ui.PenWidthSpinBox.value()
		)
	
	def updateMaskAlpha():
		ui.ImageView.setAlphaValue(
			int(ui.MaskComboBox.currentText()[:-1])
		)

	def openImageAndMask():
		image_path = QFileDialog.getOpenFileName(
			ui.centralwidget,
			"选择 training image", 
			filter="Images(*.jpg *.png)"
		)
		mask_path = QFileDialog.getOpenFileName(
			ui.centralwidget,
			"选择 mask", 
			filter="Images(*.jpg *.png)"
		)
		# print(type(image_path),image_path[0])		
		ui.ImageView.initialize(
			QImage(image_path[0]),
			QImage(mask_path[0])
		)

	def savePaintImg():
		save_path = QFileDialog.getSaveFileName(
			ui.centralwidget,
			"选择保存位置", 
			filter="Images(*.png)"
		)
		ui.ImageView.savePaintImg(save_path[0])
	
	def saveAnnotation():
		save_path = QFileDialog.getSaveFileName(
			ui.centralwidget,
			"选择保存位置", 
			filter="Images(*.jpg *.png)"
		)	
		ui.ImageView.saveAnnotation(save_path[0])

	def updatePos():
		size = ui.AnnotationView.size()
		mapPt1 = ui.ImageView.mapToScene(size.width(),size.height())
		mapPt2 = ui.ImageView.mapToScene(0,0)
		if(ui.ImageView.scrollToRight):
			ui.AnnotationView.ensureVisible(			
				mapPt1.x(),
				mapPt1.y(),
				0,0,0,0					
			)
		else:
			ui.AnnotationView.ensureVisible(
				mapPt2.x(),
				mapPt2.y(),
				0,0,0,0
			)

	def updateDisplay():		
		scale = ui.ImageView.resizeScale*ui.ImageView.scale
		if(ui.checkBox.checkState()==Qt.Checked):
			size = QSize(
				ui.ImageView.resultImg.width()*scale,
				ui.ImageView.resultImg.height()*scale
			)
			updatePos()
		else:
			ui.AnnotationView.centerOn(0,0)
			size = ui.AnnotationView.size()
		ui.AnnotationView.displayImg = ui.ImageView.resultImg				
		ui.AnnotationView.totalScene.removeItem(ui.AnnotationView.displayItem)	
		ui.AnnotationView.displayItem = QGraphicsPixmapItem(
			QPixmap.fromImage(
				ui.AnnotationView.displayImg.scaled(
					size,
					aspectRatioMode=Qt.KeepAspectRatio
				)
			)
		)		
		ui.AnnotationView.totalScene.addItem(ui.AnnotationView.displayItem)
		ui.AnnotationView.setScene(ui.AnnotationView.totalScene)

	# 更新两个View的大小和位置
	def updateSize():
		# QMessageBox.information(myWin,"Help","Two mode can be selected")
		size_x = (myWin.width()-80)/2
		size_y = myWin.height()-110
		ui.ImageView.setGeometry(20,50,size_x,size_y)
		ui.AnnotationView.setGeometry(60+size_x,50,size_x,size_y)

	def wheelToResize():
		if(myWin.wheelAngleDeltaY>0):
			ui.ImageView.zoomIn()
		else:
			ui.ImageView.zoomOut()

	def updateCtrlStatus():
		ui.ImageView.isCtrlPressed = myWin.isCtrlPressed
		# QMessageBox.information(myWin,"aaa",str(ui.ImageView.isCtrlPressed))
	
	def updateDragStatus():
		if(myWin.isInDragMode):
			ui.ImageView.setDragMode(QGraphicsView.ScrollHandDrag)
		else:
			ui.ImageView.setDragMode(QGraphicsView.NoDrag)			

	def updateScrollBarStatus():
		if(ui.checkBox_2.checkState()==Qt.Checked):
			ui.ImageView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
			ui.ImageView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		else:
			ui.ImageView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
			ui.ImageView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)



#-----------------------------------[ Connect ]--------------------------------#
	ui.PenWidthSpinBox.valueChanged.connect(updatePenWidth)
	ui.MaskComboBox.currentIndexChanged.connect(updateMaskAlpha)
	ui.action_image.triggered.connect(openImageAndMask)
	ui.action_2.triggered.connect(saveAnnotation)
	ui.action_3.triggered.connect(savePaintImg)
	ui.ImageView.paintSignal.connect(updateDisplay)
	ui.checkBox_2.stateChanged.connect(updateScrollBarStatus)
	myWin.resizeSignal.connect(updateSize)
	myWin.wheelSignal.connect(wheelToResize)
	myWin.keySignal.connect(updateCtrlStatus)
	myWin.dragSignal.connect(updateDragStatus)

#--------------------------------[ AnnotationView ]----------------------------#
	#创建右侧窗体,设置显示内容
	ui.AnnotationView.totalScene = QGraphicsScene(ui.AnnotationView)
	ui.AnnotationView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
	ui.AnnotationView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
	ui.AnnotationView.sceneSize = QSize(
		    int(ui.AnnotationView.width()), 
		    int(ui.AnnotationView.height())
		)
	ui.AnnotationView.displayImg = ui.ImageView.resultImg				
	ui.AnnotationView.displayItem = QGraphicsPixmapItem(
		QPixmap.fromImage(
			ui.AnnotationView.displayImg.scaled(
				ui.AnnotationView.sceneSize,
				aspectRatioMode=Qt.KeepAspectRatio
			)
		)
	)		
	ui.AnnotationView.totalScene.addItem(ui.AnnotationView.displayItem)
	ui.AnnotationView.setScene(ui.AnnotationView.totalScene)

#-----------------------------------[ Novel end ]------------------------------#	
	myWin.show()
	sys.exit(app.exec_())