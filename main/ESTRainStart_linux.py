import argparse
import logging
import json
from selenium.webdriver.common.by import By
import selen
import threading
import readline

# parser = argparse.ArgumentParser(description='api抢票或者买票')
# parser.add_argument('UserAccount', type=int, help='用户账号')
# parser.add_argument('UserPassword', type=int, help='用户密码')
# parser.add_argument('FromStation', type=str, help='出发地')
# parser.add_argument('ToStation', type=str, help='目的地')
# parser.add_argument('Date', type=str, help='日期(2023-05-05)')
# parser.add_argument('UserName', type=str, help='用户名(买票人姓名)')
# parser.add_argument('-a', action='store_true')
# args = parser.parse_args()
# print(args)
import data_proces

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class ESTrainStartLinux(object):

    def __init__(self):

        self.pa_browser = None
        self.first_browser = False
        self.user_account = []

    def project_start(self):

        while True:
            try:
                number = int(input("1. 查询车票信息\n2. 购票\\抢票('注意：需先输入用户信息')\n3. 输入用户信息\n0. 退出\n''''填写需要即可'''\n请输入:"))
            except:
                continue
            if number == 1:
                self.select_piao()

            elif number == 2:
                self.shop_qiang_piao()

            elif number == 3:
                self.user_data()

            elif number == 0:
                self.pa_browser.browser.close()
                break

    def select_piao(self):
        self.datas = []
        self.from_station = input("[出发地:]>>")
        self.to_station = input("[目的地:]>>")
        self.date = input("[日期:(格式:2023-05-05)]>>")
        if self.first_browser:
            self.pa_browser.fromStationText(self.from_station)
            self.pa_browser.toStationText(self.to_station)
            self.pa_browser.date_icon_1(self.date)
            self.pa_browser.browser.find_element(By.XPATH, '//*[@id="query_ticket"]').click()
        else:
            self.browser_chrome(self.from_station, self.to_station, self.date)
            self.first_browser = True
        self.tr, self.len_tr = self.pa_browser.pa()
        for td in self.pa_browser.tr:
            self.data_list = self.pa_browser.pa_data(td)
            data_list_0_len = len(self.data_list[0])
            data = []
            data.extend(self.data_list[0][i] for i in range(4))
            n = 0
            for i in range(4, data_list_0_len):
                if self.data_list[0][i] != "--":
                    data.append(self.data_list[1][n])
                    n += 1
            self.datas.append(self.data_list)
            logging.info(data)

    def user_data(self):
        # self.user_account = input("[用户账户:]>>")
        # self.user_password = input("[用户密码:]>>")
        # self.user_name = input("[买票人姓名(可多选):]>>")
        # self.user_email = input("[邮箱:(接收抢票信息用的)]>>")
        user_datas = open("../UserDataSetting.json", 'r', encoding="utf-8")
        user_datas_json = json.loads(user_datas.read())
        self.user_account = user_datas_json.get("UserAccount")
        self.user_password = user_datas_json.get("UserPassword")
        self.user_name_list = user_datas_json.get("UserName").split(",")
        logging.info(str(self.user_name_list))
        self.user_email = user_datas_json.get("UserEmail")
        logging.info("用户信息保存成功")

    def shop_qiang_piao(self):
        if self.user_account is None:
            logging.info("请先输入用户信息！！！")
            return
        self.che_piao = input("[车次名(可多选):(例:G1234,G4321)]>>")
        self.che_piao_list = self.che_piao.split(",")
        self.zuoweileixing = input("[选票座(可多选):(例:二等座、硬座)]>>")
        self.zuoweileixing_list = self.zuoweileixing.split(",")
        self.zuoweihao = input("[座位号(可多选):(A,F)]>>")
        self.zuoweihao_list = self.zuoweihao.split(",")
        self.normalPassenger = input("[票类型(可多选):(成人票,成人票)]>>")
        self.normalPassenger_list = self.normalPassenger.split(",")
        logging.info(f"{str(self.che_piao_list)},{str(self.zuoweileixing_list)},{self.zuoweihao_list},{self.normalPassenger_list}")
        for i in range(len(self.che_piao_list)):
            str_ck = []
            ck_cc_data = []
            for j in range(len(self.user_name_list)):
                logging.info(self.zuoweihao_list)
                str_ck.append([self.normalPassenger_list[j], self.zuoweileixing_list[i], self.user_name_list[j]])
                logging.info(str(str_ck))
                for z in range(len(self.datas)):
                    if self.che_piao_list[i] == self.datas[z][0][0]:
                        td_int = z
                        logging.info(td_int)
                        break
                self.piao_money = data_proces.data_heard_process_1([self.datas[td_int][1], self.datas[td_int][2]])
            threading.Thread(target=self.pa_browser.update_login, args=(self.zuoweihao_list, str_ck, td_int, self.piao_money)).start()
            self.browser_chrome(self.from_station, self.to_station, self.date)

    def browser_chrome(self, from_station, to_station, date):
        self.pa_browser = selen.paData()
        self.pa_browser.browser_pa(departure=from_station, destination=to_station, date=date)


if __name__ == '__main__':
    start = ESTrainStartLinux()
    start.project_start()
