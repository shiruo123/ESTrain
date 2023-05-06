import smtplib
from email.mime.text import MIMEText


def mail(user_email):
    my_sender = '2576210620@qq.com'  # 填写发信人的邮箱账号
    my_pass = 'iptsvsgximpaeajc'  # 发件人邮箱授权码
    my_user = user_email  # 收件人邮箱账号
    ret = True
    try:
        msg = MIMEText('抢票成功，请在20分钟内付钱', 'plain', 'utf-8')  # 填写邮件内容
        msg['From'] = my_sender  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = my_user  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "抢票状态"  # 邮件的主题，也可以说是标题
        server = smtplib.SMTP_SSL("smtp.qq.com", 465, 'utf-8')  # 发件人邮箱中的SMTP服务器
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱授权码
        server.sendmail(my_sender, my_user, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret
