import smtplib
from email.mime.text import MIMEText


def mail(user_email, text, user_name_list):
    my_sender = '1500536201@qq.com'  # 填写发信人的邮箱账号
    my_pass = 'gqpqszvgerbdhcch'  # 发件人邮箱授权码
    my_user = user_email  # 收件人邮箱账号
    try:
        msg = MIMEText("乘客"+str(user_name_list)+"的"+text, 'plain', 'utf-8')  # 填写邮件内容
        msg['From'] = my_sender  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = my_user  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "抢票状态"  # 邮件的主题，也可以说是标题
        server = smtplib.SMTP_SSL("smtp.qq.com", 465, 'utf-8')  # 发件人邮箱中的SMTP服务器
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱授权码
        server.sendmail(my_sender, my_user, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except smtplib.SMTPDataError:
        print(f"乘客{str(user_name_list)}的票:收件人可能包含不存在的帐户，请检查收件人地址")
        return f"乘客{str(user_name_list)}的票:收件人可能包含不存在的帐户，请检查收件人地址"
    except smtplib.SMTPRecipientsRefused:
        print(f"乘客{str(user_name_list)}的票:错误的地址合成")
        return f"乘客{str(user_name_list)}的票:错误的地址合成"
    except Exception as e:
        print(e)
        return e
    else:
        print(f"乘客{str(user_name_list)}的票:购票(抢票)成功，请在规定时间缴费")
        return f"乘客{str(user_name_list)}的票:购票(抢票)成功，请在规定时间缴费"


if __name__ == '__main__':

    mail("2576210620@qq.com", "22222", "1111")

