import json
import time


def rfp():
    now_time = time.localtime()
    read = open("../setting.json", 'r', encoding="utf-8")
    try:
        rjson = json.loads(read.read())
        date = rjson.get("data").get("searchgui").get("date")
        strp_date = time.strptime(date, "%Y-%m-%d")
        if strp_date.tm_mday < time.localtime().tm_mday and strp_date.tm_mon == time.localtime().tm_mon:
            rjson.get("data").get("searchgui")["date"] = time.strftime("%Y-%m-%d", time.localtime())
        read.close()
        return rjson
    except:
        rjson = {'data': {'logingui': {'account': '', 'password': ''},
                'searchgui': {'departure': '萍乡北', 'destination': '醴陵东', 'date': time.strftime("%Y-%m-%d", time.localtime())}}}
        read.close()
        return rjson


if __name__ == '__main__':
    a = rfp()
    print(a)
