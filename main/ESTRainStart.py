import argparse
import selen


parser = argparse.ArgumentParser(description='api抢票或者买票')
parser.add_argument('UserAccount', type=int, help='用户账号')
parser.add_argument('UserPassword', type=int, help='用户密码')
parser.add_argument('FromStation', type=str, help='出发地')
parser.add_argument('ToStation', type=str, help='目的地')
parser.add_argument('Date', type=str, help='日期(2023-05-05)')
parser.add_argument('UserName', type=str, help='用户名(买票人姓名)')
# parser.add_argument('-a', action='store_true')
args = parser.parse_args()
print(args)

browser = selen.paData()
browser.browser_pa(departure=args.FromStation, destination=args.ToStation, date=args.Date)
tr, len_tr = browser.pa()
datas = []
for td in browser.tr:
    data_list = browser.pa_data(td)
    data = []
    for i in range(len(data_list[0])):
        if data_list[0][i] != "--":
            data.append(data_list[0][i])
    print(data)
    datas.append(data)

input("车次>>")

