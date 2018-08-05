# encoding: utf-8
import base64

import redis
import requests

import encryption
from ia_token import GetHeader
from setting import USER_AGENT_IOS, USER_AGENT_ANDROID

"""
    __auth__: 焦淑鹏
    __require__: 通过线上用户uid,获取该用户的鉴权串
    __version__: 无要求
    __function__: 通过线上用户uid,获取该用户的鉴权串
    __mark__: 需要连接线上环境VPN
"""


class GetToken:
    def __init__(self, **kwargs):
        self.redis_host = kwargs.get('redis_host')
        self.device = kwargs.get('device')
        self.uid = kwargs.get('uid')
        self.http_host = kwargs.get('http_host')
        self.pc = encryption.EncryptDecrypt()
        self.key = {
            'ios': {
                'AK': 'ac7d',
                'SK': 'hTFBGbJ1w2kD9W3S9a6QAA=='
            },
            'android': {
                'AK': 'df0b',
                'SK': 'VlEc5qsEDXWChrWJ0AzMXQ=='
            }

        }

    def im_token(self):
        get_token = self.get_token()
        if get_token is False:
            return False
        authorization = base64.decodestring(get_token)
        result = {
            'authorization': authorization,
            'user_info': self.user_info()
        }
        return result

    def get_token_http(self):
        get_token = self.get_token()
        if get_token is False:
            return get_token
        b2 = base64.encodestring(str(self.uid) + ':' + get_token).replace('\n', '')
        token = 'Basic ' + b2
        return token

    def get_token(self):
        r = redis.Redis(host=self.redis_host, port=6379)
        access_token = r.get("u:%d:session_id" % int(self.uid))
        if access_token is None:
            print "用户[%s]已退出登录,无法获取session id" % str(self.uid)
            return False
        en_text = self.pc.encrypt(access_token)
        ak_text = self.pc.padAK(en_text)
        return ak_text

    def header_auth(self):
        user_agent = USER_AGENT_IOS
        if self.device == 'android':
            user_agent = USER_AGENT_ANDROID
        header = GetHeader(user_agent=user_agent).header_default()
        header['Authorization'] = self.get_token_http()
        return header

    @staticmethod
    def request(url, headers, data=''):
        if data == '':
            response = requests.get(url=url, headers=headers).content
        else:
            response = requests.post(url=url, data=data, headers=headers).content
        return response

    def user_info(self):
        url = self.http_host + '/users' + '/%s' % self.uid
        users = self.request(url=url, headers=self.header_auth())
        import json
        result = json.loads(users)["data"][0]
        return result
