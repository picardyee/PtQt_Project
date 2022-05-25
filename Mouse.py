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

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.us()

    def us(self):
        filename = QFileDialog.getOpenFileName(self, 'open', '/Users/picardy/Downloads/Seungkyu/copied/')[0]
        if filename:
            self.image = cv2.imread(filename)
            self.dir_h, self.dir_w, channel = self.image.shape

            self.window_width, self.window_height = self.dir_w, self.dir_h
            self.setMinimumSize(self.window_width, self.window_height)

            frame = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
            # self.Image_label.setPixmap(QtGui.QPixmap.fromImage(image))
            print(self.dir_w, self.dir_h)


            # self.window_width, self.window_height = 1200, 800
            # self.setMinimumSize(self.window_width, self.window_height)

            layout = QVBoxLayout()
            self.setLayout(layout)

            # self.pix = QPixmap(self.rect().size())
            # self.pix.fill(Qt.white)

            self.pix = QPixmap(image)
            self.begin, self.destination = QPoint(), QPoint()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.pix)

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 30px;
        }
    ''')

    myapp = MyApp()
    myapp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('closing')