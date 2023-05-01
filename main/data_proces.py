def login_gui_data_proces(lineedit_data_list):
    # print(lineedit_data_list[0])
    try:
        if len(lineedit_data_list[0]) == 0 | len(lineedit_data_list[1]) < 6:
            data = None
        else:
            data = {
                "account": lineedit_data_list[0],
                "password": lineedit_data_list[1]
            }
    except IndexError:
        data = None
    return data


def search_gui_data_process(data_list):
    if len(data_list[0]) == 0 | len(data_list[1]) == 0:
        data = None
    else:
        data = {
            "departure": data_list[0],
            "destination": data_list[1],
            "date": data_list[2]
        }
    return data


def data_heard_process(data_process):
    # print(data_process)
    data = ['商务座\n特等座', '一等座', '二等座\n二等包座', '高级软卧', '软卧\n一等卧', '动卧', '硬卧\n二等卧', '软座', '硬座', '无座']
    # a = '42元\n余票3', '22.5元\n余票11', '13.5元\n余票有', '--', '--', '--','--', '--', '--', '--', '--']
    str_list = []
    for i in range(len(data_process)):
        if data_process[i] != "--":
            str_data = data[i].replace("\n", "n") + "n(" + data_process[i].replace("\n", "") + ")"
            # if str_data
            str_list.append(str_data)
    return str_list


def data_heard_process_1(ck_cc_data):
    # print(ck_cc_data)
    for i in range(len(ck_cc_data[0])):
        ck_cc_data[0][i] = ck_cc_data[0][i].replace("余票", "剩")
    # print(ck_cc_data)
    if ck_cc_data[0][-1].split("票价")[0] == "无座":
        if ck_cc_data[0][-1].split("剩")[-1] != "无" and ck_cc_data[0][-1].split("剩")[-1] != "候补" and \
                ck_cc_data[0][-2].split("剩")[-1] == "候补" or ck_cc_data[0][-2].split("剩")[-1] == "无":
            ck_cc_data[0][-2] = ck_cc_data[0][-2].split("剩")[0] + "剩" + ck_cc_data[0][-1].split("剩")[-1]
            ck_cc_data[1][-2] = ck_cc_data[1][-1]
            ck_cc_data[0].pop(-1)
            ck_cc_data[1].pop(-1)
        else:
            ck_cc_data[0].pop(-1)
            ck_cc_data[1].pop(-1)
    # print(ck_cc_data)
    return ck_cc_data


if __name__ == '__main__':
    print(data_heard_process_1(['商务座票价42元余票候补', '一等座票价22.5元余票候补', '二等座票价13.5元余票候补', '无座票价13.5元余票无'], False))
    # data_heard_process_1(['软卧票价81.5元余票3', '硬卧票价55元余票候补', '硬座票价9元余票有', '无座票价9元余票有'])
