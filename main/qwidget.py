from PyQt5 import QtCore, QtGui, QtWidgets
import logging
import selectionGui
from PyQt5.QtCore import Qt
from setting import *
from multiprocessing.dummy import Process
import data_proces
import wait
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")


class Ui_QDialog(object):
    def __init__(self, data_list, data_list_heald, date, chengke_data):
        """
        选择乘车人即车票等
        :param data_list: 车次信息如['G1759', '萍乡北\n醴陵东', '08:18\n08:31', '00:13\n当日到达', '42元\n余票候补', ...
        :param data_list_heald: 车票信息和车票位置如[['商务座票价42元剩候补', '一等座票价22.5元剩候补', '二等座票价13.5元剩候补'], [2, 3, 4]]
        :param date: 如 2023-04-29
        :param chengke_data: 乘车人信息如[['name', '中国居民身份证', '身份证号码', 'phone'], ...]
        """
        # a = open("./main/chickenhearted.dat", 'r').read()
        # print(''.join([chr(i) for i in [int(b, 2) for b in a.split(' ')]]))
        self.v = 0
        self.zw = []
        self.ck = []
        self.chengke_data = chengke_data
        self.n = 0
        self.combobox_list = []
        data_title = ["票种", "席别", "姓名", "证件类型", "证件号码"]
        self.ticket_type = [["成人票", "儿童票", "学生票", "残军票"], data_list_heald[0]]
        self.qdialog = QtWidgets.QDialog()
        self.qdialog.resize(800, 650)
        self.qdialog.setWindowIcon(QtGui.QIcon(TU_BIAO_ICON_PATH))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.data_list = data_list
        self.cfd_date = self.data_list[1].split("\n")
        self.mdd_date = [self.data_list[2].split("\n")[0]+"开", self.data_list[2].split("\n")[1]+"到"]
        for i in range(0, 2):
            self.lable = QtWidgets.QLabel(self.qdialog)
            self.lable.setGeometry(QtCore.QRect(100+i*400, 30, 200, 100))
            self.lable.setObjectName(f"{i}")
            self.lable.setText(self.cfd_date[i])
            self.lable.setFont(QtGui.QFont("宋体", 30))
            self.lable = QtWidgets.QLabel(self.qdialog)
            self.lable.setGeometry(QtCore.QRect(100+i*400, 100, 200, 100))
            self.lable.setObjectName(f"{i+2}")
            self.lable.setText(self.mdd_date[i])
            self.lable.setFont(QtGui.QFont("宋体", 20))
        self.lable1 = QtWidgets.QLabel(self.qdialog)
        self.lable1.setPixmap(QtGui.QPixmap("../images/箭头.png"))
        self.lable1.setGeometry(QtCore.QRect(320, 50, 200, 70))
        self.lable2 = QtWidgets.QLabel(self.qdialog)
        self.lable2.setText("历时"+self.data_list[3].split("\n")[0]+"分钟")
        self.lable2.setGeometry(QtCore.QRect(300, 100, 200, 100))
        self.lable2.setFont(QtGui.QFont("宋体", 12))
        self.lable3 = QtWidgets.QLabel(self.qdialog)
        self.lable3.setText(date.toString("yyyy-MM-dd"))
        self.lable3.setGeometry(QtCore.QRect(300, 0, 200, 70))
        self.lable3.setFont(QtGui.QFont("宋体", 20))
        self.tableWidget = QtWidgets.QTableWidget(self.qdialog)
        self.tableWidget.setGeometry(QtCore.QRect(0, 250, 800, 300))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText("1")
        for i in range(5):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)
            item = self.tableWidget.horizontalHeaderItem(i)
            item.setText(data_title[i])
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 220)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setColumnWidth(3, 160)
        self.tableWidget.setColumnWidth(4, 200)
        if len(self.chengke_data) == 0:
            self.lineedit_list = []
            for i in range(4):
                self.lineedit = QtWidgets.QLineEdit(self.qdialog)
                self.lineedit.setGeometry(QtCore.QRect(0, 0, 0, 0))
                self.lineedit.setObjectName(str(i))
                self.lineedit_list.append(self.lineedit)
                self.lineedit.setPlaceholderText("姓名")
            self.button_1 = QtWidgets.QPushButton(self.qdialog)
            self.button_1.setGeometry(QtCore.QRect(0, 0, 0, 0))
            self.button_1.setText("确定")
            self.button_1.clicked.connect(self.button_1_click)
            self.lable4 = QtWidgets.QLabel(self.qdialog)
            self.lable4.setGeometry(QtCore.QRect(50, 200, 150, 50))
            self.lable4.setText("乘车人个数:")
            self.lable4.setFont(font)
            self.combobox_2 = QtWidgets.QComboBox(self.qdialog)
            self.combobox_2.setGeometry(175, 200, 50, 50)
            self.combobox_2.addItems(["1", "2", "3", "4"])
            self.chengke_count()
            self.combobox_2.currentTextChanged.connect(self.chengke_count)
        else:
            for i in range(len(self.chengke_data)):
                self.checkbox = QtWidgets.QCheckBox(self.qdialog)
                self.checkbox.setGeometry(QtCore.QRect(100+i*100, 200, 150, 50))
                self.checkbox.setObjectName(str(i))
                self.checkbox.setText(f"{self.chengke_data[i][0]}")
                self.checkbox.setFont(QtGui.QFont("宋体", 10))
                self.checkbox.clicked.connect(lambda: self.monitor(self.checkbox.sender()))
        self.qdialog.setWindowTitle(self.data_list[0])
        # 设置窗口的属性为ApplicationModal模态，用户只有关闭弹窗后，才能关闭主界面
        # dialog.setWindowModality(Qt.ApplicationModal)
        self.button = QtWidgets.QPushButton(self.qdialog)
        self.button.setGeometry(QtCore.QRect(350, 575, 100, 50))
        self.button.setText("确定")
        self.button.setFont(QtGui.QFont("宋体", 15))
        self.button.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(89, 175, 191);")
        self.button.clicked.connect(lambda: self.sure_message(date))

    def chengke_count(self):
        for i in range(int(self.combobox_2.currentText())):
            self.lineedit_list[i].setGeometry(QtCore.QRect(250+i*110, 200, 100, 50))
            self.button_1.setGeometry(QtCore.QRect(360+i*110, 200, 100, 50))
        else:
            if int(self.combobox_2.currentText()) < self.v:
                for j in range(int(self.combobox_2.currentText()), self.v):
                    self.lineedit_list[j].setGeometry(QtCore.QRect(0, 0, 0, 0))
            if int(self.combobox_2.currentText()) == 0:
                self.button_1.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.v = int(self.combobox_2.currentText())

    def button_1_click(self):
        self.n = 0
        self.tableWidget.clearContents()
        self.chengke_data = []
        self.combobox_list = []
        for i in range(self.v):
            chengke_name = self.lineedit_list[i].text()
            if len(chengke_name) == 0:
                self.lineedit_list[i].setPlaceholderText("不能为空")
                return
            self.chengke = [chengke_name, '中国居民身份证', '此空不填', '此空不填']
            self.chengke_data.append(self.chengke)
            self.tablewidget_add_item(i)

    def monitor(self, checkbox):
        # 判断是勾选还是取消勾选
        if self.checkbox.sender().isChecked():
            # 如果是勾选则加1，统计点击的个数
            self.tablewidget_add_item(int(checkbox.objectName()))
            logging.info(f"增加了{checkbox.text()}这一行")
        # 取消勾选，也就意味着需要删除某一行
        else:
            self.tablewidget_pop_item(checkbox.text())
            # self.tableWidget.setRowCount(self.n)

    def tablewidget_add_item(self, row):
        self.n = self.n + 1
        # 设置table的行数
        self.tableWidget.setRowCount(self.n)
        # 创建可以下拉选择的按钮combobox
        self.combobox = QtWidgets.QComboBox(self.qdialog)
        # 设置objectName方便后面分辨机调用
        self.combobox.setObjectName(f"combobox{self.n}")
        # 用for语句循环将信息传入下拉的信息
        for j in range(len(self.ticket_type[0])):
            self.combobox.addItem(self.ticket_type[0][j])
            # 创建完成后就将其设置在table里面显示
            self.tableWidget.setCellWidget(self.n - 1, 0, self.combobox)
        # 在创建一个同理
        self.combobox1 = QtWidgets.QComboBox(self.qdialog)
        self.combobox1.setObjectName(f"combobox1{self.n}")
        # 将两个combobox添加到self.combobox_list方便后面删除
        self.combobox_list.append([self.combobox, self.combobox1])
        for j in range(len(self.ticket_type[1])):
            self.combobox1.addItem(self.ticket_type[1][len(self.ticket_type[1]) - j - 1])
            self.tableWidget.setCellWidget(self.n - 1, 1, self.combobox1)
        # 用for语句来创建后面三个信息，因为后面的不用combobox了
        for i in [0, 1, 2]:
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setItem(self.n - 1, i + 2, item)
            item = self.tableWidget.item(self.n - 1, i + 2)
            item.setText(self.chengke_data[row][i])
            # 设置文字居中
            self.tableWidget.item(self.n - 1, i + 2).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    def tablewidget_pop_item(self, text):
        # 循环行数
        for i in range(self.n):
            # 如果哪行的乘客姓名的与取消勾选的姓名一样就将这行删除
            if self.tableWidget.item(i, 2).text() == text:
                # 删除名字相同的行
                self.tableWidget.removeRow(i)
                self.combobox_list.pop(i)
                logging.info(f"删除了{text}这一行")
                # 删除了就跳出，后面不可能在有一样的了，节省资源
                break
        # 把那行删除了别忘了把行数减少
        self.n = self.n - 1

    def sure_message(self, date):
        # 判断是否有行数，没有就弹出窗口提醒
        if self.n == 0:
            w = wait.Wait("请选择乘车人！！！")
            w.wait_window.exec_()
            return
        # 乘客信息的集合列表
        chengke_data_list_1 = []
        # 循环乘客的行数
        for i in range(self.n):
            chengke_data_list = []
            # 将乘客的序号设置为从1开始并添加到列表
            chengke_data_list.append(f"{i+1}")
            for j in range(5):
                if j < 2:
                    # 将两个combobox添加到列表
                    chegnke_data = self.combobox_list[i][j].currentText()
                else:
                    chegnke_data = self.tableWidget.item(i, j).text()
                # 将所有的信息保存到列表
                chengke_data_list.append(chegnke_data)
            logging.info(f"{i+1}乘客信息保存成功!")
            # 在将保存信息的列表传入总列表，打包
            chengke_data_list_1.append(chengke_data_list)
    #     Process(target=self.show_selection, args=(date, chengke_data_list_1)).start()
    #
    # def show_selection(self, date, chengke_data_list_1):
        selection_gui = selectionGui.SelectionGui(self.data_list, date, chengke_data_list_1)
        selection_gui.qdialog.exec_()
        # 获取选择的座位号
        self.zw = selection_gui.zw
        # 获取乘客信息的座位，票名， 姓名
        self.ck = [[i[j] for j in range(1, 4)] for i in chengke_data_list_1]
        if len(self.zw) > 0:
            self.qdialog.close()



if __name__ == '__main__':

    qwidget = Ui_QDialog()
    qwidget.qdialog.exec_()
    pass

