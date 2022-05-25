from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QLabel, QDialog
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import QRect, Qt, QPoint
import os, glob, cv2, sys

form_class = uic.loadUiType("Image_loader2.ui")[0]


class Label_Dialog(QDialog):
    def __init__(self, parent):
        super(Label_Dialog, self).__init__(parent)
        uic.loadUi('/Users/picardy/PycharmProjects/pythonProject/Label.ui', self)
        self.Green.setStyleSheet('background-color: #7cfc00')
        self.Yellow.setStyleSheet('background-color: yellow')
        self.Blue.setStyleSheet('background-color: #0066ff')
        self.parent = parent
        self.show()
        self.Green.clicked.connect(parent.greenColor)
        self.Yellow.clicked.connect(parent.yellowColor)
        self.Blue.clicked.connect(parent.blueColor)
        self.Green_line.textChanged.connect(self.func_G)
        self.Yellow_line.textChanged.connect(self.func_Y)
        self.Blue_line.textChanged.connect(self.func_B)
        self.Path_line.textChanged.connect(self.labelPath)
        self.toolButton.clicked.connect(self.path)

    def path(self):
        dir_path = QFileDialog.getExistingDirectory(self, 'open')
        for file in dir_path:
            exist = self.Path_line.text()
            self.Path_line.setText(exist + file)
        print(dir_path)

    def func_G(self):
        self.parent.Label_G = self.Green_line.text()

    def func_Y(self):
        self.parent.Label_Y = self.Yellow_line.text()

    def func_B(self):
        self.parent.Label_B = self.Blue_line.text()

    def labelPath(self):
        self.parent.path = self.Path_line.text()

class ViewerClass(QMainWindow, form_class):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)
        self.qPixmapVar = QPixmap()
        self.Image_label = QLabel()
        self.actionFile.triggered.connect(self.fileSelect)
        self.actionDirectory.triggered.connect(self.folderSelect)
        self.NextButton.clicked.connect(self.NextClick)
        self.PreviousButton.clicked.connect(self.PreviousClick)
        self.actionClose.triggered.connect(self.close)
        self.actionOpen_Tool.triggered.connect(self.openTool)

        self.idx = 0
        self.flag = 0
        self.start, self.end = QPoint(), QPoint()
        self.Label_G = ()
        self.Label_Y = ()
        self.Label_B = ()
        self.path = ()
        self.image = None

    # def imageSave(self):
    #     filename = QFileDialog.getSaveFileName(filter="JPG(*.jpg);;PNG(*.png);;TIFF(*.tiff);;BMP(*.bmp)")[0]
    #     cv2.imwrite(filename, self.image)

    def fileSelect(self):
        filename = QFileDialog.getOpenFileName(self, 'open', '/Users/picardy/Downloads/Seungkyu/copied/')[0]
        if filename:
            self.image = cv2.imread(filename)
            self.dir_h, self.dir_w, channel = self.image.shape
            self.qPixmapVar.load(filename)
            self.Image_label.setPixmap(self.qPixmapVar)
            QMainWindow.resize(self, self.dir_w, self.dir_h)
            print(self.dir_w, self.dir_h)

            # folderName = self.image
            self.name = filename[filename.rfind("/"): - 4]
            self.savename = str(self.path) + str(self.name) + '.txt'
            try:
                if str(self.path) == self.savename:
                    print(self.savename)
                    self.write = open(self.savename, 'w', encoding='utf8')
                else:
                    os.mkdir(str(self.path))
                    self.savename = str(self.path) + str(self.name) + '.txt'
                    self.write = open(self.savename, 'w', encoding='utf8')
            except:
                self.Path_error()

    def folderSelect(self):
        dirName = QFileDialog.getExistingDirectory(self, 'open', '/Users/picardy/Downloads/Seungkyu/copied/')
        self.files = []
        if dirName:
            for file in glob.glob(os.path.join(dirName, '*.png')):
                self.files.append(file)
            for file in glob.glob(os.path.join(dirName, '*.jpg')):
                self.files.append(file)
            self.image = cv2.imread(self.files[self.idx])
            self.dir_h, self.dir_w, channel = self.image.shape
            self.qPixmapVar.load(self.files[0])
            self.Image_label.setPixmap(self.qPixmapVar)
            QMainWindow.resize(self, self.dir_w, self.dir_h)

            folderName = self.files[self.idx]
            self.name = folderName[folderName.rfind("/"): - 4]
            self.savename = str(self.path) + str(self.name) + '.txt'
            try:
                if str(self.path) == self.savename:
                    print(self.savename)
                    self.write = open(self.savename, 'w', encoding='utf8')
                else:
                    os.mkdir(str(self.path))
                    self.savename = str(self.path) + str(self.name) + '.txt'
                    self.write = open(self.savename, 'w', encoding='utf8')
            except:
                self.Path_error()

    def NextClick(self):
        try:
            if self.idx < len(self.files):
                self.idx += 1
                self.qPixmapVar.load(self.files[self.idx])
                self.Image_label.setPixmap(self.qPixmapVar)
                self.cv_file = cv2.imread(self.files[self.idx])
                self.dir_h, self.dir_w, channel = self.cv_file.shape
                QMainWindow.resize(self, self.dir_w, self.dir_h)

                folderName = self.files[self.idx]
                self.name = folderName[folderName.rfind("/"): - 4]
                self.savename = str(self.path) + str(self.name) + '.txt'
                self.write = open(self.savename, 'w', encoding='utf8')
                # print(self.idx)
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
            self.Image_label.setPixmap(self.qPixmapVar)
            self.cv_file = cv2.imread(self.files[self.idx])
            self.dir_h, self.dir_w, channel = self.cv_file.shape
            QMainWindow.resize(self, self.dir_w, self.dir_h)
            folderName = self.files[self.idx]
            self.name = folderName[folderName.rfind("/"): - 4]
            self.savename = str(self.path) + str(self.name) + '.txt'
            self.write = open(self.savename, 'w', encoding='utf8')
            # print(self.idx)
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

        if not self.start.isNull() and not self.end.isNull():
            rect = QRect(self.start, self.end)
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            painter.drawRect(rect.normalized())

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.start = event.pos()
            self.end = self.start
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if not event.buttons() & Qt.LeftButton:
            if self.flag == 0:
                rect = QRect(self.start, self.end)
                painter = QPainter(self.qPixmapVar)
                painter.setPen(QPen(Qt.green, 2, Qt.SolidLine))
                painter.drawRect(rect.normalized())
                self.fileName()
                print('x0, y0 =', self.start.x(), self.start.y())
                print('x1, y1 =', self.end.x(), self.end.y())
                self.start, self.end = QPoint(), QPoint()
                self.update()
            elif self.flag == 1:
                rect = QRect(self.start, self.end)
                painter = QPainter(self.qPixmapVar)
                painter.setPen(QPen(Qt.yellow, 2, Qt.SolidLine))
                painter.drawRect(rect.normalized())
                self.fileName()
                print('x0, y0 =', self.start.x(), self.start.y())
                print('x1, y1 =', self.end.x(), self.end.y())
                self.start, self.end = QPoint(), QPoint()
                self.update()
            elif self.flag == 2:
                rect = QRect(self.start, self.end)
                painter = QPainter(self.qPixmapVar)
                painter.setPen(QPen(Qt.blue, 2, Qt.SolidLine))
                painter.drawRect(rect.normalized())
                self.fileName()
                print('x0, y0 =', self.start.x(), self.start.y())
                print('x1, y1 =', self.end.x(), self.end.y())
                self.start, self.end = QPoint(), QPoint()
                self.update()

    def fileName(self):
        # folderName = self.files[self.idx]
        # self.name = folderName[folderName.rfind("/"): - 4]
        # self.savename = str(self.path) + str(self.name) + '.txt'
        # if self.flag == 0:
        #     with open(self.savename, 'w', encoding='utf8') as self.write:
        if self.flag == 0:
            self.write.write('{4} 0 0 0 {0} {1} {2} {3} 0 0 0 0 0 0 0\n'
                             .format(self.start.x(), self.start.y(), self.end.x(), self.end.y(), self.Label_G))

        if self.flag == 1:
            self.write.write('{4} 0 0 0 {0} {1} {2} {3} 0 0 0 0 0 0 0\n'
                             .format(self.start.x(), self.start.y(), self.end.x(), self.end.y(), self.Label_Y))

        if self.flag == 2:
            self.write.write('{4} 0 0 0 {0} {1} {2} {3} 0 0 0 0 0 0 0\n'
                             .format(self.start.x(), self.start.y(), self.end.x(), self.end.y(), self.Label_B))

    def Path_error(self):
        msg = QMessageBox()
        msg.setWindowTitle('Error!')
        msg.setIcon(QMessageBox.Warning)
        msg.setText('Label 경로를 설정하세요')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.buttonClicked.connect(self.msg_Button)
        result = msg.exec_()

    def msg_Button(self):
        self.close()

    def openTool(self):
        Label_Dialog(self)

#change_Color

    def greenColor(self):
        self.flag = 0
        self.update()
        print(self.flag)

    def yellowColor(self):
        self.flag = 1
        self.update()
        print(self.flag)

    def blueColor(self):
        self.flag = 2
        self.update()
        print(self.flag)


app = QApplication(sys.argv)
myWindow = ViewerClass(None)
myWindow.show()
app.exec_()

