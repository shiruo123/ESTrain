import logging
import subprocess
import sys
import time
import threading
from PyQt5.QtCore import Qt
import logging
from mysql import *
from PyQt5 import QtCore, QtGui, QtWidgets
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import DeleteRowsEvent, UpdateRowsEvent, WriteRowsEvent
import ESTRainClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")


class Mysql(MysqlSetData, MysqlGetData, MysqlUpdateDate, MysqlDeleteData):
    def __init__(self):
        super(Mysql, self).__init__()


class ShowTools(QtWidgets.QMainWindow):
    def __init__(self):
        self.head = ["账号", "密码", "邮箱", "出发地", "目的地", "日期", "出发时间\n到达时间", "车次", "买票人\n姓名", "座位号", "座位类型", "乘车类型", "当前状态",
                     "Error", "", ""]
        super(ShowTools, self).__init__()
        self.mysql = Mysql()
        self.__init_setting()

    def __init_setting(self):
        self.first_finish = False
        self.all_data_list = []
        self.state_error_data = []
        self.i_trainid = []
        self.table_row = 0
        self.is_data_show = False
        self.write_list = []

    def setupui(self):
        self.desktop = QtWidgets.QApplication.desktop()
        self.resize(self.desktop.width(), self.desktop.height() - 90)
        self.table_widget = QtWidgets.QTableWidget(self)
        self.table_widget.setGeometry(QtCore.QRect(0, 80, int(self.desktop.width()), int(self.desktop.height()) - 170))
        self.table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_widget.verticalHeader().setDefaultSectionSize(50)
        # 设置表格不可编辑
        # self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_widget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # self.table_widget.itemClicked.connect(self.cell_data_update)
        self.table_widget.itemChanged.connect(self.cell_data_update)
        self.table_widget.setColumnCount(14)
        for i in range(14):
            item = QtWidgets.QTableWidgetItem()
            item.setText(self.head[i])
            self.table_widget.setHorizontalHeaderItem(i, item)
        self.table_widget.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.train_all_ids = self.train_ids()
        self.menubar = QtWidgets.QMenuBar(self)
        self.main_menubar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1920, 30))
        self.menubar.setObjectName("menubar")
        self.window().setMenuBar(self.menubar)
        threading.Thread(target=self.show_data, args=(self.train_all_ids,)).start()
        threading.Thread(target=self.update_data, daemon=True).start()

    def cell_data_update(self, Item=None):
        # 如果单元格对象为空
        if Item is None:
            return
        else:
            row = Item.row()  # 获取行数
            col = Item.column()  # 获取列数 注意是column而不是col哦
            text = Item.text()  # 获取内容
            # self.mysql.update()


    def main_menubar(self):
        menu_file = self.menubar.addMenu("文件")
        menu_file.addAction("新建")
        menu_file.triggered.connect(lambda: self.menubar_connect(menu_file))
        save = QtWidgets.QAction('保存', self)
        save.setShortcut('Ctrl + s')
        menu_file.addAction(save)
        save.triggered.connect(lambda: self.menubar_connect(save))
        menu_tool = self.menubar.addMenu("工具")
        menu_window = self.menubar.addMenu("数据管理")
        menu_window.addAction("刷新")
        menu_window.addAction("增加数据(购票)")
        menu_window.triggered.connect(lambda: self.menubar_connect(menu_window))
        menu_help = self.menubar.addMenu("帮助")

    def menubar_connect(self, sender):
        if sender.sender().text() == "刷新":
            self.__init_setting()
            self.menu_window_updata()
        elif sender.sender().text() == "增加数据(购票)":
            self.ui = ESTRainClient.Ui_MainWindow()  # ui是Ui_MainWindow()类的实例化对象
            self.ui.setupUi()  # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
            self.ui.MainWindow.show()  # 执行QMainWindow的show()方法，显示这个QMainWindow

    def menu_window_updata(self):
        threading.Thread(target=self.show_data, args=(self.train_all_ids,)).start()

    def show_data(self, train_ids):
        for i, train_id in enumerate(train_ids):
            show_data = threading.Thread(target=self.__show_to_data, args=(i, train_id))
            show_data.start()
            time.sleep(0.1)
        else:
            show_data.join()
            for i, d in enumerate(self.i_trainid):
                if i != d[0]:
                    for j, jd in enumerate(self.i_trainid):
                        if i == jd[0]:
                            t, n = self.i_trainid[j], self.all_data_list[j]
                            self.i_trainid[j], self.all_data_list[j] = self.i_trainid[i], self.all_data_list[i]
                            self.i_trainid[i], self.all_data_list[i] = t, n
            with open("./data.txt", "w", encoding="utf-8") as fp:
                for i, data in enumerate(self.all_data_list):
                    fp.write(str(data[6]) + f" {self.i_trainid[i][0]}" + "\n")
            fp.close()
            self.is_data_show = True

    def train_ids(self):
        train_ids = self.mysql.get_all_data()
        logging.info(train_ids)
        return train_ids

    def __show_to_data(self, i, train_id, **kwargs):
        all_data = self.row_all_data(train_id)
        if kwargs.get("show_data"):
            self.i_trainid.insert(i, [i, train_id])
            self.all_data_list.insert(i, all_data)
        else:
            self.i_trainid.append([i, train_id])
            self.all_data_list.append(all_data)
        logging.info("all_data" + str(all_data))
        self.show_row_data(i, all_data, update=kwargs.get("show_data"))

    def update_start(self):
        while True:
            train_ids = self.train_ids()
            for i, train_id in enumerate(train_ids):
                all_data = self.row_all_data(train_id)
                try:
                    all_data1 = self.all_data_list[i]
                except IndexError:
                    all_data1 = "None"
                if all_data != all_data1:
                    try:
                        self.all_data_list[i] = all_data
                    except IndexError:
                        self.all_data_list.append(all_data)
                    logging.info(f"row: {str(i)}")
                    self.show_row_data(i, all_data)
                    print("已修改更改的内容！")
            time.sleep(3)

    def show_row_data(self, i, all_data, **kwargs):
        if kwargs.get("update"):
            pass
        else:
            self.table_row += 1
        self.table_widget.setRowCount(self.table_row)
        print(all_data)
        print(len(all_data))
        for j in range(8):
            self.set_table_widget_item(i, j, all_data[j])
        for j in range(12, 13):
            self.set_table_widget_item(i, j, all_data[j - 3])
        user_name_list = all_data[8]
        if len(user_name_list) == 1:
            print("user_name_list:", user_name_list)
            user_name = user_name_list[0]
        else:
            user_name = ["", "", "", ""]
            first = True
            for user_name_id in user_name_list:
                logging.info(user_name_id)
                for k in range(4):
                    if first:
                        user_name[k] = user_name[k] + user_name_id[k]
                    else:
                        user_name[k] = user_name[k] + "\n" + user_name_id[k]
                else:
                    first = False
            self.table_widget.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        self.user_login_data(user_name, i)
        self.table_widget.viewport().update()

    @staticmethod
    def row_all_data(train_id, **kwargs):
        if kwargs.get("mysql"):
            mysql = kwargs.get("mysql")
        else:
            mysql = MysqlGetData()
        all_data = []
        user_station_id = mysql.get_user_station_id(train_id)[0]
        all_data.extend(mysql.get_user(user_station_id[0]))
        all_data.extend(mysql.get_station(user_station_id[1]))
        all_data.extend(mysql.get_train(train_id, "Train, TrainDate"))
        username_logindata_ids = mysql.get_username_logindata_id(train_id)
        user_name_list = []
        for username_logindata_id in username_logindata_ids:
            user_name_list.append(mysql.get_user_name(username_logindata_id[0], "Seat"))
        all_data.append(user_name_list)
        all_data.extend(mysql.get_train(train_id, "State, Error"))
        if kwargs.get("row"):
            all_data.append(kwargs.get("row"))
        logging.info(all_data)
        return all_data

    def user_login_data(self, user_name, i):
        print(user_name, i)
        user_name = list(user_name)
        user_name[0], user_name[3] = user_name[3], user_name[0]
        for j in range(8, 12):
            self.set_table_widget_item(i, j, user_name[j - 8])
        self.table_widget.viewport().update()

    def set_table_widget_item(self, row, count, text):
        time.sleep(0.005)
        item = QtWidgets.QTableWidgetItem()
        item.setText(text)
        self.table_widget.setItem(row, count, item)
        try:
            self.table_widget.item(row, count).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        except AttributeError:
            self.set_table_widget_item(row, count, text)

    def show_all_data_list(self):
        for i, all_data in enumerate(self.all_data_list):
            self.show_row_data(i, all_data)

    def update_data(self):
        # 监听数据库
        mysql_connect = {
            "host": "119.29.244.36",
            "port": 3306,
            "user": "youthrefuel",
            "passwd": "dsq171007"
        }
        stream = BinLogStreamReader(
            connection_settings=mysql_connect,
            server_id=3,  # slave标识，唯一
            blocking=True,  # 阻塞等待后续事件
            resume_stream=True,  # True为从最新位置读取, 默认False
            # 设定只监控写操作：增、删、改
            only_events=[
                DeleteRowsEvent,
                UpdateRowsEvent,
                WriteRowsEvent
            ],
        )
        for event in stream:
            # update_data = str(event.dump())  # 打印所有信息
            # for data in update_data:
            #     print(data)
            # print(event)
            for row in event.rows:
                # print(row)
                data = {"schema": event.schema, "table": event.table}  # 取出库和表的信息
                if isinstance(event, DeleteRowsEvent):
                    data["action"] = "DELETE"  # 记录操作类型
                    data["data"] = row['values']  # 添加数据
                    self.__delete(data)
                elif isinstance(event, UpdateRowsEvent):
                    data['action'] = "UPDATE"
                    data['data'] = row['after_values']
                    threading.Thread(target=self.__update, args=(data,)).start()
                elif isinstance(event, WriteRowsEvent):
                    data['action'] = "INSERT"
                    data['data'] = row['values']
                    threading.Thread(target=self.__write, args=(data,)).start()

    def __delete(self, data):
        if data.get("table") == "train":
            pass

    def __update(self, data):
        if data.get("table") == "train":
            for i, train_id in self.i_trainid:
                if int(train_id[0]) == int(data.get("data").get("ID")):
                    all_data = self.row_all_data(train_id)
                    for j, new_data in enumerate(all_data):
                        print(new_data, self.all_data_list[i][j])
                        if new_data != self.all_data_list[i][j]:
                            print("new_data", new_data)
                            self.all_data_list[i][j] = new_data
                            if j < 8:
                                self.set_table_widget_item(i, j, new_data)
                                self.item_color(i, j)
                            elif j == 8:
                                pass
                            else:
                                self.set_table_widget_item(i, j + 3, new_data)
                                threading.Thread(target=self.item_color, args=(i, j + 3)).start()

    def item_color(self, i, j):
        logging.info("item_color:" + str(i) + str(j))
        for k in range(1, 101):
            try:
                time.sleep(0.0005)
                self.table_widget.item(i, j).setBackground(QtGui.QBrush(QtGui.QColor(55 + 2 * k, 55 + 2 * k, 255)))
                self.table_widget.viewport().update()
            except Exception as e:
                continue

    def __write(self, data):
        if self.is_data_show:
            if len(self.write_list) != 0:
                for i in self.write_list:
                    self.write(i)
                    self.write_list.remove(i)
        else:
            self.write_list.append(data)
            return
        self.write(data)

    def write(self, data):
        time.sleep(0.3)
        if data.get("table") == "train":
            logging.info("write train:" + str(data))
            self.__show_to_data(len(self.i_trainid), (data.get("data").get("ID"),))
            self.train_all_ids.append(data.get("data").get("ID"))
            for n in range(14):
                threading.Thread(target=self.item_color, args=(len(self.i_trainid) - 1, n)).start()
        elif data.get("table") == "user_name":
            time.sleep(1)
            logging.info("write user_name:" + str(data))
            for i, train_id in self.i_trainid:
                print(train_id, data.get("data").get("TrainID"))
                if int(train_id[0]) == int(data.get("data").get("TrainID")):
                    all_data = self.row_all_data(train_id)
                    self.show_row_data(i, all_data, update=True)

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, '提示',
                                               "是否要关闭所有窗口?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            subprocess.call('taskkill /im chrome.exe /F', creationflags=0x08000000)
            subprocess.call('taskkill /im chromedriver.exe /F', creationflags=0x08000000)
            event.accept()
            sys.exit(0)  # 退出程序
        else:
            event.ignore()


class DataGetUpdate(object):
    pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
    ui = ShowTools()  # ui是Ui_MainWindow()类的实例化对象
    ui.setupui()
    ui.show()
    # ui.setupUi(MainWindow)  # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    # threading.Thread(target=ui.update_start, daemon=True).start()
    # print(ui.combobox_list)
    app.exec_()
