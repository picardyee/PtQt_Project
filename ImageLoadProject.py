import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, qApp, QFileDialog, QMessageBox, QRubberBand, QLabel
from PyQt5.uic import loadUiType
from PyQt5.QtGui import *
from PyQt5.QtCore import QRect, Qt, QPoint, QSize, QRectF
import os
import glob
import cv2
import numpy as np

form_class = loadUiType("Image_loader.ui")[0]

class ViewerClass(QMainWindow, form_class):
    def __init__(self, parent=None):
        super().__init__()
        # QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.qPixmapVar = QPixmap()
        self.actionFile.triggered.connect(self.fileSelect)
        self.actionFolder.triggered.connect(self.folderSelect)
        self.NextButton.clicked.connect(self.NextClick)
        self.PreviousButton.clicked.connect(self.PreviousClick)
        self.CloseButton.clicked.connect(qApp.quit)
        self.idx = 0
        self.tmp = None

        # self.x0 = 0
        # self.y0 = 0
        # self.x1 = 0
        # self.y1 = 0
        # self.flag = False

    def fileSelect(self):
        filename = QFileDialog.getOpenFileName(self, 'open', '/Users/picardy/Downloads/Seungkyu/copied/')[0]
        if filename:
            self.image = cv2.imread(filename)
            self.setPhoto(self.image)

    def setPhoto(self, image):
        self.tmp = image
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        self.Image_label.setPixmap(QtGui.QPixmap.fromImage(image))

    def folderSelect(self):
        dirName = QFileDialog.getExistingDirectory(self, 'open', '/Users/picardy/Downloads/Seungkyu/copied/')
        self.files = []
        if dirName:
            for file in glob.glob(os.path.join(dirName, '*.png')):
                self.files.append(file)
            for file in glob.glob(os.path.join(dirName, '*.jpg')):
                self.files.append(file)
            self.qPixmapVar.load(self.files[0])
            self.Image_label.setPixmap(self.qPixmapVar)

    def NextClick(self, file):
        try:
            if self.idx < len(self.files):
                self.idx += 1
                self.qPixmapVar.load(self.files[self.idx])
                self.Image_label.setPixmap(self.qPixmapVar)
                print(self.idx)
        except IndexError:
            self.endOfimage()
            self.idx -= 1
        except AttributeError:
            self.endOfimage()
            self.idx -= 1

    def endOfimage(self):
        msg = QMessageBox()
        msg.setWindowTitle('Error!')
        msg.setIcon(QMessageBox.Warning)
        msg.setText('마지막 이미지 입니다.')
        msg.setStandardButtons(QMessageBox.Ok)
        result = msg.exec_()

    def PreviousClick(self):
        if self.idx > 0:
            self.idx -= 1
            self.qPixmapVar.load(self.files[self.idx])
            self.qPixmapVar = self.qPixmapVar.scaled(700, 700, aspectRatioMode=True)
            self.Image_label.setPixmap(self.qPixmapVar)
            print(self.idx)
        else:
            self.firstImage()

    def firstImage(self):
        msg = QMessageBox()
        msg.setWindowTitle('Error!')
        msg.setIcon(QMessageBox.Warning)
        msg.setText('첫 번째 이미지 입니다.')
        msg.setStandardButtons(QMessageBox.Ok)
        result = msg.exec_()

# mouse Draw Event
class mouseEvent(ViewerClass):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False

    def __init__(self):
        super().__init__()

    def mousePressEvent(self, event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()
        print(self.x0, self.y0)

    def mouseReleaseEvent(self, event):
        self.flag = False
        print(self.x1, self.y1)

    def mouseMoveEvent(self, event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        rect = QRect(self.x0, self.y0, abs(self.x1 - self.x0), abs(self.y1 - self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))


#11
    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     painter.drawPixmap(self.rect(), self.image)
    #
    # def mousePressEvent(self, event):
    #     if event.button() == Qt.LeftButton:
    #         self.drawing = True
    #         self.lastPoint = event.pos()
    #
    # def mouseMoveEvent(self, event):
    #     if event.buttons() and Qt.LeftButton and self.drawing:
    #         painter = QPainter(self.image)
    #         painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))
    #         painter.drawLine(self.lastPoint, event.pos())
    #         self.lastPoint = event.pos()
    #         self.update()
    #
    # def mouseReleaseEvent(self, event):
    #     if event.button == Qt.LeftButton:
    #         self.drawing = False

# 22
    # def mousePressEvent(self, event):
    #     self.flag = True
    #     self.x0 = event.x()
    #     self.y0 = event.y()
    #
    # def mouseReleaseEvent(self, event):
    #     self.flag = False
    #
    # def mouseMoveEvent(self, event):
    #     if self.flag:
    #         self.x1 = event.x()
    #         self.y1 = event.y()
    #         self.update()
    #
    # def paintEvent(self, event):
    #     super().paintEvent(event)
    #     rect = QRect(self.x0, self.y0, abs(self.x1-self.x0), abs(self.y1-self.y0))
    #     painter = QPainter(self)
    #     painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
    #     painter.drawRect(rect)


app = QApplication(sys.argv)
myWindow = ViewerClass(None)
myWindow.show()
app.exec_()