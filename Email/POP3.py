# Python内置一个poplib模块，实现了POP3协议，可以直接用来收邮件。
# 注意到POP3协议收取的不是一个已经可以阅读的邮件本身，而是邮件的原始文本，这和SMTP协议很像，SMTP发送的也是经过编码后的一大段文本。

# 要把POP3收取的文本变成可以阅读的邮件，还需要用email模块提供的各种类来解析原始文本，变成可阅读的邮件对象。

# 所以，收取邮件分两步：
# 第一步：用poplib把邮件的原始文本下载到本地；
# 第二部：用email解析原始文本，还原为邮件对象。

# 通过POP3下载邮件
# POP3协议本身很简单，以下面的代码为例，我们来获取最新的一封邮件内容：

import poplib

# 输入邮件地址, 口令和POP3服务器地址:
email=input('Email:')
password=input('password:')
POP3_sever=input('POP3_sever:')