# encoding: utf-8
"""
    __auth__: 焦淑鹏
    __require__: json格式化类
    __version__: 无要求
    __function__: 输出格式化的json
"""
import json


class JsonFormatter:
    def __init__(self, intend=4, json_data=""):
        self.json_data = json_data
        self.intend = intend
        self.stack = []
        self.obj = None
        self.source = self.get_source(json_data)
        self.prepare()

    @staticmethod
    def json_str(s):
        return '"' + s + '"'

    @staticmethod
    def get_source(json_data):
        if type(json_data) == dict:
            json_data = json.dumps(json_data).decode('raw_unicode_escape')
        return ''.join(json_data.split())

    def prepare(self):
        try:
            self.obj = eval(self.source)
        except:
            raise Exception('Invalid json string!')

    def line_intend(self, level=0):
        return '\n' + ' ' * self.intend * level

    def parse_dict(self, obj=None, intend_level=0):
        self.stack.append(self.line_intend(intend_level) + '{')
        intend_level += 1
        for key, value in obj.items():
            key = self.json_str(str(key))
            self.stack.append(self.line_intend(intend_level) + key + ':')
            self.parse(value, intend_level)
            self.stack.append(',')
        self.stack.append(self.line_intend(intend_level - 1) + '}')

    def parse_list(self, obj=None, intend_level=0):
        self.stack.append(self.line_intend(intend_level) + '[')
        intend_level += 1
        for item in obj:
            self.parse(item, intend_level)
            self.stack.append(',')
        self.stack.append(self.line_intend(intend_level - 1) + ']')

    def parse(self, obj, intend_level=0):
        if obj is None:
            self.stack.append('null')
        elif obj is True:
            self.stack.append('true')
        elif obj is False:
            self.stack.append('false')
        elif isinstance(obj, (int, long, float)):
            self.stack.append(str(obj))
        elif isinstance(obj, str):
            self.stack.append(self.json_str(obj))
        elif isinstance(obj, (list, tuple)):
            self.parse_list(obj, intend_level)
        elif isinstance(obj, dict):
            self.parse_dict(obj, intend_level)
        else:
            raise Exception('Invalid json type %s!' % obj)

    def render(self):
        self.parse(self.obj, 0)
        res = ''.join(self.stack)
        return res


# if __name__ == "__main__":
#     json_data = {
#         "profile": {"device_token": "", "lang": "zh-cn", "name": "我是3", "distance": 0, "is_locked": false, "note": "",
#                     "coords": ["116.47047", "39.899876"],
#                     "avatar": "http://77g4l9.com5.z0.glb.qiniucdn.com/userfiles/009/334/494/48796!Head.jpg",
#                     "friend": 0, "vbadge": 7}, "type": 1, "from": 9334494, "contents": "哈哈", "session_status": 0}
#     jf = JsonFormatter(json_data=json.dumps(json_data))
#     print jf.render()
