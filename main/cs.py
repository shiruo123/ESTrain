# # # -*- coding:utf-8 -*-
# # # Time : 2019/08/18 下午 4:42
# # # Author : 御承扬
# # # e-mail:2923616405@qq.com
# # # project:  PyQt5
# # # File : qt34_MenuTest.py
# # # @software: PyCharm
# #
import threading
import time

from selenium import webdriver
# import sys
#
# from PyQt5 import QtWidgets
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# import getdata
#
# print(getdata.rfp().get("data").get("searchgui").copy().get("date"))
#
#
# class MenuDemo(QMainWindow):
#     def __init__(self, parent=None):
#         super(MenuDemo, self).__init__(parent)
#         self.setWindowTitle("Menu 示例")
#         self.setWindowIcon(QIcon("./images/Python2.ico"))
#         self.setFixedSize(1000, 1000)
#         self.lineedit = QtWidgets.QLineEdit(self)
#         self.lineedit.setGeometry(QRect(100, 100, 100, 50))
#         self.lineedit.textChanged.connect(lambda: self.text_print(self.lineedit.text()))
#         # self.lineedit.editingFinished.connect(lambda: self.text_print(self.lineedit.text()))
#         self.lineedit1 = QtWidgets.QLineEdit(self)
#         self.lineedit1.setGeometry(QRect(100, 200, 100, 50))
#         # self.lineedit1.selectionChanged.connect(lambda: self.text_print(self.lineedit1.selectedText()))
#         self.button = QtWidgets.QPushButton(self)
#         self.button.setGeometry(QRect(200, 100, 100, 50))
#         print(self.button.geometry().getRect())
#         self.button.setText("确定")
#         self.dateEdit = QtWidgets.QDateEdit(self)
#         self.dateEdit.setGeometry(QRect(750, 100, 200, 40))
#         self.dateEdit.setCalendarPopup(True)
#         self.dateEdit.setObjectName("dateEdit")
#         self.dateEdit.setDate(QDate(2023, 4, 25))
#         self.dateEdit.dateChanged.connect(lambda: self.text_print(self.dateEdit.text()))
#         bar = self.menuBar()
#         # self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏主窗口边界
#         bar.setWindowIcon(QIcon("../images/main.ico"))
#         # self.lay.setSpacing(0)  # 去除控件间的距离
#         # self.lay.setContentsMargins(0, 0, 0, 0)
#         file = bar.addMenu("File")
#         file.addAction("New")
#         save = QAction("Save", self)
#         save.setShortcut("Ctrl+S")
#         file.addAction(save)
#         edit = file.addMenu("Edit")
#         edit.addAction("copy")
#         edit.addAction("paste")
#         quit = QAction("Quit", self)
#         file.addAction(quit)
#         file.triggered[QAction].connect(self.processTrigger)
#
#     def text_print(self, text):
#         text = text.replace("/", "-")
#         if len(text) == 0:
#             print("空")
#         print(text)
#
#     @staticmethod
#     def processTrigger(q):
#         print(q.text() + " is triggered")
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     win = MenuDemo()
#     win.show()
#     sys.exit(app.exec_())
# # a = int("a")
# # a = None
# # if a:
# #     print(1)
#
# a = ["1", "2"]
# b = a[3]
# from selenium.webdriver.common.by import By
#
#
# browser = webdriver.Chrome()
# browser.get("https://www.12306.cn/index/")
# browser.find_element(By.XPATH, '//*[@id="fromStationText"]').click()
# with open("PlaceName.txt", "a", encoding="utf-8") as fp:
#     for i in range(2, 7):
#         browser.find_element(By.XPATH, f'//*[@id="nav_list{i}"]').click()
#         flip = browser.find_element(By.XPATH, f'//*[@id="flip_cities2"]')
#         while True:
#             uls = browser.find_elements(By.XPATH, f'//*[@id="ul_list{i}"]/ul')
#             for ul in uls:
#                 lis = ul.find_elements(By.XPATH, 'li')
#                 for li in lis:
#                     # try:
#                     li_text = li.get_attribute("title")
#                     if len(li_text) != 0:
#                         fp.write(li_text+"\n")
#                     # except:
#                     #     pass
#             a_s = flip.find_elements(By.XPATH, 'a')
#             if len(a_s) == 1 and a_s[0].text == "« 上一页":
#                 break
#             for a in a_s:
#                 if a.text == "下一页 »":
#                     a.click()
#                     continue


def a(text):
    if text == 1:
        # print(1.0)
        exit()
    time.sleep(3)
    # print(2.0)


def b(text):
    print(1.1)
    a(text)
    print(2.1)


# threading.Thread(target=b, args=(1, )).start()
# threading.Thread(target=b, args=(3, )).start()
# threading.Thread(target=b, args=(4, )).start()
a_1 = (1, 2, 3, )
b_1 = [2, 3]
b_1.extend(a_1)
print(b_1)
for i in range(3):
    print(i)

a_2 = [1, ]
if len(a_2):
    print(1234)
