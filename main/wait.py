import time
from PyQt5 import QtCore, QtGui, QtWidgets
from setting import *


class Wait(object):

    def __init__(self, text, login_bool=False):
        self.button_T_F = False
        self.wait_window = QtWidgets.QDialog()
        self.wait_window.setFixedSize(400, 200)
        self.wait_window.setWindowTitle(text)
        self.wait_window.setWindowIcon(QtGui.QIcon(TU_BIAO_ICON_PATH))
        self.lable = QtWidgets.QLabel(self.wait_window)
        self.lable.setGeometry(QtCore.QRect(25, 0, 350, 100))
        self.lable.setFont(QtGui.QFont("宋体", 15))
        self.lable.setText(text)
        if text == "未输入账号和密码！" or login_bool is True:
            self.button = QtWidgets.QPushButton(self.wait_window)
            self.button.setGeometry(QtCore.QRect(50, 125, 100, 50))
            self.button.setText("取消")
            self.button.setFont(QtGui.QFont("宋体", 15))
            self.button.clicked.connect(lambda: self.button_click(self.button))
            self.button_1 = QtWidgets.QPushButton(self.wait_window)
            self.button_1.setGeometry(QtCore.QRect(250, 125, 100, 50))
            self.button_1.setText("登入")
            self.button_1.setStyleSheet("color: blue")
            self.button_1.setFont(QtGui.QFont("宋体", 15))
            self.button_1.clicked.connect(lambda: self.button_click(self.button_1))

    def button_click(self, button):
        if button.text() == "登入":
            self.button_T_F = True
        self.wait_window.close()
