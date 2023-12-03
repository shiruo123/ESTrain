import requests
from lxml import etree
import pymysql


def save(table, data):
    try:
        print(f"insert into {table} values {tuple(data)};")
        cursor.execute(f"insert into {table} values {tuple(data)};")
        db.commit()
    except:
        print("失败")


db = pymysql.connect(host="119.29.244.36", user="youthrefuel", password="dsq171007", port=3306, database="bysj")
cursor = db.cursor()

url = "http://cooco.net.cn/zuowen/516098.html"
response = requests.get(url)

tree = etree.HTML(response.text)
a = []
c = []
s = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
ps = tree.xpath("//p")
ps.pop(0)
ps = [i.text for i in ps]
# print(ps)
for p in ps:
    if p[0] in s:
        if len(a) != 0:
            c.append(a)
        a = []
        p = p.split(".")[-1]
    a.append(p)

s = 0
g = 0
for k, i in enumerate(c):
    if len(i) == 5:
        continue
        s += 1
        t = ""
        for x, j in enumerate(i):
            # print(j[-5:-1])
            if j[-5:-1] == "正确答案":
                i[x] = i[x][0:-6]
                t += i[x][0]
        i.append(t)
        i.insert(0, s)
        # print(i)
        save('app1_TiKu_xzt', i)
    if len(i) == 4:
        s += 1
        for x, j in enumerate(i):
            # print(j[-5:-1])
            if j[-5:-1] == "正确答案":
                i[x] = i[x][0:-6]
                i.append(i[x][0])
        i.insert(0, s)
        if len(i) == 6:
            # continue
            g += 1
            i.pop(0)
            i.insert(0, g)
            save('app1_TiKu_xzt1', i)
        elif len(i) == 5:
            continue
            g += 1
            i.pop(0)
            i.insert(0, g)
            i[-1] = i[-1].split("：")[-1]
            save("app1_TiKu_pdt", i)





