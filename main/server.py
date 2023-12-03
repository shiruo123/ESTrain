import logging
import time
import data_proces
from selenium.webdriver.common.by import By
import mysql
import selenLinux
from concurrent.futures import ThreadPoolExecutor

WHILE_TIME = 3

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")


class Server(object):
    def __init__(self):
        self.get_mysql = mysql.MysqlGetData()
        self.update_mysql = mysql.MysqlUpdateDate()
        self.set_mysql = mysql.MysqlSetData()

    def start(self):
        while True:
            all_data_generator = self.all_data()
            pool = ThreadPoolExecutor(20)
            while True:
                try:
                    all_ids = next(all_data_generator)
                    logging.info(all_ids)
                    pa_data = StartPaData(*all_ids)
                    pool.submit(pa_data.selen_pa)
                except StopIteration:
                    break
            self.while_time()
        # self.selen_pa()

    def all_data(self):
        all_datas_IDs = self.get_mysql.get_all_data()
        logging.info(all_datas_IDs)
        for data_ID in all_datas_IDs:
            account_data = self.get_mysql.get_user_station_id(data_ID)
            user_data = self.get_mysql.get_username_logindata_id(data_ID)
            selen_state = self.get_mysql.get_train(data_ID, "State")
            print(selen_state, account_data, user_data)
            if selen_state[0] == "static":
                yield account_data[0], user_data, data_ID[0]
            else:
                continue
    @staticmethod
    def while_time():
        time.sleep(WHILE_TIME)


class StartPaData(mysql.Mysql):
    def __init__(self, user_id, login_ids, train_id):
        super(StartPaData, self).__init__()
        self.get_mysql = mysql.MysqlGetData()
        self.update_mysql = mysql.MysqlUpdateDate()
        self.set_mysql = mysql.MysqlSetData()
        self.train_id = None
        self.train = None
        self.user_id = user_id
        self.login_ids = login_ids
        self.train_id = train_id
        self.pa = None

    def selen_pa(self):
        self.update_mysql.update_train_state(self.train_id, "active")
        self.train = self.train_name()
        login_data = self.get_mysql.get_station(self.user_id[1])
        self.pa = selenLinux.paData()
        self.pa.browser_pa(*login_data)
        print(self.train)
        self.pa.td_int, td = self.is_td_pa_data(self.pa.tr)
        data = self.pa.pa_data(td)
        data = data_proces.data_heard_process_1(data)
        self.pa.str_ck = self.user_name(self.login_ids)
        self.update_login(data)
        self.pa.update_login(self.train_id, self.train)
        self.login(self.user_id[0])
        self.pa.user_name()
        self.pa.piao_data()
        self.seat(self.login_ids)
        self.pa.selection_seat()
        text = self.pa.user_email_send()
        if text.split("，")[0] == "席位已锁定":
            self.update_mysql.update_train_state(self.train_id, "finish")
        else:
            self.update_mysql.update_train_state(self.train_id, "static")

    def train_name(self):
        train = self.get_mysql.get_train(self.train_id)[0]
        return train

    def update_login(self, ck_cc_data):
        for i in range(len(ck_cc_data[0])):
            if ck_cc_data[0][i].split("票价")[0] == self.pa.str_ck[0][1]:
                self.set_mysql.set_train_data(self.train_id, ck_cc_data, i)
                self.update_mysql.update_train_data_station_data(self.train_id, ck_cc_data)
                break
        else:
            self.error(self.train_id, f"{self.train}:没有{self.pa.str_ck[0][1]}这个座位。")

    def login(self, ID):
        datas = self.get_mysql.get_user(ID)
        self.pa.login(*datas)

    def user_name(self, IDs):
        str_ck = []
        print(IDs)
        for ID in IDs:
            datas = self.get_mysql.get_user_name(ID[0])
            str_ck.append(list(datas))
        return str_ck

    def seat(self, IDs):
        seats = []
        for ID in IDs:
            seat = self.get_mysql.get_seat(ID[1])[0]
            seats.append(seat)
        self.pa.str_zw = seats

    def is_td_pa_data(self, tr):
        for i, td in enumerate(tr):
            txt = td.find_element(By.XPATH, 'td[1]/div/div[1]/div/a').text
            if txt == self.train:
                return i, td
        else:
            self.error(self.train_id, f"未知的车票:{self.train}。请确认当前地址和时间是否有此车票。")

    def error(self, train_id, text):
        self.update_mysql.update_train_error(train_id, text)
        self.update_mysql.update_train_state(train_id, "static")
        exit()


if __name__ == '__main__':
    getdata = Server()
    getdata.start()
