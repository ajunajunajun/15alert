# coding: UTF-8
from pywinauto import application
from time import sleep

app = application.Application().start("notepad.exe")

# sleep(1)
# app[].CaptureAsImage().save('window.png')
