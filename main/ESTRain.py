import sys
import time
import wait
import loginGui
import data_proces
from PyQt5.QtCore import Qt
import data_save
import selen
from PyQt5 import QtCore, QtGui, QtWidgets
import qwidget
import threading
import logging
import wifi
import ctypes
from setting import *
import subprocess
import bide
from concurrent.futures import ThreadPoolExecutor


ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")
place_name_list = open("../PlaceName.txt", "r", encoding="utf-8").read().split("\n")


class Ui_MainWindow(object):
    def __init__(self):
        self.pool = ThreadPoolExecutor(max_workers=POOL_NUMBER)
        self.chrome_count = []
        self.data_list = 0
        self.wifi = False
        self.che_list = []
        self.data_15_1 = []
        self.now_date_M_D = [time.localtime().tm_mday, time.localtime().tm_mon]
        # 调用data_save类,以便后面的出发地、目的地、账号、密码、如期的保存v
        self.datasave = data_save.DataSave()
        # 调用sele类爬取车次数据的类
        self.pa = selen.paData()
        self.List = ['车次', '出发站\n到达站', '出发时间\n到达时间', '历时', '商务座\n特等座', '一等座', '二等座\n二等包座', '高级\n软卧', '软卧\n一等卧', '动卧', '硬卧\n二等卧', '软座', '硬座', '无座', '其他', '备注']
        # self.searchgui = searchGui.SearchQdialog()
        # self.searchgui.MainWindow1.exec_()
        self.wifi = wifi.WIFI()
        # 动态过去wifi的情况，如果有wifi就退出，没有则过几秒检查一次
        threading.Thread(target=self.wifi.wifi_update_time, args=(0.2, ), daemon=True).start()
        # 用线程调用browser_pa,作用是提前打开浏览器并打开网址以便节省后面爬取的时间
        threading.Thread(target=self.wifi_panduan, daemon=True).start()
        # if self.wifi.ret is False:

    def setupUi(self, MainWindow):
        self.data_data = []
        self.data = self.datasave.rjson.get("data").get("searchgui")
        try:
            self.date = time.strptime(self.data.get('date'), "%Y-%m-%d")
        except:
            self.date = time.localtime()
        # print(self.date)
        # MainWindow.setObjectName("ESTrain")
        self.MainWindow = MainWindow
        self.__init_pyqt()
        self.__init_set_Geometry()
        self.__init_set_objectname_text()
        self.__init_font()
        self.__select_checkbox()
        self.__init_disposition()
        self.__add_button()
        self.__init_connect()
        self.dataUi()
        self.MainWindow.statusBar()
        self.MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 20))
        self.menubar.setObjectName("menubar")
        self.MainWindow.window().setMenuBar(self.menubar)
        self.retranslateUi(self.MainWindow)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)
        self.__loginGui()
        self.__login_state()

    def __init_pyqt(self):
        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.lineedit_1 = QtWidgets.QLineEdit(self.centralwidget)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.dateEdit = QtWidgets.QDateEdit(self.centralwidget)
        self.button = QtWidgets.QPushButton(self.centralwidget)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.completer = QtWidgets.QCompleter(place_name_list)
        self.button_1 = QtWidgets.QPushButton(self.centralwidget)

    def __init_connect(self):
        self.lineedit.textChanged.connect(lambda: self.pa.fromStationText(self.lineedit.text()))
        self.lineedit_1.textChanged.connect(lambda: self.pa.toStationText(self.lineedit_1.text()))
        self.dateEdit.dateChanged.connect(lambda: self.pa.date_icon_1(self.dateEdit.text()))
        self.lineedit.setCompleter(self.completer)
        self.lineedit_1.setCompleter(self.completer)
        self.button.clicked.connect(lambda: self.button_click())
        self.button_1.clicked.connect(lambda: self.button_1_click())

    def __init_font(self):
        self.font = QtGui.QFont()
        self.font.setFamily("宋体")
        self.font.setPointSize(11)
        self.label.setFont(self.font)
        self.label_1.setFont(self.font)
        self.lineedit.setFont(self.font)
        self.label_2.setFont(QtGui.QFont("宋体", 12))
        self.lineedit_1.setFont(self.font)
        self.dateEdit.setFont(self.font)
        self.button.setFont(self.font)
        self.tableWidget.setFont(self.font)

    def __init_set_Geometry(self):
        self.MainWindow.setFixedSize(MAIN_WINDOWS_SIZE)
        self.label.setGeometry(LABEL_SIZE)
        self.lineedit.setGeometry(LINEEDIT_SIZE)
        self.label_1.setGeometry(LABEL_SIZE_1)
        self.label_2.setGeometry(LABEL_SIZE_2)
        self.lineedit_1.setGeometry(LINEEDIT_SIZE_1)
        self.dateEdit.setGeometry(DATE_EDIT_SIZE)
        self.button.setGeometry(BUTTON_SIZE)
        self.tableWidget.setGeometry(TABLEWIDGET_SIZE)
        self.button_1.setGeometry(BUTTON_SIZE_1)

    def __init_set_objectname_text(self):
        self.centralwidget.setObjectName("centralwidget")
        self.label.setText("出发地:")
        self.lineedit.setText(self.data.get("departure"))
        self.label_1.setText("目的地:")
        self.lineedit_1.setText(self.data.get("destination"))
        self.dateEdit.setObjectName("dateEdit")
        self.dateEdit.setDate(QtCore.QDate(self.date.tm_year, self.date.tm_mon, self.date.tm_mday))
        self.button.setText("查询")
        self.tableWidget.setObjectName("tableWidget")

    def __init_disposition(self):
        threading.Thread(target=self.wifi_F, daemon=True).start()
        # 窗口初始最大化
        self.MainWindow.showMaximized()
        self.MainWindow.setWindowIcon(QtGui.QIcon(TU_BIAO_ICON_PATH))
        self.label_2.setStyleSheet("color:red")
        self.dateEdit.setDisplayFormat("yyyy-MM-dd")
        self.dateEdit.setCalendarPopup(True)
        self.completer.setFilterMode(Qt.MatchStartsWith)
        # 设置表格行大小
        self.tableWidget.horizontalHeader().setDefaultSectionSize(117)
        # 设置表头的颜色增加美观
        self.tableWidget.horizontalHeader().setStyleSheet("QHeaderView::section{background:lightblue;}")
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.button_1.setStyleSheet("font: 25px;color: blue")
        self.button_1.setFlat(True)
        self.button_1.setCursor(QtGui.QCursor(Qt.PointingHandCursor))

    def __select_checkbox(self):
        t = ["GC-高铁", "D-动车", "Z-直达", "T-特快", "K-快速"]
        for i in range(5):
            self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
            self.checkBox.setGeometry(QtCore.QRect(1150 + 130 * i, 20, 130, 40))
            self.checkBox.setObjectName(f"checkBox{i}")
            self.checkBox.setFont(self.font)
            self.checkBox.setText(t[i])
            self.checkBox.clicked.connect(lambda: self.checkbox(self.checkBox.sender()))

    def __add_button(self):
        try:
            # 添加按钮到每行的最后一个位置上
            for i in range(self.data_list):
                self.new_btn = QtWidgets.QCommandLinkButton(self.data_15[i])
                self.new_btn.setObjectName(f"{i}")
                self.new_btn.clicked.connect(lambda: self.btn_college(self.new_btn.sender()))
                self.tableWidget.setCellWidget(i, 15, self.new_btn)
        except:
            pass

    def __login_state(self):
        if self.logingui.button_close_T_F:
            self.button_1.setText(f"{self.logingui.lineEdit.text()}\n注销")
        else:
            self.button_1.setText("请登入")

    def __loginGui(self):
        self.logingui = loginGui.LoginQdialog()
        self.logingui.MainWindow.exec_()
        logging.info("登入页面信息已保存")
        self.chengke_data_pa_is = self.logingui.checkBox_1.isChecked()
        if self.chengke_data_pa_is:
            # 登入信息填完后进入爬取状态，爬取乘客信息
            threading.Thread(target=self.login_wifi_panduan, daemon=True).start()
        if self.logingui.checkBox_2.isChecked():
            threading.Thread(target=bide.no_xipin, daemon=True).start()

    def checkbox(self, checkbox):
        """
        将得到的数据进行筛选，点击G的框就选择只有G的车次，可多选且按时间顺序排序
        :param checkbox: 获取点击的CheckBox的信息
        :return: None
        """
        # print(self.data_data, self.data_list)
        # 判断主窗口是否有数据且数据量要等于按钮的数量,这就说明爬取完了
        if len(self.data_data) == self.data_list and len(self.data_data) != 0:
            # 先将表中的数据全部清除
            self.tableWidget.clearContents()
            # 设置行数的初始值
            n = 0
            # 1. 数据保存部分
            # 判断checkbox是否被选中
            if checkbox.isChecked():
                # 如果checkbox被选中,在判断是否是只有一个被选中,如果是择self.data_15_1里面没有数据
                if len(self.data_15_1) == 0:
                    # 如果是只有一个checkbox被选中，用for将[“车次信息”，“车票信息”]传入给self.che_list、将[”预约“, 车票序号/排号]
                    for i in range(len(self.data_data)):
                        # 判断选择的开头是G还是K等，将其与车次信息的车次的首个相比如果相等就添加保存
                        if self.data_data[i][0][0][0] == checkbox.text()[0]:
                            self.che_list.append(self.data_data[i])
                            self.data_15_1.append([self.data_15[i], i])
                # 如果checkbox被选中，并且这不是第一个被选中的
                else:
                    # 首先用for循环所有数据
                    for i in range(len(self.data_data)):
                        # 判断选择的开头是G还是K等，将其与车次信息的车次的首个相比是否相等
                        if self.data_data[i][0][0][0] == checkbox.text()[0]:
                            # print("i", str(i))
                            # 如果相等循环已有的数据，因为这不是第一个被选中所以里面有数据
                            for j in range(len(self.data_15_1)):
                                # print("j:", str(self.data_15_1[j][1]))
                                # 判断已有的数据的车票序号/排号是否大于现在的车次信息
                                if int(self.data_15_1[j][1]) > i:
                                    # print(self.data_data[i])
                                    # 如果大于则将数据插入这条数据的后面
                                    self.che_list.insert(j, self.data_data[i])
                                    self.data_15_1.insert(j, [self.data_15[i], i])
                                    break
                            # 如果所有的数据都比过了，数据还没有保存则将数据直接保存，不用插入保存
                            else:
                                self.che_list.append(self.data_data[i])
                                self.data_15_1.append([self.data_15[i], i])
            # 如果不是被选中则说明是取消选中，那么就要删除数据
            else:
                # 首先用for循环所有数据
                for i in range(len(self.data_data)):
                    # 判断选择的开头是G还是K等，将其与车次信息的车次的首个相比是否相等
                    if self.data_data[i][0][0][0] == checkbox.text()[0]:
                        # print(self.data_data[i])
                        # 如果相等则删除这条数据
                        self.che_list.remove(self.data_data[i])
                        self.data_15_1.remove([self.data_15[i], i])
            # 2. 数据显示部分
            # 判断数据是否有数据，也可以理解为判断是否有checkbox被选中
            if len(self.che_list) > 0:
                # print([t[0] for t in self.data_15_1])
                # 如果有checkbox被选中则将选中的数据显示
                self.button_setcellwidget(len(self.che_list), [t[0] for t in self.data_15_1], [t[1] for t in self.data_15_1])
                for i in range(len(self.che_list)):
                    self.center_data_proces(self.che_list[i], n)
                    n += 1
            # 没有数据，即没有checkbox被选中
            else:
                # 没有数据则将之前爬到的所有数据进行显示
                self.button_setcellwidget(self.data_list, self.data_15)
                # print(self.data_data)
                for i in range(len(self.data_data)):
                    self.center_data_proces(self.data_data[i], n)
                    n += 1
        # 如果没有数据,并且车次数量等于按钮数量
        elif len(self.data_data) == self.data_list and len(self.data_data) == 0:
            self.wait_gui("当前无数据请\n请先查询您的车次!!!")
            # 将checkbox的状态回到初始状态,即将勾选去掉
            checkbox.setChecked(False)
        # 最后一种情况有数据但是车次数量不等于按钮数量,那么说明数据还没有爬取完
        else:
            self.wait_gui("请等待数据全部爬取完!!!")
            checkbox.setChecked(False)

    def lineedit_isnone(self, lineedit_list):
        lineedit_is = False
        for lineedit in lineedit_list:
            if len(lineedit.text()) == 0:
                lineedit.setPlaceholderText("此处不能为空")
                lineedit_is = True
        return lineedit_is

    def button_click(self):
        # 判断是否有wifi
        if self.wifi.wifi is False:
            # 没有wifi就弹出一个窗口，提示当前无网络
            self.wait_gui("请连接网络！！！")
            return
        lineedit_is = self.lineedit_isnone([self.lineedit, self.lineedit_1])
        if lineedit_is:
            return
        if self.dateEdit.date().day() < self.now_date_M_D[0] and \
                self.dateEdit.date().month() == self.now_date_M_D[1]:
            logging.info("日期选择有误！")
            self.wait_gui("请选择正确的日期！")
            return
        logging.info(self.lineedit.text() + self.lineedit_1.text() + self.dateEdit.text())
        # 查询按钮点击后首先就开始保存信息
        threading.Thread(target=self.data_save, args=([self.lineedit.text(), self.lineedit_1.text(), self.dateEdit.text()], )).start()
        # self.tableWidget.setCursor(Qt.WaitCursor)
        # 开始爬取车次信息传入参数none，获取车次总数和每个车次的备注，并且将无票的改为抢票所以返回总数，【‘预约’，‘抢票’...】
        self.data_list, self.data_15 = self.pa.pa()
        # 清除所有数据
        self.tableWidget.clearContents()
        # 将获取到的车次总数设置行数
        logging.info(f"共有{self.data_list}条数据")
        # 正式开始爬取车次信息,用线程来爬取在平凡的去更新数据就能达到一行一行的将数据显示出来防止数据爬取完后一次性将数据显示避免了等待时间
        threading.Thread(target=self.button_pa_data).start()
        self.button_setcellwidget(self.data_list, self.data_15)
        # if process.isAlive() == "false"
        # self.button_pa_data()

    def button_1_click(self):
        self.__loginGui()
        self.__login_state()

    def button_setcellwidget(self, rowcount, rowcount_list, button_setobjectname=None):
        """
        创建按钮，预约或者抢票的按钮
        :param rowcount: 按钮个数
        :param rowcount_list: 每个按钮的名字，是预约还是抢票
        :param button_setobjectname: 传入每个按钮的编号/排号
        :return: None
        """
        self.tableWidget.setRowCount(rowcount)
        # 有行数后就可以设置button了，每行最后一个数据都设置为button
        # 判断是否有button的编号
        if button_setobjectname is None:
            # 如果没有编号，则设置编号
            button_setobjectname = [i for i in range(rowcount)]
        # 创建按钮在每行数据的最后一列
        for i in range(rowcount):
            self.new_btn = QtWidgets.QCommandLinkButton(rowcount_list[i])
            # 将按钮的objectName编号设置一下，方便后面辨认是哪个按钮
            self.new_btn.setObjectName(f"{button_setobjectname[i]}")
            if rowcount_list[i] == "抢票":
                self.new_btn.setStyleSheet("color: red;font: 20px;")
            self.new_btn.clicked.connect(lambda: self.btn_college(self.new_btn.sender()))
            self.tableWidget.setCellWidget(i, 15, self.new_btn)

    def button_pa_data(self):
        # 设置行的参数，因为后面返回的是数据
        n = 0
        # 装爬取的数据
        self.data_data = []
        # 每爬取一行数据就传给data
        logging.info("开始爬取数据！")
        pa_data_pools = []
        for td in self.pa.tr:
            pool_data = self.pool.submit(self.pa.pa_data, td)
            pa_data_pools.append(pool_data)
        for data_pro in pa_data_pools:
            data = data_pro.result()
            logging.info(str(data)+"爬取成功")
            self.data_data.append(data)
            # 将传过来的data进行数据分析，显示
            # self.tableWidget.setCursor(Qt.ArrowCursor)
            self.center_data_proces(data, row=n)
            # 更新表格数据，这个很重要，没有这个数据也不能一行一行的显示
            self.tableWidget.viewport().update()
            n = n + 1
            time.sleep(0.25)
        # self.tableWidget.setCursor(Qt.ArrowCursor)
        logging.info("数据爬取完毕！！！")

    def center_data_proces(self, data, row):
        """
        将数据进行显示
        :param data: [[“车次信息”]，[“车票信息”], ["车票信息的序号"]]这样的二维数组
        :param row: 行数插入数据的行数
        :return: None
        """
        for i in range(15):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(row, i, item)
            # 设置表格位置数据居中
            self.tableWidget.item(row, i).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item = self.tableWidget.item(row, i)
            item.setText(data[0][i])

    def dataUi(self):
        # 设置表格的列数，这个是固定的所以可以直接创建
        self.tableWidget.setColumnCount(16)
        for i in range(16):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ESTrain"))
        self.tableWidget.setSortingEnabled(False)
        # 给头数据保存上去，标题
        for i in range(16):
            item = self.tableWidget.horizontalHeaderItem(i)
            item.setText(_translate("MainWindow", self.List[i]))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(__sortingEnabled)

    def btn_college(self, sender):
        # 将每个浏览器的控制参数添加到chrome_count中方便结束后关闭全部浏览器
        try:
            self.button_sender_data = self.data_data[int(sender.objectName())]
        except IndexError:
            self.wait_gui("还未爬到此处！")
            return
        self.chrome_count.append(self.pa.browser)
        # print(sender.text())
        # 判断乘客信息是否爬取完成了
        if self.logingui.button_close_T_F and len(self.logingui.tr_list) > 0 or self.logingui.button_close_T_F and self.chengke_data_pa_is is False:
            # 将车票信息和车票的编号传入data_heard_process_1进行处理，将有无票的进行处理，返回一个二维数组
            self.piao_money = data_proces.data_heard_process_1([self.button_sender_data[1], self.data_data[int(sender.objectName())][2]])
            # print(self.data_data[int(sender.objectName())][0], self.data_data[int(sender.objectName())][1])
            # 传入四个参数data_list是点击的车的信息如:车次，出发，到站等的信息是数组 data_list_heald是票的信息二维列表 chengke_data是爬取到的乘车信息是二维数组， date日期
            qw = qwidget.Ui_QDialog(data_list=self.button_sender_data[0], data_list_heald=self.piao_money, date=self.dateEdit.date()
                                    , chengke_data=self.logingui.tr_list)
            qw.qdialog.exec_()
            logging.info("已将数据传进买票")
            # 判断是否选了乘车人，并按了确定键
            if len(qw.zw) > 0:
                # print(sender.text())
                # 开始购票或者抢票
                # print(qw.zw, qw.ck, int(sender.objectName()), self.piao_money)
                threading.Thread(target=self.pa.update_login, args=(qw.zw, qw.ck, int(sender.objectName()), self.piao_money), daemon=True).start()
                # threading.Thread(target=self.pa.login, args=(qw.zw, qw.ck, int(sender.objectName())), daemon=True).start()
                # 上面那个浏览器抢票去了，重新创建一个浏览器
                self.pa = selen.paData(chaxun_list=True)
                # 将这个新的浏览器执行前面的搜索内容
                threading.Thread(target=self.pa.browser_pa, daemon=True).start()
        # 如果没有乘车人则说明乘客信息还在爬取当中
        else:
            # 判断登入页面是否按了确定按钮
            if self.logingui.button_close_T_F:
                self.wait_gui("乘客信息爬取中,请等待")
            else:
                if self.logingui.button_event_text is not None:
                    button = self.wait_gui(self.logingui.button_event_text, True)
                # 如果没有按确定按钮就提示其没有登入
                else:
                    button = self.wait_gui(wait_str="未输入账号和密码！", event_bool=True)
                # 判断是否按了登入按钮，如果按了则显示登入窗口
                if button:
                    self.__loginGui()

    def wait_gui(self, wait_str, event_bool=False, *args, **kwargs):
        w = wait.Wait(wait_str, event_bool, *args, **kwargs)
        w.wait_window.exec_()
        return w.button_T_F

    def data_save(self, list_1):
        """
        以json数据形式保存数据
        :param list_1:[出发地，目的地，日期]
        :return: none
        """
        logingui_process = data_proces.login_gui_data_proces(self.logingui.list)
        self.datasave.login_gui_data_save(logingui_process)
        search_process = data_proces.search_gui_data_process(list_1)
        self.datasave.search_gui_data_save(search_process)
        self.datasave.write()
        logging.info("数据保存成功！！！")

    def wifi_panduan(self):
        while True:
            # print(self.wifi.wifi)
            if self.wifi.wifi:
                threading.Thread(target=self.pa.browser_pa, daemon=True).start()
                break
            time.sleep(0.2)

    def login_wifi_panduan(self):
        while True:
            if self.wifi.wifi:
                self.logging_pa = threading.Thread(target=self.logingui.init_login, daemon=True)
                self.logging_pa.start()
                break
            time.sleep(0.2)

    def wifi_F(self):
        while True:
            if self.wifi.wifi:
                self.label_2.setText("")
                break
            else:
                self.label_2.setText("温馨提示：您还没有连接网络，请连接网络后在使用！！！")
            time.sleep(0.2)


if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
        MainWindow = QtWidgets.QMainWindow()  # 创建一个QMainWindow，用来装载你需要的各种组件、控件
        ui = Ui_MainWindow()  # ui是Ui_MainWindow()类的实例化对象
        ui.setupUi(MainWindow)  # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
        MainWindow.show()  # 执行QMainWindow的show()方法，显示这个QMainWindow
        app.exec_()
    except:
        pass
    subprocess.call('taskkill /im chrome.exe /F', creationflags=0x08000000)
    subprocess.call('taskkill /im chromedriver.exe /F', creationflags=0x08000000)
