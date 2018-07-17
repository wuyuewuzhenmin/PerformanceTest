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
from main import Home1
def get_hashid(uid):
    hash_id = Hashids(alphabet='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123567890', salt='1766',min_length=6)
    hashid = hash_id.encode(uid)
    return hashid


def reph5():
    success = 0
    num_time = 0
    consum_time = 0
    for freq in range(frequency):
        request_time = datetime.datetime.now()

        if method == "get":
            response = requests.get(url=url).content
        else:
            response = requests.post(url=url, data=json.dumps(data), ).content

        try:
            response = json.loads(response)
        except:
            print response
        print url,response

        print request_time


        response_time = datetime.datetime.now()
        print response_time
        print response
        diff_time = (response_time.second- request_time.second)
        print diff_time
        consum_time += diff_time
        success += 1
        num_time += 1
        # print "第 %s 次接口请求成功,耗时 %s " % (str(num_time), str(diff_time))
        print '第%s 次接口请求成功，耗时%s' %(freq,float(diff_time))
    print "运行完毕,成功运行 %s 次,平均耗时 %sS" % (str(success), str(consum_time / success))

if __name__ == '__main__':
    # 运行次数
    frequency=2
    method='get'
    uid=get_hashid(166)
    # frequency=20
    url = "http://activity-test.blued.cn/hd/2018-labor/award/%s" % uid
    # img_url = 'https://www.bldimg.com/hd/2018-joke/15169768-0.9649925221037152.jpg'
    data = {
        'uid': uid
    }

    reph5()


