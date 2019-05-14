# coding: UTF-8
import pywinauto
from PIL import Image
import pytesseract

app = pywinauto.application.Application().connect(title_re=u".*メモ帳.*")
app_form = app.window(title_re = u".*メモ帳.*")
app_form.capture_as_image().save('screenshot.png')

im = Image.open('screenshot.png')
im_w, im_h = im.size
im_crop = im.crop((0, 0, im_w/2, 100))
im_crop.save('screenshot.png', quality=95)
