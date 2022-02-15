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

**Recruit**

| 字段         | 类型          | 空   | 默认 | 注释         |
| ------------ | ------------- | ---- | ---- | ------------ |
| Rid *(主键)* | int(11)       | 否   |      |              |
| Did_id       | int(11)       | 否   |      |              |
| Rex_l        | varchar(255)  | 否   |      | 经验         |
| Rex_r        | varchar(255)  | 否   |      |              |
| Rdegree      | varchar(255)  | 否   |      | 学历         |
| Rsalary_l    | varchar(255)  | 否   |      | 薪资         |
| Rsalary_r    | varchar(255)  | 否   |      |              |
| Rwelfare     | varchar(5000) | 否   |      | 福利         |
| Rwork        | varchar(500)  | 否   |      | 工作内容     |
| Rscale_l     | varchar(255)  | 否   |      | 公司规模     |
| Rscale_r     | varchar(255)  | 否   |      |              |
| Cid_id       | int(11)       | 否   |      | 城市id       |
| Aid_id       | int(11)       | 否   |      | 区域id       |
| Rfinancing   | varchar(255)  | 否   |      | 公司融资状况 |
| Rjob         | varchar(255)  | 否   |      | 岗位         |
| Rdate        | varchar(255)  | 否   |      | 招聘发布日期 |
| Rcompany     | varchar(255)  | 否   |      | 公司名称     |


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
            ('', 22),   #填写IP地址
            ssh_username="",    # 用户名
            ssh_password="",    # 密码
            remote_bind_address=('', 3306)) as server: # IP地址
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
遍历目标数据，再txt文件中，一个文件有30条目标数据，所以这里循环遍历30次
```python
for x in range(0, 30):
    list = {}
    welfares = []
    jobs = []
    #职位
    list['Rposts'] = "6"

    #经验 & 数据清洗
    exp = dic['data']['list'][x]['workingExp']
    if exp == '无经验':
        exp = "0-0"
    elif exp == '不限':
        exp = "0-0"
    exp = exp.split("-")
    exp[-1] = exp[-1].split("\u5e74")[0]
    if len(exp) == 1:
        exp.append(exp[0])

    list['Rex_l'] = exp[0]
    list['Rex_r'] = exp[1]

    #公司名称
    list['Rcompany'] = dic['data']['list'][x]['companyName']

    #学历
    list['Rdegree'] = dic['data']['list'][x]['education']

    #薪资 & 数据清洗
    salary = dic['data']['list'][x]['salary60']
    k = salary.replace('\u5343', 'k').replace('\u4e07', 'w')
    s2 = k.split("-")
    left = s2[0]
    right = s2[-1]
    if left[-1] == 'w':
        left = str(int(float(left.split('w')[0])*10)) + 'k'
    if right[-1] == 'w':
        #先去掉数列元素的w，然后将str型转为float型，转换单位乘以10，加上k符号，最后再转为str型
        #这里有个坑，数列中的元素不能直接转为float型，要明确数组元素位置，比如x[0]
        right = str(int(float(right.split('w')[0])*10)) + 'k'
    list['Rsalary_l'] = left
    list['Rsalary_r'] = right

    #福利
    welfare = dic['data']['list'][x]['welfareLabel']
    for j in range(len(welfare)):
        welfares.append(dic['data']['list'][x]['welfareLabel'][j]['value'])
    list['Rwelfare'] = ",".join(welfares)

    #工作范畴
    list['Rwork'] = dic['data']['list'][x]['name']

    #公司规模  & 数据清洗
    scale = dic['data']['list'][x]['companySize']
    if scale == '1000人以上':
       scale = "1000-1500人"
    elif scale == '10000人以上':
        scale = "10000-12000人"
    elif scale == "20人以下":
        scale = "10-20人"
    elif scale == '':
        scale = "50-100人"
    scales = scale.split("-")
    replace_scalce = scales[1].replace('人', '')
    scales[1] = replace_scalce
    list['Rscale_l'] = scales[0]
    list['Rscale_r'] = scales[1]

    #城市
    list['Rcity'] = '1'

    #行政区
    dictrists = dic['data']['list'][x]['cityDistrict']
    if dictrists == '':
        dictrists = '天河区'
    district = {
        '天河区': '1',
        '番禺区': '2',
        '白云区': '3',
        '黄埔区': '4',
        '花都区': '5',
        '从化区': '6',
        '增城区': '7',
        '海珠区': '8',
        '越秀区': '9',
        '荔湾区': '10',
        '南沙区': '11',
    }
    list['Rdistrict'] = district.get(dictrists)
    #融资(经验模式）
    list['Rfinancing'] = dic['data']['list'][x]['property']
    #职位描述
    Rjob = dic['data']['list'][x]['skillLabel']
    for i in range(len(Rjob)):
        jobs.append(dic['data']['list'][x]['skillLabel'][i]['value'])
    list['Rjob'] = ','.join(jobs)
    #发布时间
    date = dic['data']['list'][x]['publishTime']
    list['Rdate'] = date[0:10]
    print(list)

```
最后将数据插入
```python
cursor = conn.cursor()
info = """INSERT INTO Recruit(Did_id,Rex_l,Rex_r,Rdegree,Rsalary_l,
    Rsalary_r,Rwelfare,Rwork,Rscale_l,Rscale_r,
    Rcompany,Cid_id,Aid_id,Rfinancing,Rjob,Rdate) 
    VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',
    '%s','%s','%s','%s','%s','%s')""" \
           % (
               list['Rposts'],
               list['Rex_l'],
               list['Rex_r'],
               list['Rdegree'],
               list['Rsalary_l'],
               list['Rsalary_r'],
               list['Rwelfare'],
               list['Rwork'],
               list['Rscale_l'],
               list['Rscale_r'],
               list['Rcompany'],
               list['Rcity'],
               list['Rdistrict'], 
               list['Rfinancing'],
               list['Rjob'],
               list['Rdate'],
           )
cursor.execute(info)
conn.commit()                     
```

### END

运行之后，数据就传到了MySQL上，有了数据源，之后便可以用来做数据可视化了