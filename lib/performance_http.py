## encoding: utf-8
# 性能测试基类
import re
import time
import requests
import threading
import json



class Performance(threading.Thread):
    def __init__(self, url="", method="", header={},body_type =""):
        threading.Thread.__init__(self)
        self.url = url
        self.method = method
        self.header = header
        self.data = body_type

    def get_percent_time(data_list, percent):
        data_list = sorted(data_list)
        if len(data_list) * (1 - percent) <= 1:
            r_length = 1
        else:
            r_length = len(data_list) * (1 - percent)
            r_length = int(round(r_length))
        data_list = data_list[:len(data_list) - r_length]
        return data_list[-1]

    def test_performance(self):

        try:
            responsess = self.send_request()
            b= json.loads(responsess)
            c=int(b["code"])
            # print responsess
            print b
            # if b["code"] == 200:
            if c == 200:
                status = "success"
                print 'aaaaaa'
            else:
                status = "fail"
                print 'status'
        except Exception, e:
            print e
            status = "except"
        # end_time = time.time()
        # spend_time = end_time - start_time
        request_time = b['request_time']
        print type(request_time)
        response_time = b['response_time']
        print response_time, request_time
        spend_time = float(response_time) - float(request_time)
        return status, spend_time

    def send_request(self):

        if self.method == 'GET':
            response = requests.get(self.url, headers=self.header).content
            print "self.s:" + self.url
        else:
            response=requests.post(self.url,data=json.dumps(self.data),headers=self.header).content
            # response = requests.post(self.url, data=self.data, headers=self.header).content
            print 'surl:'+self.url

        return response