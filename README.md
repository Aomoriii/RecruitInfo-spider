## python:将txt文本数据传到MySQL

python可以通过打开指定的文件，读取文件的数据，因此我想用python读取txt文件，然后再将数据传到mysql上

> 前提条件

*  远程mysql（这里用到的是服务器里的MySQL，非本地）
*  txt文本数据（已在本项目文件中)
*  需要在MySQL中设计数据库表

### 库表设计

> 数据模型图

![image](https://github.com/Aomoriii/RecruitInfo-spider/blob/main/static/img/table.png?raw=true)

> 数据字典

> 部分数据字段解释

### 代码

打开txt文件所在路径
```python
import json

def started():
    # 循环打开文件
    for i in range(3):
        file = open("D:/Scrapy Project/geturl/python/"+ str(i) +".TXT", 'r', encoding='UTF-8')
        js = file.read()
        dic = json.loads(js)    #将JSON格式的字符串反序列化为 Python 对象
```

连接远程MySQl
```python
import pymysql
from sshtunnel import SSHTunnelForwarder
def started():
    with SSHTunnelForwarder(
            ('', 22),
            ssh_username="",
            ssh_password="",
            remote_bind_address=('', 3306)) as server:
        print('SSH连接成功')

        conn = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                               port=server.local_bind_port,
                               user='RecruitInfo',
                               passwd='RecruitInfo',
                               db='recruitinfo')

        print('mysql数据库连接成功')

        cursor = conn.cursor()
        print('游标获取成功')
```

