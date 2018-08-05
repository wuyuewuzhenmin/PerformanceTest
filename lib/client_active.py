# encoding: utf-8
"""
    __auth__: 焦淑鹏
    __require__: 模拟客户端,与它端进行交互
    __version__: 无要求
"""
import socket
import ssl
import threading
import msgpack
import time
import sys
import datetime

from convert import Convert
from ..message_type import Message
from ..json_formatter import JsonFormatter
from ..setting import path


# from ..logger import Log


class ClientIM:
    def __init__(self, **kwargs):
        # 设置聊天host和port
        self.config = kwargs.get("parameter")
        self.uid = self.config['user_info']['uid']
        self.message = kwargs.get('message')
        self.chat_host = self.config['host']
        self.chat_port = 8080
        self.classCon = Convert(config=self.config)
        self.num = 10
        self.protocol = self.message['protocol']
        # self.log = Log()
        if '--verbose' in sys.argv:
            self.verbose = True
        else:
            self.verbose = False
        if self.chat_host[0] != 'h':
            self.is_online = 1
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.is_online = 0
            self.sock = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
        self.sock.connect((self.chat_host, self.chat_port))

    def socket_im(self):
        try:
            send_data = self.classCon.arrays_comb(0b00011001)
            if send_data == 0:
                return
            # 定义鉴权包
            self.sock.send(bytearray(send_data))
            # 发送鉴权包
            reply = self.sock.recv(16)
            get_header = self.header_byte(reply)
            # 获取鉴权头
            if get_header == '00010010':  # 判断鉴权是否成功
                print '鉴权成功'
                threads = []
                # 发送消息
                send_msg = threading.Thread(target=self.send_msg, args=())
                threads.append(send_msg)
                # 接收消息
                # 后期需要释放------------************------------
                rec_msg = threading.Thread(target=self.rec_msg, args=())
                threads.append(rec_msg)
                # self.sync()
                for thread in threads:
                    thread.setDaemon(False)
                    thread.start()
                thread.join()
            else:
                print '连接断开'
                return False
        finally:
            self.sock.close()

    @staticmethod
    def header_byte(reply):  # 解析头部
        get_reply = bytearray(reply)
        head = bin(get_reply[0]).replace('0b', '').zfill(8)
        return head

    def ping_byte(self, reply):
        header = reply[0]
        if header == '00101001':  # 心跳包只包含头
            try:
                data_byte = []
                for num in range(8):
                    data = bin(reply[num]).replace('0b', '').zfill(8)
                    data_byte.append(data)
                version = self.montage(data_byte[1])
                message_len = self.montage(data_byte[2:6])
                ping_time = self.montage(data_byte[6:8])
                print '接收到服务器发送的心跳包,心跳包版本为%d,消息体长度为%d,间隔时间为%d秒' % (version, message_len, ping_time)
            except:
                # pass
                print '接收到服务器发送的心跳包,心跳包仅包含header'
        elif header == '00111010':  # 消息送达成功
            if len(reply) == 23:
                header = reply[0]
                version = int(reply[1], 2)
                msg_lenth = int(''.join(reply[2:6]), 2)
                res = int(reply[6], 2)
                local_id = int(''.join(reply[7:11]), 2)
                if res == 0:
                    print '消息成功送达,header为%s, 版本为%s, 消息长度为%s, local ID为%s' % (header, version, msg_lenth, local_id)
                else:
                    print '消息送达失败, header为%s, 版本为%s, 消息长度为%s' % (header, version, msg_lenth)
            else:
                error_code = int(reply[6], 2)
                print Message().send_error_code(error_code)

        elif header == '00100001':
            # print '接收到服务器不带有payloads PING'
            ping_data = bytearray(self.classCon.ping(1))
            self.sock.send(ping_data)
        elif header == '01111010':
            self.return_req(reply)
        else:
            self.msg_type_push(reply)

    @staticmethod
    def montage(values):
        if type(values) == str:
            result = values
        else:
            result = ''.join(values)
        res = int(result, 2)
        return res

    def send_msg(self, robot=False):
        if "is_robot" in self.message.keys():
            if robot is True:
                msg_data = bytearray(self.classCon.send_protocol(self.message))
                self.sock.send(msg_data)
        else:
            while True:
                if self.protocol == 'send':
                    contents = raw_input("请输入发送内容:\n")
                    self.message['contents'] = contents
                    msg_data = bytearray(self.classCon.send_protocol(self.message))
                elif self.protocol == 'req':
                    msg_data = bytearray(self.classCon.req_protocol(self.message))
                else:
                    print "消息发送失败"
                    msg_data = None
                if msg_data is not None:
                    self.sock.send(msg_data)
                    if self.protocol == 'req':
                        break
                else:
                    break

    # 异常关闭socket
    def sign_out(self):
        self.sock.shutdown(2)
        self.sock.close()

    def rec_msg(self):
        while True:
            try:
                recv_data = self.recv_basic()
            except Exception, e:
                if e.args[0] == 9:
                    print "关闭socket"
                break
            try:
                header = recv_data[0]
            except:
                # print recv_data
                break
            if header == '00101001':
                self.ping_byte(recv_data)
                ping_data = bytearray(self.classCon.ping(1))
                self.sock.send(ping_data)
            elif header == '11101000':
                value = int(recv_data[6])
                print Message().connect_ack(value)
                return False
            else:
                self.ping_byte(recv_data)

    def sync(self):
        msg_data = bytearray(self.classCon.sync())
        self.sock.send(msg_data)

    # def sync_only(self):
    #     # end = 83508
    #     # 最新的消息ID
    #     end = 82168
    #     for i in range(200):
    #         start = end - 10
    #         msg_data = bytearray(self.classCon.sync_only(start, end))
    #         self.sock.send(msg_data)
    #         end -= 10
    #         time.sleep(10)
    def json_formt(self, data):
        try:
            data = str(data)
            jf = JsonFormatter(json_data=data).render()[1:]
            print "\033[1;31m %s" % jf
        except:
            print data

    def recv_basic(self):
        total_data = []
        while True:
            data = self.sock.recv(2048)
            if not len(data):
                break
            data = bytearray(data)
            for num in range(0, len(data)):
                data_msg = bin(data[num]).replace('0b', '').zfill(8)
                total_data.append(data_msg)
            if len(total_data) > 2:
                index = 2
                if total_data[0] == '00100001' and total_data[1] == '01001000':
                    total_data = total_data[1:]
                msg_len = int(''.join(total_data[index:index + 4]), 2) + 6
                if len(total_data) == msg_len:
                    return total_data
                if total_data[0] == '01001000' and total_data[1] == '00000011':
                    return total_data
            else:
                return total_data

    def msg_type_push(self, reply):
        index = 0
        header = reply[0]
        body = reply
        if header == '01011110':
            body = reply[16:]
        for i in range(0, len(body)):
            msg_body = int("".join(body[index + 2:index + 6]), 2) + 6
            push_data = body[index:index + msg_body]
            self.return_push(push_data)
            index += msg_body
            if index == len(body):
                break

    def return_push(self, push_data):
        header = push_data[0]
        if header == '01001000' and len(push_data) == 20:
            print "对方查看了你的消息"
            return
        session = int(push_data[7], 2)
        s_type = Message().session_list(session)  # 会话类型
        # messageId = int(''.join(push_data[12:20]), 2)  # 消息ID
        # messageTime = int(''.join(push_data[20:24]), 2)  # 消息时间戳
        other_uid = int(''.join(push_data[8:12]), 2)
        bin_msg = ''.join(push_data[28:])
        str_msg = msgpack.unpackb(Convert().restore(bin_msg))
        print '当前时间：'+str(datetime.datetime.now())

        print 'str_msg:'+str(str_msg)

        name = ""
        if 'profile' in str_msg.keys() and len(str_msg['profile']) != 0:
            if 'name' in str_msg['profile'].keys():
                name = str_msg['profile']['name']
        elif 'from' in str_msg.keys():
            name = str_msg['from']


        if 'contents' in str_msg.keys():
            contents=str_msg['contents']

        else:
            print 'contents失败'



        # contents = str_msg['contents']

        # print 'aaaa:'+contents
        # 处理红包逻辑,如果收到主播红包,记录红包id
        # if str_msg['type'] == 92:
        #
        #     file = open('%s/req_http/hongbao/logs/hongbao_id.txt' % path, 'w')
        #     file.write(str_msg['extra']['hongbao_id'])
        #     file.close()
        #     self.sock.shutdown(2)
        #     self.sock.close()
        m_type = Message().message_list(str_msg['type'])  # 消息类型
        if header == '01001100':
            if str_msg['type'] == 9:
                print '\033[1;32m 同步群组%s 会话类型为%s 群名称为%s 群简介为%s' % (
                    other_uid, s_type, str_msg['extra']['groups_name'], str_msg['extra']['groups_description'])
            elif contents == '':
                print '\033[1;32m 同步用户%s 会话类型为%s,消息类型为:%s' % (other_uid, s_type, m_type)
            else:
                print '\033[1;32m 同步用户 %s 会话类型为%s,消息类型为:%s 返回详情为:' % (
                    str_msg['profile']['name'], s_type, m_type)
                self.json_formt(str_msg)
        else:
            print '\033[1;32m %s 给您发来%s,消息类型为:%s 返回详情为:' % (name, s_type, m_type)
            self.json_formt(str_msg)
            if "is_robot" in self.message.keys():
                call_me = 0
                robot_name = self.message['robot_name']
                if s_type == "群消息":
                    if "@" + robot_name in contents:
                        call_me = 1
                        contents = contents.replace("@" + robot_name, "")
                    else:
                        import re
                        re_list = re.findall("@\((.*?)\)", contents)
                        if len(re_list) != 0 and robot_name in re_list[0]:
                            contents = contents.replace("@(" + re_list[0] + ")", "")
                            call_me = 1
                message_type = str_msg['type']
                try:
                    if other_uid in [5265956]:
                        return
                    if message_type == 9:
                        from robot_send_message import AutoReply
                        self.message = AutoReply(config=self.config, msg=str_msg,
                                                 message=self.message).group_invitation()
                        if "message_send" in self.message.keys():
                            self.send_msg(robot=True)
                    elif s_type == "私人消息" or call_me == 1:
                        from ..setting import ROBOT_URL
                        import json
                        import requests
                        data = {
                            'contents': contents,
                            "uid": other_uid,
                            "profile": str_msg['profile'],
                            "type": message_type,
                            "session_type": session
                        }
                        post_data = json.dumps(data)
                        response = json.loads(requests.post(url=ROBOT_URL, data=post_data).content)
                        response_data = response['data']
                        text = response_data['contents']
                        if session == 3:
                            from ..hashid import get_hashid
                            hashuid = get_hashid(int(str_msg['from']))
                            name = str_msg["profile"]["name"].decode('utf-8')
                            response_data['contents'] = u"@(name:%s,id:%s) " % (name, hashuid) + text
                        self.message['session_type'] = session
                        self.message = dict(self.message, **response_data)
                        keys = response_data.keys()
                        if 'special' not in keys and message_type in [1, 6]:
                            time.sleep(len(text) * 0.08)
                        self.send_msg(robot=True)
                        if 'image' in keys:
                            self.message['message_type'] = response_data['image']['message_type']
                            self.message['contents'] = response_data['image']['contents']
                            time.sleep(0.8)
                            self.send_msg(robot=True)
                except:
                    pass

    def return_req(self, push_data):
        error_code = int(push_data[6], 2)
        if error_code == 0:
            bin_msg = ''.join(push_data[11:])
            str_msg = msgpack.unpackb(Convert().restore(bin_msg))
            if 'req_type' in str_msg.keys():
                req_type = Message().req_type_list(str_msg['req_type'])
                print '当前时间为：'+str(datetime.datetime.now())
                print "\033[1;32m REQ类型为%s 请求成功,body为:" % req_type
                if str_msg['req_type'] == 6:
                    # 获取直播间信息
                    self.message['req_type'] = 8
                    self.send_msg()
                elif str_msg['req_type'] == 3:
                    self.message['req_type'] = 8
                    self.message['session_id'] = str_msg['session_id']
                    self.message['session_type'] = 4
                    self.send_msg()
            self.json_formt(str_msg)


        else:
            print "请求失败,失败原因为: %s" % Message().req_error_code(error_code)
            self.sign_out()

