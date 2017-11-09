#-*- coding:utf-8 -*-
#!/usr/bin/python
import smtplib
import datetime
import pymsql
from email.mime.text import MIMEText


mail_to_list=['xutao@1234.com']

mial_host='' # 设置服务器
mail_user='' # 登录名
mail_pass='' # 登录密码

mail_cc='xuaot@212.com'

# 当前时间
day_now=datetime.date.today()-datetime.timedelta(days=1)
# 当前日期-7
day=datetime.date.today()-datetime.timedelta(days=7)
# 月初
day_from=datetime.date(day.year,day.month,1)
