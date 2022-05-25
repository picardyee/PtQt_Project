import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, qApp, QFileDialog, QMessageBox, QRubberBand, QLabel, QWidget
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
        self.Image_label = QLabel()
        self.actionFile.triggered.connect(self.fileSelect)
        self.actionFolder.triggered.connect(self.folderSelect)
        self.NextButton.clicked.connect(self.NextClick)
        self.PreviousButton.clicked.connect(self.PreviousClick)
        self.CloseButton.clicked.connect(qApp.quit)
        self.idx = 0
        self.tmp = None

        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.flag = False

        self.begin, self.destination = QPoint(), QPoint()


    def fileSelect(self):
        filename = QFileDialog.getOpenFileName(self, 'open', '/Users/picardy/Downloads/Seungkyu/copied/')[0]
        if filename:
            self.image = cv2.imread(filename)
            self.dir_h, self.dir_w, channel = self.image.shape
            frame = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
            self.Image_label.setPixmap(QtGui.QPixmap.fromImage(image))
            print(self.dir_w, self.dir_h)

    def folderSelect(self):
        dirName = QFileDialog.getExistingDirectory(self, 'open', '/Users/picardy/Downloads/Seungkyu/copied/')
        self.files = []
        if dirName:
            for file in glob.glob(os.path.join(dirName, '*.png')):
                self.files.append(file)
            self.cv_file = cv2.imread(self.files[self.idx])
            self.dir_h, self.dir_w, channel = self.cv_file.shape
            self.qPixmapVar.load(self.files[0])
            self.Image_label.setPixmap(self.qPixmapVar)
            QMainWindow.resize(self, self.dir_w, self.dir_h)
            print(self.dir_w, self.dir_h)

    def NextClick(self, file):
        try:
            if self.idx < len(self.files):
                self.idx += 1
                self.qPixmapVar.load(self.files[self.idx])
                self.Image_label.setPixmap(self.qPixmapVar)
                self.cv_file = cv2.imread(self.files[self.idx])
                self.dir_h, self.dir_w, channel = self.cv_file.shape
                QMainWindow.resize(self, self.dir_w, self.dir_h)
                print(self.idx)
                print(self.dir_w, self.dir_h)

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
            self.cv_file = cv2.imread(self.files[self.idx])
            self.dir_h, self.dir_w, channel = self.cv_file.shape
            QMainWindow.resize(self, self.dir_w, self.dir_h)
            print(self.idx)
            print(self.dir_w, self.dir_h)
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

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.qPixmapVar)

        if not self.begin.isNull() and not self.destination.isNull():
            rect = QRect(self.begin, self.destination)
            painter.setPen(QPen(Qt.green, 2, Qt.SolidLine))
            painter.drawRect(rect.normalized())

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.begin = event.pos()
            self.destination = self.begin
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.destination = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            rect = QRect(self.begin, self.destination)
            painter = QPainter(self.pix)
            painter.drawRect(rect.normalized())

            self.begin, self.destination = QPoint(), QPoint()
            self.update()

app = QApplication(sys.argv)
myWindow = ViewerClass(None)
myWindow.show()
app.exec_()

