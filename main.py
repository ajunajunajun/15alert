# coding: UTF-8
import pywinauto
from PIL import Image
import pytesseract
import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread

class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.resize(260, 180)
        self.move(300, 300)
        self.setWindowTitle('15Alert')
        self.setWindowIcon(QIcon('hiyoko.png'))

        btn = QPushButton('Button', self)
        btn.resize(200,40)
        btn.move(30,120)
        btn.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        app = pywinauto.application.Application().connect(title_re=u".*メモ帳.*")
        app_form = app.window(title_re = u".*メモ帳.*")
        app_form.capture_as_image().save('screenshot.png')

        im = Image.open('screenshot.png')
        im_w, im_h = im.size
        im_crop = im.crop((100, 200, 550, 260))
        im_crop.save('screenshot.png', quality=95)

        im = Image.open('screenshot.png')
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
        number = pytesseract.image_to_string(im)
        print(number)
        str = number.find('ROUND 15')
        if str != -1:
            print('ROUND 15 だよ！！！')
        QThread.sleep(3)

if __name__ == '__main__':
    myApp = QApplication(sys.argv)
    myWindow = Window()
    myWindow.show()

    sys.exit(myApp.exec_())
