import logging
import time
from setting import *
import selenium.webdriver.support.ui
from PyQt5 import QtCore, QtGui, QtWidgets
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import getdata
from selenium.common.exceptions import *
from selenium import webdriver
from wait import Wait

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")


class LoginQdialog(object):
    def __init__(self):
        self.tr_list = []
        self.button_close_T_F = False
        self.button_event_text = None
        self.MainWindow = QtWidgets.QDialog()
        self.list = []
        self.getdata = getdata.rfp()
        self.MainWindow.setObjectName("登入页面")
        self.MainWindow.setFixedSize(1000, 950)
        self.MainWindow.setWindowIcon(QtGui.QIcon(TU_BIAO_ICON_PATH))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(15)
        self.label = QtWidgets.QLabel(self.MainWindow)
        self.label.setGeometry(QtCore.QRect(120, -250, 1920, 1080))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("../images/12306main1.jpg"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.MainWindow)
        self.label_2.setGeometry(QtCore.QRect(150, 600, 100, 50))
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(font)
        self.label_3 = QtWidgets.QLabel(self.MainWindow)
        self.label_3.setGeometry(QtCore.QRect(150, 700, 100, 50))
        self.label_3.setObjectName("label_3")
        self.label_3.setFont(font)
        self.lineEdit = QtWidgets.QLineEdit(self.MainWindow)
        self.lineEdit.setGeometry(QtCore.QRect(300, 600, 500, 60))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setFont(font)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.MainWindow)
        self.lineEdit_2.setGeometry(QtCore.QRect(300, 700, 500, 60))
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setFont(font)
        self.checkBox = QtWidgets.QCheckBox(self.MainWindow)
        self.checkBox.setGeometry(QtCore.QRect(850, 700, 120, 60))
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setFont(font)
        self.checkBox_1 = QtWidgets.QCheckBox(self.MainWindow)
        self.checkBox_1.setGeometry(QtCore.QRect(300, 775, 200, 60))
        self.checkBox_1.setText("爬取乘车人")
        self.checkBox_1.setFont(font)
        self.checkBox_2 = QtWidgets.QCheckBox(self.MainWindow)
        self.checkBox_2.setGeometry(QtCore.QRect(500, 775, 360, 60))
        self.checkBox_2.setFont(font)
        self.checkBox_2.setText("抢票防电脑熄屏")
        self.pushButton_2 = QtWidgets.QPushButton(self.MainWindow)
        self.pushButton_2.setGeometry(QtCore.QRect(350, 850, 300, 80))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setFont(font)
        self.pb1()
        self.pb2(self.MainWindow)
        self.retranslateUi(self.MainWindow)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def pb1(self):
        self.checkBox.clicked.connect(self.pb1_cl)

    def pb2(self, MainWindow):
        self.pushButton_2.clicked.connect(lambda: self.pb2_cl(MainWindow))

    def pb1_cl(self):
        _translate = QtCore.QCoreApplication.translate
        if self.checkBox.text() == "显示":
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.checkBox.setText(_translate("MainWindow", "隐藏"))
        else:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
            self.checkBox.setText(_translate("MainWindow", "显示"))

    def pb2_cl(self, MainWindow):
        if len(self.lineEdit.text()) == 0:
            self.lineEdit.setPlaceholderText("账号不能为空")
        elif len(self.lineEdit_2.text()) < 6:
            self.lineEdit_2.clear()
            self.lineEdit_2.setPlaceholderText("密码不少于6位")
        else:
            MainWindow.close()
            self.list.append(self.lineEdit.text())
            self.list.append(self.lineEdit_2.text())
            self.button_close_T_F = True

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "登入页面"))
        self.label_2.setText(_translate("MainWindow", "账号:"))
        self.label_3.setText(_translate("MainWindow", "密码:"))
        self.lineEdit.setText(_translate("MainWindow", self.getdata.get("data").get("logingui").get("account")))
        self.lineEdit_2.setText(_translate("MainWindow", self.getdata.get("data").get("logingui").get("password")))
        self.checkBox.setText(_translate("MainWindow", "显示"))
        self.pushButton_2.setText(_translate("MainWindow", "确定"))

    def init_login(self):
        """
        爬取乘客信息
        :return:
        """
        # try:
        self.tr_list = []
        # 判断是否正常登入，即是否点击了确定按钮进行了登入
        if self.button_close_T_F is False:
            return
        try:
            option = webdriver.ChromeOptions()
            # option.add_argument('headless')
            # option.add_argument("--window-size=1920,1050")
            # option.add_argument('blink-settings=imagesEnabled=false')
            option.add_experimental_option('excludeSwitches', ['enable-automation'])
            option.binary_location = CHROME_PATH
            self.browser = webdriver.Chrome(options=option)
            self.browser.minimize_window()
            self.wait = selenium.webdriver.support.ui.WebDriverWait(self.browser, 3)
            self.browser.get("https://kyfw.12306.cn/otn/resources/login.html")
            self.browser.find_element(By.XPATH, '//*[@id="J-userName"]').send_keys(self.lineEdit.text())
            self.browser.find_element(By.XPATH, '//*[@id="J-password"]').send_keys(self.lineEdit_2.text())
            self.browser.find_element(By.XPATH, '//*[@id="J-login"]').click()
            time.sleep(2)
            script = 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined,});'
            self.browser.execute_script(script)
            while True:
                try:
                    # 获取滑块位置
                    span = self.browser.find_element(By.XPATH, '//*[@id="nc_1_n1z"]')
                except NoSuchElementException:
                    # 如果没有找到滑块的位置，就点击左上角的滑块验证进行使其出现滑块
                    self.browser.find_element(By.XPATH, '//*[@id="verification"]/li[1]/a').click()
                    continue
                try:
                    action = webdriver.ActionChains(self.browser)
                    action.click_and_hold(span)
                    # 移动滑块
                    action.drag_and_drop_by_offset(span, 300, 0).perform()
                except:
                    pass
                try:
                    # 是否出现刷新验证
                    self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div[2]/div/span/a'))).click()
                    continue
                except:
                    pass
                try:
                    self.button_event_text = self.browser.find_element(By.XPATH, '//*[@id="J-login-error"]/span').text.split("。")[0]
                    self.browser.close()
                    self.button_close_T_F = False
                    return
                except:
                    pass
                try:
                    # 点击乘车人，使其加载乘车人信息
                    self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="cylianxiren"]/a'))).click()
                except:
                    try:
                        self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="cylianxiren"]/a'))).click()
                    except:
                        self.button_event_text = (self.browser.find_element(By.XPATH, '//*[@id="J-login-error"]/span').text.split("。")[0])
                        self.browser.close()
                        self.button_close_T_F = False
                        return
                break
        except:
            self.button_close_T_F = False
            return
        # self.browser.find_element(By.XPATH, "/html/body/div[6]/div[2]/div[2]/div[2]/a").click()
        # self.browser.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/ul/li[6]/ul/li[1]/a').click()
        # 以下为乘车人信息爬取
        tbody = self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="content_list"]/div/div[2]/table/tbody')))
        for tr in tbody.find_elements(By.XPATH, "tr"):
            td_list = []
            for td in range(2, 6):
                td_list.append(tr.find_element(By.XPATH, f'td[{td}]/div').text)
            logging.info("以爬取:" + str(td_list))

            self.tr_list.append(td_list)
        logging.info("爬取结果:"+str(self.tr_list))
        logging.info("乘客信息保存成功")
        self.browser.close()
        # except:
        #     self.init_login()
