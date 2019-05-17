# coding: UTF-8
import pywinauto
from PIL import Image
import pytesseract
import sys
import os
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QThread
from tkinter import messagebox

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.resize(260, 180)
        self.move(300, 300)
        self.setWindowTitle('15Alert')
        self.setWindowIcon(QIcon('hiyoko.png'))

        lbl = QLabel('ROUND15をお知らせするよ\nDota2を起動してからボタン押してね', self)
        lbl.move(30,20)

        self.img = QLabel(self)
        pixmap = QPixmap('screenshot.png')
        self.img.setPixmap(pixmap)
        self.img.resize(200,40)
        self.img.move(30,60)

        self.flag = 0

        btn = QPushButton('START', self)
        btn.resize(100,40)
        btn.move(30,120)
        btn.clicked.connect(self.buttonClicked)

        btn2 = QPushButton('STOP', self)
        btn2.resize(100,40)
        btn2.move(130,120)
        btn2.clicked.connect(self.buttonClicked2)

    def alert(self):
        app = pywinauto.application.Application().connect(title_re=u".*メモ帳.*")
        app_form = app.window(title_re = u".*メモ帳.*")
        app_form.capture_as_image().save('screenshot.png')

        im = Image.open('screenshot.png')
        im_w, im_h = im.size
        im_crop = im.crop((100, 200, 550, 260))
        im_crop.save('screenshot.png', quality=95)
        im.close()

        im = Image.open('screenshot.png')
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
        number = pytesseract.image_to_string(im)
        print(number)
        str = number.find('ROUND 15')
        if str != -1:
            print('ROUND 15 だよ！！！')
            messagebox.showinfo("15Alert","ROUND15だよ！")
        else:
            if self.flag == 1:
                t = threading.Timer(5,self.alert)
                t.start()
            else:
                print('stop')
                self.flag = 0

        pixmap = QPixmap('screenshot.png')
        self.img.setPixmap(pixmap)
        im.close()


    def buttonClicked(self):
        if self.flag == 0:
            print('start')
            self.flag = 1
            self.t = threading.Thread(target=self.alert)
            self.t.start()

    def buttonClicked2(self):
        if self.flag == 1:
            self.flag = -1

if __name__ == '__main__':
    myApp = QApplication(sys.argv)
    myWindow = Window()
    myWindow.show()

    os._exit(myApp.exec_())
