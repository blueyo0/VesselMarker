# -*- coding: utf-8 -*-

import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PaintView import *
from mainWindow import *

# 目前程序结构说明：
#  main.py 定义File IO 和 左右图像的同步刷新
#  mainWindow.py UI界面设计
#  paintView.py 加强版QGraphicsView

if __name__ == '__main__':
	app = QApplication(sys.argv)
	myWin = QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(myWin)

	# slot
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
				ui.ImageView.backgroundImg.width()*scale,
				ui.ImageView.backgroundImg.height()*scale
			)
			updatePos()
		else:
			ui.AnnotationView.centerOn(0,0)
			size = ui.AnnotationView.size()
		ui.AnnotationView.displayImg = ui.ImageView.backgroundImg				
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

	ui.PenWidthSpinBox.valueChanged.connect(updatePenWidth)
	ui.MaskComboBox.currentIndexChanged.connect(updateMaskAlpha)
	ui.action_image.triggered.connect(openImageAndMask)
	ui.action_2.triggered.connect(saveAnnotation)
	ui.action_3.triggered.connect(savePaintImg)
	ui.ImageView.paintSignal.connect(updateDisplay)

	ui.AnnotationView.totalScene = QGraphicsScene(ui.AnnotationView)
	ui.AnnotationView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
	ui.AnnotationView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
	ui.AnnotationView.sceneSize = QSize(
		    int(ui.AnnotationView.width()), 
		    int(ui.AnnotationView.height())
		)

	ui.AnnotationView.displayImg = ui.ImageView.backgroundImg				
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
	
	myWin.show()
	sys.exit(app.exec_())