# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'picUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class PointLine(object):
    startPt = QPoint()
    endPt = QPoint()
    width = 1

class PaintView(QtWidgets.QGraphicsView):
    isPressed = False
    mouseButton = Qt.NoButton
    sPt = QPoint() #起点
    ePt = QPoint() #终点
    lineArr = [] #线条数组，存放PointLine
    scale = 1.0
    resizeScale = 1.0
    penWidth = 5
    paintSignal = pyqtSignal()
    scrollToRight = True
    originPt = QPoint()

    def __init__(self,dialog):
        super().__init__(dialog)
        self.setMouseTracking(True)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.show()
        img = QImage(256,256,QImage.Format_ARGB32)
        img.fill(QColor(255, 255, 255, 255))
        self.initialize(img,img)        

    def initialize(self,image,mask):
        self.lineArr = []
        self.scale = 1.0
        self.resizeScale = 1.0
        self.defaultImg = image.convertToFormat(QImage.Format_ARGB32)
        self.maskImg = mask.convertToFormat(QImage.Format_ARGB32)
        self.defaultMaskImg = QImage(self.maskImg.size(),QImage.Format_ARGB32)
        for i in range(self.maskImg.width()):
            for j in range(self.maskImg.height()):
                color = self.maskImg.pixel(i,j)%0x1000000
                if(color > 0x000000):
                    self.maskImg.setPixel(i,j,0x00FFFFFF)
                    self.defaultMaskImg.setPixel(i,j,0x00FFFFFF)
                else:
                    self.maskImg.setPixel(i,j,0x80000000)
                    self.defaultMaskImg.setPixel(i,j,0xFF000000)

        self.paintImg = QImage(self.defaultImg.size(),QImage.Format_ARGB32)
        self.paintImg.fill(QColor(255, 255, 255, 0))
        self.imageScene = QGraphicsScene(self)
        
        length = self.defaultImg.width() \
                if (self.defaultImg.width()>self.defaultImg.height()) \
                else self.defaultImg.height() 
        if(length!=0):       
            self.resizeScale = self.width()/length*1.2
        newSize = QSize(
            int(self.defaultImg.width()*self.resizeScale), 
            int(self.defaultImg.height()*self.resizeScale)
        )

        self.imageItem = QGraphicsPixmapItem(
            QPixmap.fromImage(
                self.defaultImg.scaled(
                    newSize,
                    aspectRatioMode=Qt.KeepAspectRatio
                )
            )
        )      
        self.maskItem = QGraphicsPixmapItem(
            QPixmap.fromImage(
                self.maskImg.scaled(
                    newSize,
                    aspectRatioMode=Qt.KeepAspectRatio
                )
            )   
        )
        self.paintItem = QGraphicsPixmapItem(
            QPixmap.fromImage(
                self.paintImg.scaled(
                    newSize,
                    aspectRatioMode=Qt.KeepAspectRatio
                )
            )
        )
        self.imageScene.addItem(self.imageItem)
        self.imageScene.addItem(self.maskItem)
        self.imageScene.addItem(self.paintItem)
        self.setScene(self.imageScene)
        self.originPt = self.mapToScene(0,0) # modified at 26 sep 
        self.updateResult()    

#----------------------------[ Set Function ]--------------------------------#   
    def setAlphaValue(self, alpha):
        #-------TODO--------------------------------------
        # 执行PaintView的setAlphaValue后mask就没了      
        bgColor = 0x1000000*int(2.55*alpha)
        # print("%8x " %bgColor,alpha)
        for i in range(self.maskImg.width()):
            for j in range(self.maskImg.height()):
                color = self.maskImg.pixel(i,j)%0x1000000
                if(color > 0x000000):
                    self.maskImg.setPixel(i,j,0x00FFFFFF)
                else:
                    self.maskImg.setPixel(i,j,bgColor)
        self.imageScene.removeItem(self.maskItem)
        s = self.scale*self.resizeScale
        newSize = QSize(
            int(self.defaultImg.width()*s), 
            int(self.defaultImg.height()*s)
        )
        self.maskItem = QGraphicsPixmapItem(
            QPixmap.fromImage(
                self.maskImg.scaled(
                    newSize,
                    aspectRatioMode=Qt.KeepAspectRatio
                )
            )   
        )
        self.imageScene.addItem(self.maskItem)

    def setPenWidth(self,w):
        self.penWidth = w
#----------------------------[ Bool Function ]--------------------------------#
    def isOutMask(self,viewPt):
        imagePt_f = self.mapToScene(int(viewPt.x()),int(viewPt.y()))\
                                    /(self.resizeScale*self.scale)
        imagePt = QPoint(int(imagePt_f.x()),int(imagePt_f.y()))
        # print(self.maskImg.pixel(imagePt))
        if((self.maskImg.pixel(imagePt)%0x1000000) < 0xFFFFFF):
            return False
        else:
            return True
            
    def isInDistance(self, sPt, mPt, pw2):
        smPt = self.mapToScene(mPt)/(self.resizeScale*self.scale)
        x2 = sPt.x()/self.resizeScale-smPt.x()
        x2 = x2*x2
        y2 = sPt.y()/self.resizeScale-smPt.y()
        y2 = y2*y2
        # print(x2,',',y2,' with',smPt)
        return x2 + y2 < pw2

#----------------------------[ Paint System ]--------------------------------#
    def scaleChange(self,ns):
        s = ns*self.resizeScale
        self.imageScene.removeItem(self.imageItem)
        self.imageScene.removeItem(self.maskItem)
        self.imageScene.removeItem(self.paintItem)
        newSize = QSize(
            int(self.defaultImg.width()*s), 
            int(self.defaultImg.height()*s)
        )
        self.imageItem = QGraphicsPixmapItem(
            QPixmap.fromImage(
                self.defaultImg.scaled(
                    newSize,
                    aspectRatioMode=Qt.KeepAspectRatio
                )
            )
        )      
        self.maskItem = QGraphicsPixmapItem(
            QPixmap.fromImage(
                self.maskImg.scaled(
                    newSize,
                    aspectRatioMode=Qt.KeepAspectRatio
                )
            )   
        )
        self.paintItem = QGraphicsPixmapItem(
            QPixmap.fromImage(
                self.paintImg.scaled(
                    newSize,
                    aspectRatioMode=Qt.KeepAspectRatio
                )
            )
        )
        self.imageScene.addItem(self.imageItem)       
        self.imageScene.addItem(self.maskItem)
        self.imageScene.addItem(self.paintItem)
        # self.setScene(self.imageScene)

    def zoomIn(self):
        if(self.scale > 20):
            return;
        self.scale = self.scale + 0.2
        if(self.scale > 2):
            self.scale = self.scale + 0.8   
        self.scaleChange(self.scale)

    def zoomOut(self):
        if(self.scale < 0.3):
            return;
        if(self.scale > 2):
            self.scale = self.scale - 0.8           
        self.scale = self.scale - 0.2       
        self.scaleChange(self.scale)   

    def drawLineArr(self):
        # self.paintImg = self.inverseMaskImg
        #----------- 【已解决】 ------------------------------------------------#
        # 如何解决painter的初始化及定位问题
        # 目前支持的QPaintDevice: 
        # QImage, QPicture, QPixmap, QPrinter, QSvgGenerator and QWidget
        # 使用格式:
        # qp = QPainter(QPaintDevice qpd)
        # 【最终确定在paintImg上进行绘制】
        qp = QPainter(self.paintImg)
        qp.setCompositionMode(QPainter.CompositionMode_SourceOver)
        # qp.setCompositionMode(QPainter.CompositionMode_DestinationOut)
        # qp.begin(self.maskImg)
        #------------------------------------------------------------------#
        pen = QPen()
        pen.setColor(QColor(255, 0, 0, 255))       
        offset = self.scale*self.resizeScale
        #-------------【已解决】------------------------------------------------------#
        # qp.drawLine(self.mapToScene(30,1)-self.mapFromScene(0,0), self.mapToScene(30,88)-self.mapFromScene(0,0))
        # BUG: 拖动和放缩会产生尾迹
        # 疑似是拖动时重新调用paintEvent时drawLine的位置计算出错
        # 在LineArr中存储坐标时，没有考虑拖动和放缩时的换算，需要将offset和scale都添加进去
        # 【最终的坐标公式如下】
        # newLine.startPt = (self.mapToScene(self.sPt)-self.mapToScene(self.mapFromScene(0,0)))/self.scale
        # newLine.endPt = (self.mapToScene(self.ePt)-self.mapToScene(self.mapFromScene(0,0)))/self.scale
        
        for i in range(len(self.lineArr)-1, -1, -1):
            pen.setWidth(self.lineArr[i].width)
            qp.setPen(pen)  
            qp.drawLine(
                self.lineArr[i].startPt/self.resizeScale, 
                self.lineArr[i].endPt/self.resizeScale
            )
            # print(self.lineArr[i].startPt/self.resizeScale,' ',self.lineArr[i].startPt/self.resizeScale)
        
        qp.setCompositionMode(QPainter.CompositionMode_DestinationOut)
        qp.drawImage(QPoint(0,0),self.defaultMaskImg)        
        qp.setCompositionMode(QPainter.CompositionMode_SourceOver)

        # ----------------------------------------------------------------------
        self.imageScene.removeItem(self.paintItem)
        self.paintItem = QGraphicsPixmapItem(
            QPixmap.fromImage(
                self.paintImg.scaled(
                    self.paintImg.width()*self.scale*self.resizeScale,
                    self.paintImg.height()*self.scale*self.resizeScale,
                    aspectRatioMode=Qt.KeepAspectRatio
                )
            )
        )
        self.imageScene.addItem(self.paintItem)
        qp.end()
        self.updateResult()

    def clearPaints(self):
        pass
        # TO-DO

    def updateResult(self):
        self.backgroundImg = QImage(self.paintImg.size(),QImage.Format_ARGB32)
        self.backgroundImg.fill(QColor(0,255,0,255))
        qp = QPainter(self.backgroundImg)
        qp.drawImage(QPoint(0,0),self.paintImg)
        qp.drawImage(QPoint(0,0),self.defaultMaskImg)
        qp.end()


#----------------------------[ File System ]--------------------------------#
    def saveAnnotation(self,path):
        self.updateResult()
        self.backgroundImg.save(path)

    def savePaintImg(self,path):
        self.paintImg.save(path)  
    
#----------------------------[ Event System ]--------------------------------#

    def dragMoveEvent(self, dmEvent):
        print(dmEvent.answerRect())

    def paintEvent(self,event):
        self.paintImg.fill(QColor(255, 255, 255, 0))
        super().paintEvent(event)
        # qp = QPainter(self.viewport())
        # qp.drawPixmap(QPoint(0,0),self.imageItem.pixmap())
        # qp.end()
        self.drawLineArr()
        newOriginPt = self.mapToScene(0,0) # modified at 26 sep
        if(newOriginPt.x()<self.originPt.x() or
           newOriginPt.y()<self.originPt.y()):
            self.scrollToRight = False
        elif(newOriginPt.x()>self.originPt.x() or
             newOriginPt.y()>self.originPt.y()):
            self.scrollToRight = True
        self.originPt = newOriginPt
        self.paintSignal.emit()
        
    def mousePressEvent(self, mEvent):        
        # [print color]
        # imagePt_f = self.mapToScene(mEvent.pos())/(self.resizeScale*self.scale)
        # imagePt = QPoint(int(imagePt_f.x()),int(imagePt_f.y()))
        # print((self.maskImg.pixel(imagePt)%0x1000000) < 0xFFFFFF)
        if(self.isOutMask(mEvent.pos())):            
            self.sPt = mEvent.pos()
            self.ePt = mEvent.pos()
            self.mouseButton = mEvent.button()    

    def mouseReleaseEvent(self, mEvent):
        self.mouseButton = Qt.NoButton
                    
    def mouseMoveEvent(self, mEvent):
        # print("isOutMask: ",self.isOutMask(mEvent.pos()))
        if(
            self.mouseButton == Qt.LeftButton and 
            self.isOutMask(mEvent.pos())
        ):
            self.ePt = mEvent.pos()           
            newLine = PointLine()
            newLine.startPt = (self.mapToScene(self.sPt)-self.mapToScene(self.mapFromScene(0,0)))/self.scale
            newLine.endPt = (self.mapToScene(self.ePt)-self.mapToScene(self.mapFromScene(0,0)))/self.scale
            newLine.width = self.penWidth
            self.lineArr.append(newLine)
            self.sPt = self.ePt
        elif(
            self.mouseButton == Qt.RightButton
        ):
            pw2 = self.penWidth*self.penWidth
            mPt = mEvent.pos()
            # print("Right: ",mPt)
            for i in range(len(self.lineArr)-1, -1, -1):
                if( 
                    self.isInDistance(self.lineArr[i].startPt,mPt,pw2) or 
                    self.isInDistance(self.lineArr[i].endPt,mPt,pw2)
                ):
                    self.lineArr.pop(i)
                    # print("pop ",i)
 
    def wheelEvent (self, wEvent):
        if(wEvent.angleDelta().y()>0):
            self.zoomIn()
        else:
            self.zoomOut()



