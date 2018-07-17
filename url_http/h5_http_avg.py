# encoding: utf-8

'''''
1.h5多次请求平均响应时间
2.get请求，修改url即可
3.frequency:修改运行次数
'''''
import requests
import json
import datetime
from hashids import Hashids
# from lib.hashid import get_hashid

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

def get_hashid(uid):
    hash_id = Hashids(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123567890', salt='1766',min_length=6)
    hashid = hash_id.encode(uid)
    return hashid


def reph5(frequency,method,url,data):
    listaaa=['']
    success = 0
    num_time = 0
    consum_time = 0
    print frequency,method,url

    if method == "GET":
        print '该接口是get接口'
        try:
            for freq in range(frequency):
                request_time = datetime.datetime.now()
                print request_time
                # response = requests.get(url=url).content
                response = requests.get(url=url)
                #请求后时间
                response_time = datetime.datetime.now()
                print response_time
                response1 = response.content
                #打印状态码
                response_code =response.status_code
                print response_code
                diff_time = (response_time.second- request_time.second)
                print diff_time
                consum_time += diff_time
                success += 1
                num_time += 1
                print '第%s 次接口请求成功，耗时%s' %(freq+1,float(diff_time))
                aa= '第%s 次接口请求成功，耗时%s' %(freq+1,float(diff_time))
                listaaa.append(aa+'\n')
            # aa = str(listaaa).decode('string_escape')
            aa=" ".join(listaaa)
            # print aa
            print "运行完毕,成功运行 %s 次,平均耗时 %sS" % (str(success), str(consum_time / success))
            bb= "运行完毕,成功运行 %s 次,平均耗时 %sS" % (str(success), str(consum_time / success))
            # print 'bbbb'+bb
            return aa.decode('utf-8')+ '\n'+bb.decode('utf-8')
        except:
            bb = '请输入正常的接口'
            print bb
            return bb.decode('utf-8')

    else:
        print '该接口是post接口'
        print data,type(data)
        data = json.loads(data)
        data = json.dumps(data)
        try:
            for freq in range(frequency):
                request_time = datetime.datetime.now()
                print request_time
                # response = requests.post(url=url, data=json.dumps(data), ).content
                response = requests.post(url=url, data=data)
                # response = json.loads(response)
                #请求后时间
                response_time = datetime.datetime.now()
                print response_time
                #打印状态吗
                response_code = response.status_code
                print response_code
                diff_time = (response_time.second- request_time.second)
                print diff_time
                consum_time += diff_time
                success += 1
                num_time += 1
                # aa = '第%s 次接口请求成功，耗时%s' % (freq+1, float(diff_time))
                # listaaa.append(aa)
                print '第%s 次接口请求成功，耗时%s' %(freq+1,float(diff_time))
                aa= '第%s 次接口请求成功，耗时%s' %(freq+1,float(diff_time))
                listaaa.append(aa+'\n')
            aa=" ".join(listaaa)
            print "运行完毕,成功运行 %s 次,平均耗时 %sS" % (str(success), str(consum_time / success))
            bb= "运行完毕,成功运行 %s 次,平均耗时 %sS" % (str(success), str(consum_time / success))
            # print 'bbbb'+bb
            return aa.decode('utf-8')+ '\n'+bb.decode('utf-8')
        except:
            bb = '请查看输入的内容'
            print bb
            return bb.decode('utf-8')

