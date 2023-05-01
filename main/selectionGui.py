import calendar
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from setting import *

week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]


class SelectionGui(object):
    def __init__(self, data_list, date, chengke_data):
        """
        对乘客信息进行处理并选座
        :param data_list: 车次信息如['G1759', '萍乡北\n醴陵东', '08:18\n08:31', '00:13\n当日到达', '42元\n余票候补',...]
        :param date: 日期 如2023-04-29
        :param chengke_data: 乘客信息二维列表如[['1', '成人票', '二等座票价13.5元剩候补', 'name', '中国居民身份证', '身份证号码']]
        """
        self.x = 0
        self.n = []
        self.zw = []
        title = ["序号", "席别", "票种", "姓名", "证件类型", "证件号码"]
        self.data = chengke_data
        self.qdialog = QtWidgets.QDialog()
        # self.qwidget = QtWidgets.QWidget(self.qdialog)
        self.qdialog.setFixedSize(1000, 500)
        self.qdialog.setWindowIcon(QtGui.QIcon(TU_BIAO_ICON_PATH))
        self.qdialog.setWindowTitle("请核对以下信息")
        s = ["开", "到"]
        for i in range(0, 2):
            self.lable = QtWidgets.QLabel(self.qdialog)
            self.lable.setGeometry(QtCore.QRect(350 + 100+i*340, 10, 200, 100))
            self.lable.setObjectName(f"{i}")
            self.lable.setText(data_list[1].split("\n")[i])
            self.lable.setFont(QtGui.QFont("宋体", 15))
            self.lable = QtWidgets.QLabel(self.qdialog)
            self.lable.setGeometry(QtCore.QRect(450 + 100+i*340, 15, 200, 100))
            self.lable.setObjectName(f"{i+2}")
            self.lable.setText(data_list[2].split("\n")[i]+s[i])
            self.lable.setFont(QtGui.QFont("楷体", 13, 100))
        self.lable1 = QtWidgets.QLabel(self.qdialog)
        self.lable1.setPixmap(QtGui.QPixmap("../images/箭头.png"))
        self.lable1.setGeometry(QtCore.QRect(660, 25, 200, 70))
        self.label3 = QtWidgets.QLabel(self.qdialog)
        self.label3.setGeometry(QtCore.QRect(20, 10, 220, 100))
        self.label3.setText(date.toString("yyyy-MM-dd"))
        self.label3.setFont(QtGui.QFont("楷体", 20, 100))
        self.label3.setStyleSheet("color:rgb(255,0,0)")
        self.label4 = QtWidgets.QLabel(self.qdialog)
        self.label4.setGeometry(QtCore.QRect(340, 10, 120, 100))
        self.label4.setText(data_list[0])
        self.label4.setFont(QtGui.QFont("楷体", 20, 100))
        self.label5 = QtWidgets.QLabel(self.qdialog)
        self.label5.setGeometry(QtCore.QRect(230, 10, 120, 100))
        self.label5.setText("("+week_list[calendar.weekday(date.year(), date.month(), date.day())]+")")
        self.label5.setFont(QtGui.QFont("楷体", 14, 50))
        self.tableWidget = QtWidgets.QTableWidget(self.qdialog)
        self.tableWidget.setGeometry(QtCore.QRect(50, 100, 900, 150))
        self.tableWidget.setColumnCount(6)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setShowGrid(False)
        # 信息的宽度
        size = [110, 110, 110, 110, 230, 228]
        # 设置显示的行数
        self.tableWidget.setRowCount(len(self.data))
        for i in range(6):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(i, item)
            item = self.tableWidget.horizontalHeaderItem(i)
            item.setText(title[i])
        for i in range(6):
            self.tableWidget.setColumnWidth(i, size[i])
        for i in range(len(self.data)):
            for j in range(6):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(i, j, item)
                self.tableWidget.item(i, j).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item = self.tableWidget.item(i, j)
                item.setText(self.data[i][j])
        a = ["窗", "过道"]
        if chengke_data[0][2].split("票价")[0] == "二等座" or chengke_data[0][2].split("票价")[0] == "二等座包座":
            button_int = [3, 4, 5, 7, 8]
            zuowei = ["A", "B", "C", "D", "F"]
        elif chengke_data[0][2].split("票价")[0] == "一等座":
            button_int = [3, 5, 7, 8]
            zuowei = ["A", "C", "D", "F"]
        elif chengke_data[0][2].split("票价")[0] == "商务座" or chengke_data[0][2].split("票价")[0] == "特等座":
            button_int = [3, 5, 8]
            zuowei = ["A", "C", "F"]
        else:
            button_int = []
            zuowei = []
        # 设置座位选择的按钮A，B等
        try:
            remaining_tickets = int(chengke_data[0][2].split("剩")[-1])
        except ValueError:
            remaining_tickets = 6
        if len(chengke_data) > 1:
            for i in range(1, len(chengke_data)):
                if chengke_data[i][2] != chengke_data[i-1][2]:
                    remaining_tickets = 4
        if len(button_int) > 0 and remaining_tickets >= 5:
            self.label6 = QtWidgets.QLabel(self.qdialog)
            self.label6.setText("*如果本次列车剩余席位无法满足您的选座需求,系统将自动为您分配席位。")
            self.label6.setGeometry(QtCore.QRect(50, 265, 900, 20))
            self.tableWidget1 = QtWidgets.QTableWidget(self.qdialog)
            self.tableWidget1.setGeometry(QtCore.QRect(50, 300, 900, 45))
            self.tableWidget1.verticalHeader().setVisible(False)
            self.tableWidget1.setShowGrid(False)
            self.tableWidget1.horizontalHeader().setVisible(False)
            self.tableWidget1.setColumnCount(11)
            self.tableWidget1.setRowCount(1)
            self.tableWidget1.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
            self.tableWidget1.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            for i in range(11):
                self.tableWidget1.setColumnWidth(i, 80)
            for i in range(len(button_int)):
                button = QtWidgets.QPushButton(self.qdialog)
                button.setText(zuowei[i])
                button.setObjectName(f"{zuowei[i]}")
                button.clicked.connect(lambda: self.button_click(button.sender()))
                self.tableWidget1.setCellWidget(0, button_int[i], button)
            for i in [2, 6, 9]:
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget1.setItem(0, i, item)
                self.tableWidget1.item(0, i).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                item = self.tableWidget1.item(0, i)
                item.setText(a[i % 5 % 2])
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget1.setItem(0, 0, item)
            self.tableWidget1.item(0, 0).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            item = self.tableWidget1.item(0, 0)
            item.setText("请选座:")
        else:
            self.lable9 = QtWidgets.QLabel(self.qdialog)
            self.lable9.setGeometry(QtCore.QRect(50, 300, 900, 45))
            self.lable9.setText("*系统将随机为您申请席位，暂不支持自选席位。")
            self.lable9.setStyleSheet("color: #4987c6")
            self.n = self.data
        self.label7 = QtWidgets.QLabel(self.qdialog)
        self.label7.setGeometry(QtCore.QRect(50, 345, 600, 50))
        self.label7.setText(f"本次列车，二等座余票{self.data[0][2].split('剩')[-1]}")
        self.label8 = QtWidgets.QLabel(self.qdialog)
        self.label8.setGeometry(QtCore.QRect(400, 345, 200, 50))
        self.label8.setText("")
        self.label8.setStyleSheet("color:rgb(255,0,0);")
        self.button_close = QtWidgets.QPushButton(self.qdialog)
        self.button_close.setGeometry(QtCore.QRect(500, 400, 150, 75))
        self.button_close.setText("确定")
        self.button_close.setFont(QtGui.QFont("楷体", 13))
        self.button_close.setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(255, 0, 0);")
        self.button_close.setCursor(Qt.ClosedHandCursor)
        self.button_close.clicked.connect(self.button_c)
        self.button_quit = QtWidgets.QPushButton(self.qdialog)
        self.button_quit.setGeometry(QtCore.QRect(300, 400, 150, 75))
        self.button_quit.setText("返回修改")
        self.button_quit.setFont(QtGui.QFont("楷体", 13))
        self.button_quit.clicked.connect(self.button_q)

    def button_click(self, button_sender):
        self.n.append(button_sender)
        try:
            for i in range(len(self.n)-1):
                if button_sender == self.n[i]:
                    self.n[i].setStyleSheet("color: none; background-color: none;")
                    self.n.pop(i)
                    self.n[-1].setStyleSheet("color: none; background-color: none;")
                    self.n.pop(-1)
        except:
            pass
        if len(self.n) > len(self.data):
            self.n.pop(-1)
        # try:
        #     self.n[-len(self.data)-1].setStyleSheet("color: none; background-color: none;")
        # except:
        #     pass
        try:
            self.n[-1].setStyleSheet("color: rgb(255, 255, 255); background-color: rgb(24, 200, 224);")
        except:
            pass

    def button_c(self):
        zw = []
        if len(self.n) < len(self.data):
            self.label8.setText(f"请选座{len(self.data)}个座位！")
        else:
            try:
                for i in self.n:
                    zw.append(i.objectName())
                    # print(i.objectName())
            except:
                zw = "G"
            self.zw = zw
            self.qdialog.close()

    def button_q(self):
        self.qdialog.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
    MainWindow = QtWidgets.QMainWindow()  # 创建一个QMainWindow，用来装载你需要的各种组件、控件
    ui = SelectionGui()  # ui是Ui_MainWindow()类的实例化对象  # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    ui.qdialog.show()  # 执行QMainWindow的show()方法，显示这个QMainWindow
    app.exec_()
