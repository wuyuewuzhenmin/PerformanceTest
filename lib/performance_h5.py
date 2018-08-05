# -*-coding:utf8-*-
# 性能测试基类
import re
import time
import requests
import threading
import json
import threadpool



class Performance(threading.Thread):
# class Performance(threadpool.ThreadPool):
#     def __init__(self, url="", method="get", header={},  body_type="data"):
    def __init__(self, url="", method="get", body_type="data"):
        threading.Thread.__init__(self)
        # threadpool.ThreadPool.__init__(self)
        self.url = url
        self.method = method
        # self.header = header
        # self.body = body
        self.body_type = body_type

    # def run(self):
    #     self.test_performance()

    def test_performance(self):
        start_time = time.time()
        try:
            response = self.send_request()
            a=response.content
            b=json.loads(a)
            print 'aaaaa:'+a
            if b['code'] == 200:
            # if response.status_code == 200:
                status = "success"
            else:
                status = "fail"
        except Exception, e:
            print e
            status = "except"
        end_time = time.time()
        spend_time = end_time - start_time
        return status, spend_time

    def send_request(self):
        if re.search(self.method, 'GET', re.IGNORECASE):
            response = requests.get(self.url)
            # response = requests.get(self.url)
            print "self.s:"+self.url
        else:
            if self.body_type == "json":
                response = requests.post(self.url, json=self.body)
            elif self.body_type == "file":
                response = requests.post(self.url, files=self.body)
            elif self.body_type == "data":
                response = requests.post(self.url, data=self.body)

        return response


    def get_percent_time(data_list, percent):
        data_list = sorted(data_list)
        if len(data_list) * (1 - percent) <= 1:
            r_length = 1
        else:
            r_length = len(data_list) * (1 - percent)
            r_length = int(round(r_length))
        data_list = data_list[:len(data_list) - r_length]
        return data_list[-1]