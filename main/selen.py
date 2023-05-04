import threading
import random
import time
from queue import Queue
import getdata
import selenium
import wait
from selenium.common.exceptions import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from multiprocessing.dummy import Process
from selenium.webdriver.support import ui, expected_conditions
from selenium.webdriver.common.action_chains import ActionChains
import logging
from setting import *

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")


class paData(object):
    def __init__(self, chaxun_list=False):
        self.browser_is_input = True
        self.chaxun_list = chaxun_list

    def browser_pa(self):
        departure_destination_date = getdata.rfp().get("data").get("searchgui").copy()
        option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        # option.add_argument('blink-settings=imagesEnabled=false')
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.binary_location = CHROME_PATH
        self.browser = webdriver.Chrome(options=option)
        self.browser.minimize_window()
        self.browser.get("https://kyfw.12306.cn/otn/leftTicket/init")
        # 出发地输入
        self.fromStationText(departure_destination_date.get("departure"))
        # 目的地输入
        self.toStationText(departure_destination_date.get("destination"))
        # 日期输入
        self.date_icon_1(departure_destination_date.get("date"))
        self.browser_is_input = False
        if self.chaxun_list:
            self.pa()

    def pa(self):
        """
        爬取一共有多少车次，即最后面的预约还是抢票
        :return:
        """
        if self.browser_is_input:
            self.pa_wait = wait.Wait(text="请等待浏览器初始化", login_wait=True)
            threading.Thread(target=self.while_wait).start()
            self.pa_wait.wait_window.exec_()
            # time.sleep(3)
            # tr_int, td_15_list = self.pa()
            # return tr_int, td_15_list
        logging.info("正在获取数据总数和有无票信息。")
        self.data_list = []
        self.data_list_b = []
        self.browser.find_element(By.XPATH, '//*[@id="query_ticket"]').click()
        while True:
            try:
                self.tr = self.browser.find_elements(By.XPATH, '//*[@id="queryLeftTable"]/tr')
                self.tr.pop(-1)
                break
            except IndexError:
                time.sleep(0.5)
        self.tr = self.tr[::2]
        a = []
        for td in self.tr:
            try:
                a.append(td.find_element(By.XPATH, 'td[13]/a').text)
            except NoSuchElementException:
                a.append("抢票")
        return len(self.tr), a

    def while_wait(self):
        while True:
            if self.browser_is_input:
                time.sleep(0.1)
            else:
                self.pa_wait.wait_window.close()
                break

    def fromStationText(self, fromstation):
        self.browser.find_element(By.XPATH, '//*[@id="fromStationText"]').clear()
        self.browser.find_element(By.XPATH, '//*[@id="fromStationText"]').click()
        self.browser.find_element(By.XPATH, '//*[@id="fromStationText"]').send_keys(fromstation, Keys.ENTER)

    def toStationText(self, tostation):
        self.browser.find_element(By.XPATH, '//*[@id="toStationText"]').clear()
        self.browser.find_element(By.XPATH, '//*[@id="toStationText"]').click()
        self.browser.find_element(By.XPATH, '//*[@id="toStationText"]').send_keys(tostation, Keys.ENTER)

    def date_icon_1(self, date):
        self.browser.find_element(By.XPATH, '//*[@id="date_icon_1"]').click()
        self.browser.find_element(By.XPATH, '//*[@id="train_date"]').clear()
        self.browser.find_element(By.XPATH, '//*[@id="train_date"]').send_keys(date)

    def pa_data(self):
        for td in self.tr:
            a = []
            b = []
            c = []
            a.append(td.find_element(By.XPATH, 'td[1]/div/div[1]/div/a').text)
            a.append(td.find_element(By.XPATH, 'td[1]/div/div[2]/strong[1]').text + "\n" + td.find_element(By.XPATH,
                                                                                                           'td[1]/div/div[2]/strong[2]').text)
            a.append(td.find_element(By.XPATH, 'td[1]/div/div[3]/strong[1]').text + "\n" + td.find_element(By.XPATH,
                                                                                                           'td[1]/div/div[3]/strong[2]').text)
            try:
                a.append(td.find_element(By.XPATH, 'td[1]/div/div[4]/strong').text + "\n" + td.find_element(By.XPATH,
                                                                                                            'td[1]/div/div[4]/span').text)
            except:
                yield [["--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--", "--"], []]
            for i in range(2, 13):
                text = td.find_element(By.XPATH, f'td[{i}]').get_attribute("aria-label")
                if text is None:
                    text = "--"
                else:
                    b.append(text.split("，")[-2] + text.split("，")[-1])
                    c.append(i)
                    text = f'{text.split("，")[-2].split("票价")[-1]}\n{text.split("，")[-1]}'
                a.append(text)
            logging.info(str(a) + "爬取成功")
            # print(a)
            # print(b)
            yield [a, b, c]
            # self.data_list.append(a)
            # self.data_list_b.append(b)

    def update_login(self, str_zw, str_ck, td_int, ck_cc_data):
        # print(str_ck)
        print(ck_cc_data)
        for i in range(len(ck_cc_data[0])):
            # print(ck_cc_data[0][i], str_ck[0][1])
            if ck_cc_data[0][i] == str_ck[0][1]:
                break
        while True:
            try:
                # print(ck_cc_data[1][i])
                a = self.browser.find_element(By.XPATH, f'//*[@id="queryLeftTable"]/tr[{td_int * 2 + 1}]/td[{ck_cc_data[1][i]}]').text
                # print(a)
                if a != "候补" and a != "无":
                    break
            except NoSuchElementException or NoSuchWindowException:
                pass
            try:
                self.browser.find_element(By.XPATH, '//*[@id="query_ticket"]').click()
            except:
                continue
            time.sleep(random.randint(ESTRAIN_UPDATA_TIME_MIN, ESTRAIN_UPDATA_TIME_MAX))
        self.login(str_zw, str_ck, td_int)

    def login(self, str_zw, str_ck, td_int):
        # print(str_zw, str_ck, td_int)
        login_data = getdata.rfp()
        username = login_data.get("data").get("logingui").get("account")
        password = login_data.get("data").get("logingui").get("password")
        for i in range(len(str_ck)):
            str_ck[i][1] = str_ck[i][1].split("票价")[0]
        logging.info("执行到了login开始进入买票界面" + f"{td_int}")
        # str0 = ["A", "B"]
        # str1 = [['二等座', '成人票', '邓少青'], ['一等座', '学生票', '少青']]
        wait = ui.WebDriverWait(self.browser, 3)
        self.browser.find_element(By.XPATH,
                                  f'//*[@id="queryLeftTable"]/tr[{td_int * 2 + 1}]/td[13]/a').click()
        time.sleep(3)
        self.browser.find_element(By.XPATH, '//*[@id="J-userName"]').clear()
        self.browser.find_element(By.XPATH, '//*[@id="J-userName"]').send_keys(username)
        self.browser.find_element(By.XPATH, '//*[@id="J-password"]').send_keys(password)
        self.browser.find_element(By.XPATH, '//*[@id="J-login"]').click()
        time.sleep(2)
        script = 'Object.defineProperty(navigator,"webdriver",{get:()=>undefined,});'
        self.browser.execute_script(script)
        while True:
            try:
                span = self.browser.find_element(By.XPATH, '//*[@id="nc_1_n1z"]')
            except NoSuchElementException:
                self.browser.find_element(By.XPATH, '//*[@id="verification"]/li[1]/a').click()
                continue
            try:
                action = webdriver.ActionChains(self.browser)
                action.click_and_hold(span)
                action.drag_and_drop_by_offset(span, 300, 0).perform()
            except:
                pass
            try:
                wait.until(expected_conditions.element_to_be_clickable(
                    (By.XPATH, '//*[@id="nc_1_refresh1"]'))).click()
                continue
            except:
                pass
            break
        logging.info("登入成功")
        while True:
            try:
                ck_data = wait.until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//*[@id="normal_passenger_id"]/li')))
                break
            except TimeoutException:
                try:
                    self.browser.find_element(By.XPATH, '//*[@id="qd_closeDefaultWarningWindowDialog_id"]').click()
                except:
                    self.login(str_zw, str_ck, td_int)
        for ck_cp in str_ck:
            for ck in range(len(ck_data)):
                text = self.browser.find_element(By.XPATH, f'//*[@id="normal_passenger_id"]/li[{ck+1}]/label')
                if text.text.split("(")[0] == ck_cp[2]:
                    self.browser.find_element(By.XPATH, f'//*[@id="normalPassenger_{ck}"]').click()
                    # print(ck_cp, ck_cp[1])
                    if ck_cp[0] == "学生票":
                        wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="dialog_xsertcj_ok"]'))).click()
                    else:
                        try:
                            wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="dialog_xsertcj_cancel"]'))).click()
                        except:
                            pass
                    logging.info("已选择"+ck_cp[2])
                    break
        for ck_i in range(len(str_ck)):
            # print(ck_i)
            select_1 = ui.Select(self.browser.find_element(By.XPATH, f'//*[@id="ticketType_{ck_i+1}"]'))
            select_2 = ui.Select(self.browser.find_element(By.XPATH, f'//*[@id="seatType_{ck_i+1}"]'))
            for select in [select_1, select_2]:
                for select_text in select.options:
                    # print(select_text.text.split("（")[0])
                    # print(str_ck[ck_i][0], str_ck[ck_i][1])
                    if select_text.text.split("（")[0] == str_ck[ck_i][0] or select_text.text.split("（")[0] == str_ck[ck_i][1]:
                        select.select_by_visible_text(select_text.text)
                        logging.info(("已选择"+select_text.text))
                        break
        self.browser.find_element(By.XPATH, '//*[@id="submitOrder_id"]').click()
        # wait.until(expected_conditions.presence_of_all_elements_located((By.XPATH, f'//*[@id="1{str_zw[0]}"]')))
        if str_zw == "G":
            # self.browser.find_element(By.XPATH, '//*[@id="qr_submit_id"]').click()
            pass
        else:
            time.sleep(5)
            try:
                for i in range(len(str_zw)):
                    # print(str_zw[i])
                    # print(self.browser.find_elements(By.XPATH, f'//*[@id="1{str_zw[i]}"]'))
                    for j in self.browser.find_elements(By.XPATH, f'//*[@id="1{str_zw[i]}"]'):
                        try:
                            j.click()
                            logging.info("选座成功")
                            break
                        except:
                            # print("选座失败")
                            pass
                    # self.browser.find_elements(By.XPATH, f'//*[@id="1{str_zw[i]}"]')[1].click()
            except:
                logging.info("座位选择错误")
                pass
        self.browser.find_element(By.XPATH, '//*[@id="qr_submit_id"]').click()


if __name__ == '__main__':
    pa = paData()
    pa_1, a = pa.pa("萍乡北", "醴陵东", "2023/3/29")
    pa_2 = pa.pa_data()
    for i in pa_2:
        print(i)
    print(a)
    # print(pa.pa("醴陵东", "萍乡北", "2023/3/21"))
# browser.find_element(By.XPATH, '//*[@id="back_train_date"]').send_keys("2023-03-16", Keys.ENTER)
