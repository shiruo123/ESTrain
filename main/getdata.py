import json


def rfp():
    read = open("../setting.json", 'r', encoding="utf-8")
    try:
        rjson = json.loads(read.read())
        read.close()
        return rjson
    except:
        rjson = {'data': {'logingui': {'account': '18897941661', 'password': ''},
                'searchgui': {'departure': '萍乡北', 'destination': '醴陵东', 'date': '2023/3/12'}}}
        read.close()
        return rjson


if __name__ == '__main__':
    a = rfp()
    print(a)
