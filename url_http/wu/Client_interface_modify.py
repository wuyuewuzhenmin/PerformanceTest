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



def mainaa(online,number,method,path_url,data):
    success = 0
    num_time = 0
    consum_time = 0
    listaaa=[]
    # list_users = ['3@qq.com', '666666']
    list_users=['livescf17@qq.com','1']
    # list_users = ['ldq104@163.com', '111111']
    username = list_users[0]
    password = list_users[1]
    for a in range(number):
        print 'pasteer'

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
            # url = ONLINE_HTTP_HOST + path_url
            if method == "get":

                response = requests.get(url=url, headers=headers, verify=False).content

            else:
                response = requests.post(url=url, data=json.dumps(data), headers=headers, verify=False).content

            try:
                response = json.loads(response)
                # print JsonFormatter(json_data=response).render()
            except:
                # print responses
                # print '解析失败： ', response
                print JsonFormatter(json_data=response).render()

                break

            print response

            code = int(response['code'])


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
                aa= "第 %s 次接口请求成功,耗时 %s " % (a, str(diff_time))
                # print aa
            else:
                success += 1
                num_time += 1
                print "第 %s 次接口code请求失败,错误信息 %s " % (a, str(response))
                aa = u"第 %s 次接口code请求失败,错误信息 %s " % (a, str(response))
                # return aa
    # print success

    print "运行完毕,成功运行 %s 次,平均耗时 %sS" % (str(success), str(float(consum_time/success)))
    bb = u"运行完毕,成功运行 %s 次,平均耗时 %sS" % (str(success), str(float(consum_time/success)))

    return aa.decode('utf-8')+'\n'+bb.decode('utf-8')


    # return join.(aa,bb)
        # time.sleep(4)


# if __name__ == '__main__':
#     number=
#     # anchor_id = 9334224
#     method = "get"
#     path_url = "http://106.75.100.161/ticktocks/me"
#
#     data={"hit_id":1528177649,
#          "pay_token":"f660e492-5b162264618f56-63575664-2ec61961",
#          "count":1,
#          "live_id":"149929",
#          "target_uid":"9335535",
#          "contents":"",
#          "discount_id":"",
#          "goods_id":"1917"}
#
#
#
#     main()

# mainaa(2,'get',"http://106.75.100.161/ticktocks/me",'')