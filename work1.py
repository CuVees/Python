#!/usr/bin/python
#-*- coding:utf-8 -*-
import smtplib
import datetime
import pymysql
from email.mime.text import MIMEText

mailto_list=['xutao@51jnq.com']




mail_host=""  #设置服务器
mail_user=""  #用户名
mail_pass=""   #口令


mail_cc = [ 'xutao@51jnq.com']


#当前时间
day_now=datetime.date.today()-datetime.timedelta(days=1)
# 当前日期-7
day = datetime.date.today()-datetime.timedelta(days=8)
# 月初
day_from = datetime.date(day.year, day.month, 1)
# 上月最后一天
day_tmp = datetime.date(day.year, day.month, 1) - datetime.timedelta(days=8)
# 上月的今天
try:
    last_month_day = datetime.date(day_tmp.year, day_tmp.month, day.day)
except:
    last_month_day = datetime.date(day_tmp.year, day_tmp.month, day.day-1)
    pass
# 上月的月初
last_month_day_from = datetime.date(day_tmp.year, day_tmp.month, 1)
# 当前日期往前推 31 天
day_pre = datetime.date.today()-datetime.timedelta(days=31)



#发送邮件
def send_mail(to_list,sub,content,cc):  #to_list：收件人；sub：主题；content：邮件内容
    
    me=""
    msg = MIMEText(content,_subtype='html',_charset='utf8')    #创建一个实例，这里设置为html格式邮件
    msg['Subject'] = sub    #设置主题
    msg['From'] = me
    msg['To'] = ";".join(mailto_list)
    msg['CC'] = ";".join(cc)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)  #连接smtp服务器
        s.login(mail_user,mail_pass)  #登陆服务器
        s.sendmail(me, to_list, msg.as_string())  #发送邮件
        s.close()
        return True
    except smtplib.SMTPException:
        print (smtplib.SMTPException)
        return False

def make_html_table(content_list):
    content = '<table border="1" align="center" cellpadding="4" cellspacing="0" bordercolor="#000000"> \n'
    for l in content_list:
        content += '<tr>'
        for data in l:
            if l.index(data) in (1,3,4,5,6,7):
                content += '<td align="center" width="60">' + str(data) + '</td>'
            elif l.index(data) == 2:
                content += '<td align="center" width="60">' + str(data) + '</td>'
            else:
                content += '<td align="center" width="60">' + str(data) + '</td>'
        content += '</tr> \n'
    content += '</table> \n\n'
    return content

def make_html_table_2(content_list,table_name):
    content = '<table border="1" align="center" cellpadding="4" cellspacing="0" bordercolor="#000000"> \n'
    content += '<tr align="center"><td colspan="' + str(len(content_list[0])) + '">'+ table_name +'</td></tr>'
    for l in content_list:
        content += '<tr>'
        for data in l:
            if l.index(data) in (8,10):
                content += '<td width="90"><font size="2px">' + str(data) + '</td>'
            elif l.index(data) == 9:
                content += '<td width="90"><font size="2px">' + str(data) + '</td>'
            else:
                content += '<td width="90"><font size="2px">' + str(data) + '</td>'
        content += '</tr> \n'
    content += '</table> \n\n'
    return content


def getdata(table_name):
    content_list = []
    
    head_1 = ['到账时间\t', '公司id', '公司名字', '放款金额']; 
    content_list.append(head_1)
    
    # link=['月环比','0', '0', '0', '0', '0'] #月环比
    # content_list.append(link)

    # 日期  审核通过率
    sql1 = " select  t1.a_time,t1.id,t2.name,sum(t1.balance) from (SELECT date(arrive_time) as a_time,business_id as id,\
        balance FROM bmdb.tb_credit_record WHERE DATE(arrive_time) >= date('%s') and  DATE(arrive_time) <  date('%s') \
         group by date(arrive_time),id)t1 left join(SELECT  id,name FROM bmdb.tb_lianlian_config  group by id )t2 \
        on  t1.id=t2.id   GROUP BY t1.a_time,t1.id ORDER BY 1 desc; "%(day_from,day_now)
    print(sql1)
    cursor.execute(sql1)
    result1 = cursor.fetchall()

    for data in result1:
        d = str(data[0])
        line = [d, '0', '0', '0']
        if not data[1] == None:
            line[1] = str(data[1])
        if not data[2] == None:
            line[2] = str(data[2])
        if not data[3] == None:
            line[3] = str(data[3])
        
        content_list.append(line)

    # 生成html
    content_1 = make_html_table_2(content_list,table_name)
    return content_1


if __name__ == '__main__':
    # 连接mysql
    conn = pymysql.connect(db="msdb", user="", passwd="", host="", port=) 
    cursor = conn.cursor()

    neirong1=u'<ul style="padding:0 65px"><meta charset="UTF-8"> hi all,相关数据如下:<br/></ul>'
    # print(1)
    # neirong2 = u'<p style="padding:0 65px">ps：类型push之类没有特定时间点和规律的活动，带来的导单量，请相关人员回复本邮件，一周我会汇总一次数据，感谢配合！</p>'
    # print(2)
    content = '<html lang="en"><head><meta charset="UTF-8"><title>title</title></head><body>\n'
    # print(3)
    #报表头部
    content += '<h1 align="center">每日放款-不同公司2</h1>'
    #print(4)
    content += neirong1#.encode('utf-8')
    # getdata表格
    content += getdata('每日放款-不同公司')
    
    #print(5)
    content += '</html>\n\n'

    if send_mail(mailto_list,u"每日放款-不同公司2",content,mail_cc):
        print ('send mail succeed!')
    else:
        send_mail('zhoushibin@51jnq.com',"邮件报表发送失败","邮件报表发送失败",'zhoushibin@51jnq.com')

    cursor.close() 
    conn.close()