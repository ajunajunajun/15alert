# coding: UTF-8
import pywinauto

app = pywinauto.application.Application().connect(title_re=u".*メモ帳.*")
app_form = app.window(title_re = u".*メモ帳.*")
app_form.capture_as_image().save('ss.png')
