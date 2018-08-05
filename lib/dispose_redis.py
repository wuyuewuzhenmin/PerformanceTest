# -*- coding: UTF-8 -*-
"""
    __auth__: 焦淑鹏
    __require__: 数据库存储
    __version__: 6.1.2
"""
import redis


class RedisDb:
    def __init__(self):
        self.redis_user = '10.9.87.202'  # 测试环境user库地址
        self.redis_live = '10.9.87.202'  # 测试环境user库地址
        self.redis_qa = '10.9.128.47'  # 测试环境QA redis库
        self.port = 6379

    def user_lid(self, uid):
        """
        获取测试环境users库用户的live id
        :param uid: 用户的uid
        :return: 查询结果
        """
        users_redis = redis.StrictRedis(host=self.redis_user, port=self.port)
        lid = users_redis.hget("u:%s" % uid, "live")
        return lid

    def get_chat_info(self):
        qa_redis = redis.StrictRedis(host=self.redis_qa, port=self.port)
        data = qa_redis.hget('2:9334493', 'url')
        print data