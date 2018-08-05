#!/usr/bin/env python
# encoding: utf-8

import base64
import hashlib
import json
import platform
import ssl
import logging

import requests

import encryption


class GetHeader:
    def __init__(self, **kwargs):
        self.username = kwargs.get("username")
        password = kwargs.get("password")
        if password is not None:
            self.password = hashlib.sha1(password).hexdigest()
        self.user_agent = kwargs.get("user_agent")
        self.http_host = kwargs.get("http_host")
        self.method = kwargs.get('method')
        self.header = kwargs.get('header')
        self.url = kwargs.get('url')
        self.data = kwargs.get('data')
        self.pc = encryption.EncryptDecrypt()

    def post_data(self):
        data = dict()
        if self.username[0] == "+":
            data['type'] = 'mobile'
        else:
            data['type'] = 'email'
        data['identity'] = self.username
        data['password'] = self.password
        data['dev_id'] = self.pc.get_devid()
        cipher_text = self.pc.jiami_j2j(data)
        return cipher_text

    def user_info(self):
        if platform.platform()[0:6] == 'Darwin':
            ssl._create_default_https_context = ssl._create_unverified_context
        # try:
        response = requests.post(url=self.http_host + '/passport/auth', data=self.post_data(),
                                 headers=self.header_default()).content
        # print response
        if json.loads(response)['code'] != 200:
            print response
        decrypt_response = self.pc.jiemi_j2j(response)
        user_info = json.loads(decrypt_response)
        return user_info
        # except:
        #     print "获取用户鉴权失败"
        #     return False

    def http_token(self):
        user = self.user_info()
        if user is False:
            return user
        authorization = self.obtain_token(user)
        result = {
            'authorization': authorization,
            'user_info': user
        }
        return result

    def im_token(self):
        user = self.user_info()
        if user is False:
            return user
        authorization = self.obtain_token_im(user)
        result = {
            'authorization': authorization,
            'user_info': user
        }
        return result

    def access_token(self, user_info):
        if 'access_token' not in user_info.keys():
            return False
        access_token = user_info['access_token']
        uid = user_info['uid']
        en_text = self.pc.encrypt(access_token)
        ak_text = self.pc.padAK(en_text)
        result = {
            'uid': uid,
            'ak_text': ak_text
        }
        return result

    def obtain_token(self, user):
        token_res = self.access_token(user)
        uid = token_res['uid']
        ak_text = token_res['ak_text']
        b2 = base64.encodestring(str(uid) + ':' + ak_text).replace('\n', '')
        token = 'Basic ' + b2
        return token

    def obtain_token_im(self, user):
        return_access = self.access_token(user)
        if return_access is False:
            return False
        ak_text = return_access['ak_text']
        b2 = base64.decodestring(ak_text)
        return b2

    def request(self):
        if self.method == 'get':
            response = requests.get(url=self.url, headers=self.header).content
        else:
            response = requests.post(url=self.url, data=self.data, headers=self.header).content
        return response

    def request_all(self):
        if self.method == 'get':
            response = requests.get(url=self.url, headers=self.header_auth()).content
        else:
            response = requests.post(url=self.url, data=self.data, headers=self.header_auth()).content
        return response

    def header_default(self):
        header = dict()
        header['Accept-Language'] = 'zh-cn'
        header['User-Agent'] = self.user_agent
        header['Content-Type'] = 'application/json'
        header['Connection'] = 'keep-alive'
        header['Accept'] = '*/*'
        return header

    def header_auth(self):
        header = self.header_default()
        auth = self.http_token()['authorization']
        if auth is not False:
            header['Authorization'] = auth
            return header
        else:
            return False
