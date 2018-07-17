# encoding: utf-8
"""
多次请求一个接口，取平均时间
弯豆余额
"""
import sys
import requests
import json
import time

sys.path.append('../../')
from lib.ia_token import GetHeader
from lib.setting import *
from lib.json_formatter import JsonFormatter
from lib.dispose_redis import RedisDb



def mainaa(online,number11,method,path_url,data):
    success = 0
    num_time = 0
    consum_time = 0
    listaaa=['']
    # list_users = ['3@qq.com', '666666']
    list_users=['livescf17@qq.com','1']
    # list_users = ['ldq104@163.com', '111111']
    username = list_users[0]
    password = list_users[1]
    if online == "测试环境":
        headers = GetHeader(username=username, password=password, user_agent=USER_AGENT_IOS,
                            http_host=TEST_HTTP_HOST).header_auth()
        # headers = GetHeader(username=username, password=password, user_agent=USER_AGENT_IOS,
        #                     http_host=ONLINE_HTTP_HOST).header_auth()
    else:
        headers= GetHeader(username='ldq104@163.com', password='111111', user_agent=USER_AGENT_IOS,
                               http_host=ONLINE_HTTP_HOST).header_auth()

    if headers['Authorization'] is not False:
        # url = TEST_HTTP_HOST + path_url
        url=path_url
        print  'method是：',method,type(method),url
        # url = ONLINE_HTTP_HOST + path_url
        if method == "GET":
            print '为get请求'
            try:
                for a in range(number11):
                    response = requests.get(url=url, headers=headers, verify=False).content
                    response = json.loads(response)
                    code = int(response['code'])
                    print 'code是：',code
                    if code == 200:
                        request_time = response['request_time']
                        response_time = response['response_time']
                        print response_time, request_time
                        diff_time = response_time - request_time
                        print diff_time
                        consum_time += diff_time
                        success += 1
                        num_time += 1
                        # print "第 %s 次接口请求成功,耗时 %s " % (a, str(diff_time))
                        aa= "第 %s 次接口请求成功,耗时 %s " % (a+1, str(diff_time))
                        listaaa.append(aa+'\n')
                        # print aa
                    else:
                        success += 1
                        num_time += 1
                        print "第 %s 次接口code请求失败,错误信息 %s " % (a+1, str(response))
                        aa = "第 %s 次接口code请求失败,错误信息 %s " % (a+1, str(response))
                        listaaa.append(aa+'\n')
                aa=" ".join(listaaa)
                print "运行完毕,成功运行 %s 次,平均耗时 %sS" % (str(success), str(float(consum_time/success)))
                bb = "运行完毕,成功运行 %s 次,平均耗时 %sS" % (str(success), str(float(consum_time/success)))
                return aa.decode('utf-8')+'\n'+bb.decode('utf-8')
            except:
                bb = '请检查输入的get请求是否正常'
                print bb
                return bb.decode('utf-8')
        else:
            print '请求是post请求'
            try:
                print method,path_url,data,type(data)
                data = json.loads(data)
                data = json.dumps(data)
                print data
                for a in range(number11):
                    response = requests.post(url=url, data=data, headers=headers, verify=False).content
                    response = json.loads(response)
                    print 'respomse是：',response
                    code = int(response['code'])
                    print code
                    if code == 200:
                        request_time = response['request_time']
                        response_time = response['response_time']
                        print response_time, request_time
                        diff_time = response_time - request_time
                        print diff_time
                        consum_time += diff_time
                        success += 1
                        num_time += 1
                        # print "第 %s 次接口请求成功,耗时 %s " % (a, str(diff_time))
                        aa= "第 %s 次接口请求成功,耗时 %s " % (a+1, str(diff_time))
                        listaaa.append(aa+'\n')
                    else:
                        success += 1
                        num_time += 1
                        print "第 %s 次接口code请求失败,错误信息 %s " % (a+1, str(response))
                        aa = "第 %s 次接口code请求失败,错误信息 %s " % (a+1, str(response))
                        listaaa.append(aa+'\n')
                aa=" ".join(listaaa)
                print "运行完毕,成功运行 %s 次,平均耗时 %sS" % (str(success), str(float(consum_time/success)))
                bb = "运行完毕,成功运行 %s 次,平均耗时 %sS" % (str(success), str(float(consum_time/success)))
                return aa.decode('utf-8')+'\n'+bb.decode('utf-8')
            except:
                bb = '请检查输入请求信息'
                print bb
                return bb.decode('utf-8')