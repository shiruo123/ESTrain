import time
import data_proces
from selenium.webdriver.common.by import By
import mysql
import selenLinux

WHILE_TIME = 3


class Server(object):
    def __init__(self):
        self.get_mysql = mysql.MysqlGetData()
        self.update_mysql = mysql.MysqlUpdateDate()
        self.set_mysql = mysql.MysqlSetData()

    def start(self):
        # while True:
        self.all_data()
        # self.while_time()
        # self.selen_pa()

    def all_data(self):
        all_datas_IDs = self.get_mysql.get_all_data()
        all_datas_ID = set(all_datas_IDs)
        print(all_datas_ID)
        for data_ID in all_datas_ID:
            account_data = self.get_mysql.get_select_data("user.ID, station.ID", "user, station, train", f"train.ID={data_ID[0]}")[0]
            user_data = self.get_mysql.get_select_data("user_name.ID, login_data.ID", "train, user_name, login_data",
                                                   f"train.ID=user_name.TrainID and user_name.ID=login_data.UserNameID and train.ID={data_ID[0]}")
            selen_state = self.get_mysql.get_train(data_ID, "State")
            if selen_state == "static":
                self.selen_pa(account_data, user_data, data_ID[0])

    def selen_pa(self, user_id, login_ids, train_id):
        self.update_mysql.update_train_state(train_id, "static", "active")
        login_data = self.get_mysql.get_station(user_id[1])
        pa = selenLinux.paData()
        pa.browser_pa(*login_data)
        train = self.train(train_id)
        pa.td_int, td = self.is_td_pa_data(train, pa.tr)
        data = pa.pa_data(td)
        data = data_proces.data_heard_process_1(data)
        pa.str_ck = self.user_name(login_ids)
        self.update_login(pa, data)
        self.login(pa, user_id[0])
        pa.user_name()
        pa.piao_data()
        self.seat(pa, login_ids)
        pa.selection_seat()
        text = pa.user_email_send()
        if text.split("，")[0] == "席位已锁定":
            self.update_mysql.update_train_state(train_id, "active", "finish")
        else:
            self.update_mysql.update_train_state(train_id, "active", "static")

    def train(self, ID):
        train = self.get_mysql.get_train(ID)
        return train[0]

    def update_login(self, pa, ck_cc_data):
        for i in range(len(ck_cc_data[0])):
            if ck_cc_data[0][i] == pa.str_ck[0][1]:
                pa.update_login(ck_cc_data, i)
                self.set_mysql.set_train_data(ck_cc_data[0], i)
                break

    def login(self, pa, ID):
        datas = self.get_mysql.get_user(ID)
        pa.login(*datas)

    def user_name(self, IDs):
        str_ck = []
        print(IDs)
        for ID in IDs:
            datas = self.get_mysql.get_user_name(ID[0])
            str_ck.append(list(datas))
        for i in range(len(str_ck)):
            str_ck[i][1] = str_ck[i][1].split("票价")[0]
        return str_ck

    def seat(self, pa, IDs):
        seats = []
        for ID in IDs:
            seat = self.get_mysql.get_seat(ID[1])[0]
            seats.append(seat)
        pa.str_zw = seats

    @staticmethod
    def is_td_pa_data(text, tr):
        for i, td in enumerate(tr):
            txt = td.find_element(By.XPATH, 'td[1]/div/div[1]/div/a').text
            if txt == text:
                return i, td

    def while_time(self):
        time.sleep(WHILE_TIME)


if __name__ == '__main__':
    getdata = Server()
    getdata.start()
