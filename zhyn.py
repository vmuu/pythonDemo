# coding:utf-8
import os
import datetime
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

import requests
import json

def print_hi():
    headerQ = {
        "Host": "hqjt.ynau.edu.cn",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2012K11C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4317 MMWEBSDK/20220903 Mobile Safari/537.36 MMWEBID/6597 MicroMessenger/8.0.28.2240(0x28001C53) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Cookie": "ASPSESSIONIDSSRASQRD=OCIECHPAGJLKGLIAAGJEEDJI",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    url = 'http://hqjt.ynau.edu.cn/yjsmis2/comm/api.asp?cmd=login&tp=wx&openid=okYuw1LhJQNrJD3khygsdJTF2iqo&uid=2022601787&name=%e6%9d%a8%e6%98%8e%e9%87%91&dep=%e5%a4%a7%e6%95%b0%e6%8d%ae%e5%ad%a6%e9%99%a2&tm=2023-06-29+17%3a07%3a22&url=%2fhq%2fredirect.aspx&mac=31E5805B2DC8B2900B07CED9230E48AD'
    request = requests.get(url, headerQ, allow_redirects=False)
    html_set_cookie = requests.utils.dict_from_cookiejar(request.cookies)
    print(str(html_set_cookie))
    daCardHeaders = {
        "Host": "hqjt.ynau.edu.cn",
        "Connection": "keep-alive",
        "Content-Length": "465",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Origin": "http://hqjt.ynau.edu.cn",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Linux; Android 12; M2012K11C Build/SKQ1.220303.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4317 MMWEBSDK/20220903 Mobile Safari/537.36 MMWEBID/6597 MicroMessenger/8.0.28.2240(0x28001C53) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "X-Requested-With": "com.tencent.mm",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    daCard = {
        "go": 1,
        "t2": 0,
        "t1": 2,
        "addr": "云南省昆明市盘龙区7204公路",
        "nation": "中国",
        "city": "昆明市",
        "province": "云南省",
        "district": "盘龙区",
        "street": "7204公路",
        "lat": 25.128922,
        "lon": 102.74599
}
    daCardGET = requests.post(
        'http://hqjt.ynau.edu.cn/yjsmis2/Query/StudentPost.asp?sid=2022601787', headers=daCardHeaders,
        allow_redirects=False, data=daCard,cookies=html_set_cookie)
    print(daCardGET.status_code)
    print(daCardGET.content)

    textHtmlRe = 'Log:\n' + datetime.datetime.now().strftime(
        '%Y年%m月%d日 %H时%M分%S秒') + '\n' + '结果码：' + str(
        daCardGET.status_code) + '\n***************************************'
    textss = ''
    if os.path.exists('SchoolClockLog.txt'):  # 文件读写
        myFile = open("SchoolClockLog.txt", "r")  # 设置文件对象
        dataRead = myFile.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
        myFile.close()
        if dataRead:
            for item in range(len(dataRead)):
                textss += dataRead[item]
            with open('SchoolClockLog.txt', 'w') as f:
                f.write(
                    textss + '\n' + datetime.datetime.now().strftime(
                        '%Y年%m月%d日 %H时%M分%S秒') + '\n' + '结果码：' + str(
                        daCardGET.status_code) + '\n***************************************')
    else:
        with open('SchoolClockLog.txt', 'w') as f:
            f.write(textHtmlRe)
    # 发邮件
    my_sender = 'ynkmghz616@163.com'  # 发件人邮箱账号
    my_pass = 'ZURMTAOLVXGMZKNT'  # 发件人邮箱授权码
    my_user = '68872185@qq.com'  # 收件人邮箱账号，我这边发送给自己

    def mail():
        ret = True
        mail_msg = textHtmlRe
        try:
            msg = MIMEText(mail_msg, 'plain', 'utf-8')
            msg['From'] = formataddr(["云南农业大学健康打卡提醒", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["FK", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = "你的健康打卡程序运行成功，结果如下："  # 邮件的主题，也可以说是标题
            server = smtplib.SMTP_SSL("smtp.163.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            ret = False
        return ret

    ret = mail()
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")


if __name__ == '__main__':
    print_hi()
