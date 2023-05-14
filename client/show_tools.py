import logging
import sys
import time
import threading
from PyQt5.QtCore import Qt
import logging
from mysql import *
from PyQt5 import QtCore, QtGui, QtWidgets

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")


class ShowTools(MysqlSetData, MysqlGetData, MysqlUpdateDate, MysqlDeleteData):
    def __init__(self):
        head = ["账号", "密码", "邮箱", "出发地", "目的地", "日期", "出发时间\n到达时间", "车次", "买票人\n姓名", "座位号", "座位类型", "乘车类型", "当前状态", "Error", "", ""]
        super(ShowTools, self).__init__()
        self.first_finish = False
        self.all_data_list = []
        self.state_error_data = []
        self.combobox_list = []
        self.desktop = QtWidgets.QApplication.desktop()
        self.MainWindow = QtWidgets.QMainWindow()
        self.MainWindow.resize(self.desktop.width(), self.desktop.height())
        self.table_widget = QtWidgets.QTableWidget(self.MainWindow)
        self.table_widget.resize(int(self.desktop.width()), int(self.desktop.height()))
        self.table_widget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_widget.verticalHeader().setDefaultSectionSize(50)
        # 设置表格不可编辑
        self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_widget.setColumnCount(14)
        for i in range(14):
            item = QtWidgets.QTableWidgetItem()
            item.setText(head[i])
            self.table_widget.setHorizontalHeaderItem(i, item)
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def train_ids(self):
        train_ids = sorted(list(set(self.get_all_data())))
        logging.info(train_ids)
        return train_ids

    def start(self, train_ids):
        self.table_widget.setRowCount(len(train_ids))
        for i, train_id in enumerate(train_ids):
            all_data = self.row_all_data(train_id)
            self.show_row_data(train_id, i, all_data)
            self.all_data_list.append(all_data)

    def update_start(self):
        while True:
            train_ids = sorted(list(set(self.get_all_data())))
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
                        self.table_widget.setRowCount(len(train_ids))
                        self.all_data_list.append(all_data)
                    logging.info(f"row: {str(i)}")
                    self.show_row_data(train_id, i, all_data)
                    print("已修改更改的内容！")
            time.sleep(3)

    def show_row_data(self, train_id, i, all_data):
        print(all_data)
        print(len(all_data))
        for j in range(8):
            self.set_table_widget_item(i, j, all_data[j])
        for j in range(12, 13):
            self.set_table_widget_item(i, j, all_data[j-3])
        user_name_list = all_data[8]
        if len(user_name_list) == 1:
            print("user_name_list:", user_name_list)
            user_name = user_name_list[0]
            item = QtWidgets.QTableWidgetItem()
            item.setText(user_name[3])
            self.table_widget.setItem(i, 8, item)
            self.combobox_list.append("")
        else:
            try:
                combobox = self.combobox_list[i]
                combobox.clear()
            except IndexError:
                combobox = QtWidgets.QComboBox(self.table_widget)
                self.combobox_list.append(combobox)
                combobox.setObjectName(f"{i}")
            for user_name in user_name_list:
                user_name = user_name[3]
                # print(user_name)
                combobox.addItem(user_name)
            self.table_widget.setCellWidget(i, 8, combobox)
            user_name = self.get_user_name_add_sent(train_id, "UserName='%s'" % combobox.currentText())
            combobox.currentIndexChanged.connect(lambda: self.update_user_login_data(train_id, i))
        self.user_login_data(user_name, i)
        self.table_widget.viewport().update()

    def row_all_data(self, train_id):
        all_data = []
        user_station_id = self.get_user_station_id(train_id)[0]
        all_data.extend(self.get_user(user_station_id[0]))
        all_data.extend(self.get_station(user_station_id[1]))
        all_data.extend(self.get_train(train_id, "Train, TrainDate"))
        username_logindata_ids = self.get_username_logindata_id(train_id)
        user_name_list = []
        for username_logindata_id in username_logindata_ids:
            user_name_list.append(self.get_user_name(username_logindata_id[0], "Seat"))
        all_data.append(user_name_list)
        all_data.extend(self.get_train(train_id, "State, Error"))
        logging.info(all_data)
        return all_data

    def update_user_login_data(self, train_id, i):
        combobox = self.combobox_list[i]
        user_name = self.get_user_name_add_sent(train_id, "UserName='%s'" % combobox.currentText())
        self.user_login_data(user_name, i)

    def user_login_data(self, user_name, i):
        print(user_name, i)
        for j in range(9, 12):
            self.set_table_widget_item(i, j, user_name[j-9])
        self.table_widget.viewport().update()

    def set_table_widget_item(self, row, count, text):
        item = QtWidgets.QTableWidgetItem()
        item.setText(text)
        self.table_widget.setItem(row, count, item)
        self.table_widget.item(row, count).setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)  # 创建一个QApplication，也就是你要开发的软件app
    ui = ShowTools()  # ui是Ui_MainWindow()类的实例化对象
    train_ids = ui.train_ids()
    ui.start(train_ids)
    # ui.setupUi(MainWindow)  # 执行类中的setupUi方法，方法的参数是第二步中创建的QMainWindow
    ui.MainWindow.show()
    threading.Thread(target=ui.start, daemon=True).start()
    # print(ui.combobox_list)
    app.exec_()
