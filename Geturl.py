#-*- coding=utf-8 -*-

import json
import re
import pymysql
import sshtunnel
import pymysql
from sshtunnel import SSHTunnelForwarder
class spider():
    def __init__(self):
        print("init")

    def started(self):
            for i in range(1):
                file = open("D:/Scrapy Project/geturl/python/"+ str(i) +".TXT", 'r', encoding='UTF-8')
                js = file.read()
                dic = json.loads(js)
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


                    print("---------i",i)
                    for x in range(0, 30):
                        print("-----------------x",x)
                        list = {}
                        welfares = []
                        jobs = []
                        #职位
                        list['Rposts'] = "6"
                        #经验 & 数据清洗
                        # list['Rex'] = dic['data']['list'][x]['workingExp']
                        exp = dic['data']['list'][x]['workingExp']
                        if exp == '无经验':
                            exp = "0-0"
                        elif exp == '不限':
                            exp = "0-0"

                        exp = exp.split("-")
                        exp[-1] = exp[-1].split("\u5e74")[0]
                        if len(exp) == 1:
                            print('----------------------')
                            exp.append(exp[0])

                        list['Rex_l'] = exp[0]
                        list['Rex_r'] = exp[1]
                        # print(exp)
                        # print(list['Rex_l'])
                        # print(list['Rex_r'])

                        #公司名称
                        list['Rcompany'] = dic['data']['list'][x]['companyName']
                        # print(list['Rcompany'])
                        #学历
                        list['Rdegree'] = dic['data']['list'][x]['education']

                        #薪资 & 数据清洗
                        salary = dic['data']['list'][x]['salary60']
                        k = salary.replace('\u5343', 'k').replace('\u4e07', 'w')
                        s2 = k.split("-")
                        left = s2[0]
                        right = s2[-1]
                        if left[-1] == 'w':
                            # s2 = re.search('(\d+(\.\d+)?)',left).group()
                            # s3 = float(str(s2[0]))
                            left = str(int(float(left.split('w')[0])*10)) + 'k'
                            # s2[0] = left
                        if right[-1] == 'w':
                            #先去掉数列元素的w，然后将str型转为float型，转换单位乘以10，加上k符号，最后再转为str型
                            #这里有个坑，数列中的元素不能直接转为float型，要明确数组元素位置，比如x[0]
                            right = str(int(float(right.split('w')[0])*10)) + 'k'
                            # s2[-1] =right
                        list['Rsalary_l'] = left
                        list['Rsalary_r'] = right
                        # print(k) #1.2w-1.7w
                        # print(left) # 12k
                        # print(right) # 17k
                        # print(s2) # ['12k', '17k']
                        # print(salary) # 1.2万-1.7万


                        #福利
                        welfare = dic['data']['list'][x]['welfareLabel']
                        for j in range(len(welfare)):
                            welfares.append(dic['data']['list'][x]['welfareLabel'][j]['value'])
                        list['Rwelfare'] = ",".join(welfares)
                        # print(list['Rwelfare'])


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
                        # print 'scales' result : 500-999人
                        # print 'scales[1]' result : 999人
                        #
                        replace_scalce = scales[1].replace('人', '')
                        # print(replace_scalce)
                        # print(scales)
                        scales[1] = replace_scalce
                        # # print(scales) # result: ['20', '99']
                        # print(scales[0]) #10000
                        # print(scales[1]) #12000
                        # list['Rscale'] = ','.join(scales)
                        list['Rscale_l'] = scales[0]
                        list['Rscale_r'] = scales[1]

                        #公司名称
                        # list['Rcompany'] = dic['data']['list'][x]['companyName']
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

                        # print(district.get(dictrists))
                        list['Rdistrict'] = district.get(dictrists)
                        # print(list['Rdistrict'])



                        #详细地址
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
                        # print(type(list))
                        # print(type(list['Rjob']))
                        # print(type(list['Rwelfare']))


                        # info = """INSERT INTO Recruit(Did_id,Rex_l,Rex_r,Rdegree,Rsalary_l,Rsalary_r,Rwelfare,Rwork,Rscale_l,Rscale_r,Rcompany,Cid_id,Aid_id,Rfinancing,Rjob,Rdate) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')""" \
                        #        % (
                        #            list['Rposts'], #Did_id_id
                        #            list['Rex_l'],
                        #            list['Rex_r'],
                        #            list['Rdegree'],
                        #            list['Rsalary_l'],
                        #            list['Rsalary_r'],
                        #            list['Rwelfare'],
                        #            list['Rwork'],
                        #            list['Rscale_l'],
                        #            list['Rscale_r'],
                        #            list['Rcompany'],
                        #            list['Rcity'],#Cid_id_id
                        #            list['Rdistrict'], #Aid_id_id
                        #            list['Rfinancing'],
                        #            list['Rjob'],
                        #            list['Rdate'],
                        #
                        #        )
                        # cursor.execute(info)
                        # conn.commit()
                        # print('insert succeed')

if __name__ =="__main__":
   spider = spider()
   spider.started()


