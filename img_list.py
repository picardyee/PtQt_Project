import sys
from PyQt5.QtWidgets import QMainWindow,QApplication, qApp, QFileDialog
from PyQt5.uic import loadUiType
from PyQt5.QtGui import *
import os
import glob

form_class = loadUiType("imageViewer.ui")[0]

class ViewerClass(QMainWindow, form_class):
    def __init__(self, parent=None):
        QMainWindow.__init__(self,parent)
        self.setupUi(self)
        self.qPixmapVar = QPixmap()
        self.actionSelect.triggered.connect(self.fileSelect)
        self.pushButton.clicked.connect(self.moveNextClick)
        self.actionExit.triggered.connect(qApp.quit)
        self.idx = 0

    def fileSelect(self):
        #fname = QFileDialog.getOpenFileName(self)
        dirName = QFileDialog.getExistingDirectory(self, 'Open Folder', 'E:/MyPhoto/몽이')
        self.files = []
        for file in glob.glob(os.path.join(dirName, '*.png')):
            self.files.append(file)
        self.qPixmapVar.load(self.files[0])
        self.qPixmapVar = self.qPixmapVar.scaled(700, 400, aspectRatioMode=True)
        self.label.setPixmap(self.qPixmapVar)

    def moveNextClick(self):
        self.idx += 1
        self.qPixmapVar.load(self.files[self.idx])
        self.qPixmapVar = self.qPixmapVar.scaled(700, 400, aspectRatioMode=True)
        self.label.setPixmap(self.qPixmapVar)

app = QApplication(sys.argv)
myWindow = ViewerClass(None)
myWindow.show()
app.exec_()