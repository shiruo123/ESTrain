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
import SendEmail
import mysql

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")


class paData(object):
    def __init__(self):
        self.get_mysql = mysql.MysqlGetData()
        self.td_int = 0
        self.str_ck = None
        self.tr = None
        self.str_zw = ["G"]

    def browser_pa(self, departure, destination, date, **kwargs):
        option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        # option.add_argument('blink-settings=imagesEnabled=false')
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.binary_location = CHROME_PATH
        self.browser = webdriver.Chrome(options=option)
        self.browser.minimize_window()
        self.browser.get("https://kyfw.12306.cn/otn/leftTicket/init")
        self.wait = ui.WebDriverWait(self.browser, 3)
        # 出发地输入
        self.fromStationText(departure)
        # 目的地输入
        self.toStationText(destination)
        # 日期输入
        self.date_icon_1(str(date))
        self.pa()

    def pa(self):
        """
        爬取一共有多少车次，即最后面的预约还是抢票
        :return:
        """
        logging.info("正在获取数据有无票信息。")
        self.browser.find_element(By.XPATH, '//*[@id="query_ticket"]').click()
        while True:
            try:
                self.tr = self.browser.find_elements(By.XPATH, '//*[@id="queryLeftTable"]/tr')
                self.tr.pop(-1)
                break
            except IndexError:
                time.sleep(0.5)
        self.tr = self.tr[::2]

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

    def pa_data(self, td):
        b = []
        c = []
        for i in range(2, 13):
            text = td.find_element(By.XPATH, f'td[{i}]').get_attribute("aria-label")
            if text is not None:
                b.append(text.split("，")[-2] + text.split("，")[-1])
                c.append(i)
        # print(a)
        # print(b)
        return [b, c]
        # self.data_list.append(a)
        # self.data_list_b.append(b)

    def update_login(self, ID, train_name):
        """
        传入信息，开始抢票或者买票
        :param str_zw: 座位号，如果是火车无需座位号则等于G
        :param str_ck: 乘客信息[['成人票', '硬座票价9元剩有', '乘客姓名']]
        :param td_int: 第几个车次
        :param ck_cc_data: 车票信息及车票信息序号[['软卧票价81.5元剩3', '硬卧票价55元剩有', '硬座票价9元剩有'], [6, 8, 10]]
        :return:
        """
        ck_cc_data, i = self.get_mysql.get_train_data(ID)
        ck_cc_data = eval(ck_cc_data)
        text = self.browser.find_element(By.XPATH, f'//*[@id="queryLeftTable"]/tr[{self.td_int * 2 + 1}]/td[1]/div/div/div/a').text
        logging.info(f"当前车次{text},已选择{ck_cc_data[0][i].split('票价')[0]},车票剩余{ck_cc_data[0][i].split('剩')[-1]}")
        while True:
            try:
                # print(ck_cc_data[1][i])
                a = self.browser.find_element(By.XPATH, f'//*[@id="queryLeftTable"]/tr[{self.td_int * 2 + 1}]/td[{ck_cc_data[1][i]}]').text
                # print(a)
                if a != "候补" and a != "无":
                    new_train_name = self.browser.find_element(By.XPATH, f'//*[@id="queryLeftTable"]/tr[{self.td_int * 2 + 1}]/td[1]/div/div[1]/div/a')
                    if new_train_name == train_name:
                        break
                    else:
                        for i, td in enumerate(self.tr):
                            txt = td.find_element(By.XPATH, 'td[1]/div/div[1]/div/a').text
                            if txt == train_name:
                                self.td_int = i
                                self.update_login(ID, train_name)
                                break
            except NoSuchElementException or NoSuchWindowException:
                pass
            try:
                self.browser.find_element(By.XPATH, '//*[@id="query_ticket"]').click()
            except:
                continue
            time.sleep(random.randint(ESTRAIN_UPDATA_TIME_MIN, ESTRAIN_UPDATA_TIME_MAX))

    def login(self, user_account, password, user_email):
        self.user_email = user_email
        self.browser.find_element(By.XPATH,
                                  f'//*[@id="queryLeftTable"]/tr[{self.td_int * 2 + 1}]/td[13]/a').click()
        time.sleep(3)
        self.browser.find_element(By.XPATH, '//*[@id="J-userName"]').clear()
        self.browser.find_element(By.XPATH, '//*[@id="J-userName"]').send_keys(user_account)
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
                self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="nc_1_refresh1"]'))).click()
                continue
            except:
                pass
            break
        logging.info("登入成功")

    def user_name(self):
        while True:
            try:
                ck_data = self.wait.until(expected_conditions.presence_of_all_elements_located((By.XPATH, '//*[@id="normal_passenger_id"]/li')))
                break
            except TimeoutException:
                try:
                    self.browser.find_element(By.XPATH, '//*[@id="qd_closeDefaultWarningWindowDialog_id"]').click()
                except:
                    # self.login(str_zw, str_ck, self.td_int)
                    pass
        for ck_cp in self.str_ck:
            for ck in range(len(ck_data)):
                text = self.browser.find_element(By.XPATH, f'//*[@id="normal_passenger_id"]/li[{ck+1}]/label')
                if text.text.split("(")[0] == ck_cp[2]:
                    self.browser.find_element(By.XPATH, f'//*[@id="normalPassenger_{ck}"]').click()
                    # print(ck_cp, ck_cp[1])
                    if ck_cp[0] == "学生票":
                        self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="dialog_xsertcj_ok"]'))).click()
                    else:
                        try:
                            self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, '//*[@id="dialog_xsertcj_cancel"]'))).click()
                        except:
                            pass
                    logging.info("已选择"+ck_cp[2])
                    break

    def piao_data(self):
        for ck_i in range(len(self.str_ck)):
            # print(ck_i)
            select_1 = ui.Select(self.browser.find_element(By.XPATH, f'//*[@id="ticketType_{ck_i+1}"]'))
            select_2 = ui.Select(self.browser.find_element(By.XPATH, f'//*[@id="seatType_{ck_i+1}"]'))
            for select in [select_1, select_2]:
                for select_text in select.options:
                    if select_text.text.split("（")[0] == self.str_ck[ck_i][0] or select_text.text.split("（")[0] == self.str_ck[ck_i][1]:
                        select.select_by_visible_text(select_text.text)
                        logging.info(("已选择"+select_text.text))
                        break
        self.browser.find_element(By.XPATH, '//*[@id="submitOrder_id"]').click()

    def selection_seat(self):
        if self.str_zw[0] == "G":
            time.sleep(2)
            self.browser.find_element(By.XPATH, '//*[@id="qr_submit_id"]').click()
            return
        time.sleep(5)
        try:
            for i in range(len(self.str_zw)):
                # print(str_zw[i])
                # print(self.browser.find_elements(By.XPATH, f'//*[@id="1{str_zw[i]}"]'))
                for j in self.browser.find_elements(By.XPATH, f'//*[@id="1{self.str_zw[i]}"]'):
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

    def user_email_send(self):
        while True:
            try:
                yes_chepiao = self.browser.find_element(By.XPATH, '//*[@id="main_content"]/div[1]/div/h3/span')
                break
            except:
                time.sleep(1)
        content = yes_chepiao.text
        print(content)
        user_name_list = [name[2] for name in self.str_ck]
        email_message = SendEmail.mail(self.user_email, content, user_name_list)
        logging.info(email_message)
        return content


if __name__ == '__main__':
    pa = paData()
    # print(pa.pa("醴陵东", "萍乡北", "2023/3/21"))
# browser.find_element(By.XPATH, '//*[@id="back_train_date"]').send_keys("2023-03-16", Keys.ENTER)
