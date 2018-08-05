# encoding: utf-8

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import base64
import hashlib
import json


class EncryptDecrypt:
    def __init__(self):
        self.key = base64.decodestring('hTFBGbJ1w2kD9W3S9a6QAA==')
        self.mode = AES.MODE_CBC
        self.ak = 'ac7d'
        self.sk = 'hTFBGbJ1w2kD9W3S9a6QAA=='
        self.iv = '1111111111111111'
        self.uuid = 'e30b7d4982d68096eb2c543063ee1212ece165e0'
        self.iv_de = ''

    def jiami_j2j(self, text):
        j1 = json.dumps(text)
        dj = self.padAK(self.encrypt(j1))
        values2 = {'_': dj}
        jdata2 = json.dumps(values2)
        return jdata2

    def jiemi_j2j(self, text):
        j1 = json.loads(text)
        s1 = j1['data'][0]['_']
        s2 = self.decrypt(self.unak(s1))
        return s2

    # aes加密
    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv)
        length = 16
        count = len(text)
        pad = text + (length - len(text) % length) * chr(length - len(text) % length)
        self.ciphertext = cryptor.encrypt(pad)
        return b2a_hex(self.ciphertext)

    # aes解密
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, self.iv_de)
        plain_text = cryptor.decrypt(a2b_hex(text))
        unpad = plain_text[0:-ord(plain_text[-1])]
        return unpad

    # 插入ak
    def padAK(self, text):
        ak1 = self.ak + text[0:10] + b2a_hex(self.iv) + text[10:len(text)]
        ak2 = a2b_hex(ak1)
        baseak = base64.encodestring(ak2)
        return baseak.replace('\n', '')

    # 解除ak
    def unak(self, text):
        baseak = base64.decodestring(text)
        ak1 = b2a_hex(baseak)
        ak2 = ak1[4:14] + ak1[46:len(ak1)]
        self.iv_de = a2b_hex(ak1[14:46])
        return ak2

    # 获取devid
    def get_devid(self):
        part1 = self.md5(self.uuid + self.key)
        part2 = self.md5(part1 + self.key)
        return part1 + part2

    # md5加密
    def md5(self, test1):
        m = hashlib.md5()
        m.update(test1)
        return m.hexdigest()
