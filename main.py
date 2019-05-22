# coding: UTF-8
import sys
import os
import threading
import warnings
warnings.simplefilter("ignore", UserWarning)
sys.coinit_flags = 2
import pywinauto
from PIL import Image, ImageEnhance, ImageOps
import pytesseract
from win10toast import ToastNotifier
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QThread

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.resize(260, 200)
        self.move(200, 200)
        self.setWindowTitle('15Alert')
        self.setWindowIcon(QIcon('hiyoko.png'))

        lbl = QLabel('ROUND15をお知らせするよ\nDota2を起動してからボタン押してね', self)
        lbl.move(30,20)

        self.img = QLabel(self)
        pixmap = QPixmap('screenshot.png')
        pixmap = pixmap.scaledToWidth(200)
        self.img.setPixmap(pixmap)
        self.img.move(30,60)

        self.flag = 0

        self.lblrun = QLabel('stopping', self)
        self.lblrun.move(30,120)

        btn = QPushButton('START', self)
        btn.resize(100,40)
        btn.move(30,140)
        btn.clicked.connect(self.buttonClicked)

        btn2 = QPushButton('STOP', self)
        btn2.resize(100,40)
        btn2.move(130,140)
        btn2.clicked.connect(self.buttonClicked2)

    def alert(self):
        app = pywinauto.application.Application().connect(title_re=".*Dota.*")
        app_form = app.window(title_re = ".*Dota.*")
        app_form.capture_as_image().save('screenshot.png')

        im = Image.open('screenshot.png')
        im_w, im_h = im.size
        im_crop = im.crop((im_w/6*2.2, 0, im_w/6*2.6, im_h/35))
        gray = im_crop.convert("L")                     # グレイスケールに変換
        im_crop = gray.point(lambda x: 0 if x < 150 else x)   # 値が230以下は0になる
        im_crop.save('screenshot.png', quality=95)
        im.close()

        im = Image.open('screenshot.png')
        pytesseract.pytesseract.tesseract_cmd = r'./Tesseract-OCR/tesseract.exe'
        number = pytesseract.image_to_string(im,lang="eng")
        print(number)
        str = number.find('ROUND 15')
        if str != -1:
            toaster = ToastNotifier()
            toaster.show_toast("15Alert","ROUND15だよ！！！！")
            self.lblrun.setText('stopping')
            print('stop')
            self.flag = 0
        else:
            if self.flag == 1:
                t = threading.Timer(5,self.alert)
                t.start()
            else:
                self.lblrun.setText('stopping')
                print('stop')
                self.flag = 0

        pixmap = QPixmap('screenshot.png')
        pixmap = pixmap.scaledToWidth(200)
        self.img.setPixmap(pixmap)
        im.close()


    def buttonClicked(self):
        if self.flag == 0:
            self.lblrun.setText('running')
            print('start')
            self.flag = 1
            self.t = threading.Thread(target=self.alert)
            self.t.start()

    def buttonClicked2(self):
        if self.flag == 1:
            self.lblrun.setText('stopping')
            self.flag = -1

if __name__ == '__main__':
    myApp = QApplication(sys.argv)
    myWindow = Window()
    myWindow.show()

    os._exit(myApp.exec_())
