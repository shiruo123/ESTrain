import json
import getdata


class DataSave(object):

    def __init__(self):
        self.rjson = getdata.rfp()
        self.data = {
            "data": {}
        }
        self.init_data()

    def init_data(self):
        self.init_login_data = self.rjson["data"].get("logingui")
        self.login_data = {
            "logingui": self.init_login_data
        }
        self.init_search_data = self.rjson["data"].get("searchgui")
        self.search_data = {
            "searchgui": self.init_search_data
        }

    def login_gui_data_save(self, login_data=None):
        if login_data is not None:
            self.login_data = {
                "logingui": login_data
            }
        # print(data)

    def search_gui_data_save(self, search_data=None):
        if search_data is not None:
            self.search_data = {
                "searchgui": search_data
            }

    def write(self):
        self.fp = open("../setting.json", 'w', encoding="utf-8")
        self.data.get("data").update(self.login_data)
        self.data.get("data").update(self.search_data)
        self.fp.write(json.dumps(self.data, indent=4, ensure_ascii=False))
        self.fp.close()


if __name__ == '__main__':
    a = {'account_lineEdit': '18897941661', 'password_lineEdit_2': ''}
    data = DataSave()
    data.login_gui_data_save()
    data.write()
