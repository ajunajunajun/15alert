# coding: UTF-8
import pywinauto
from PIL import Image
import pytesseract
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon

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
        app = pywinauto.application.Application().connect(title_re=".*NoxPlayer.*")
        app_form = app.window(title_re = u".*NoxPlayer.*")
        app_form.capture_as_image().save('screenshot.png')

        im = Image.open('screenshot.png')
        im_w, im_h = im.size
        im_crop = im.crop((100, 200, 550, 250))
        im_crop.save('screenshot.png', quality=95)

        im = Image.open('screenshot.png')
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
        number = pytesseract.image_to_string(im)
        print(number)
        if number == 'round 15':
            print('round 15 だよ！！！')


if __name__ == '__main__':

    myApp = QApplication(sys.argv)
    myWindow = Window()
    myWindow.show()

    sys.exit(myApp.exec_())
