# -*- coding: UTF-8 -*-
"""
    __auth__: 焦淑鹏
    __require__: 数据库存储
    __version__: 6.1.2
"""
import MySQLdb


class SqlDb:
    def __init__(self):
        self.redis_user = '10.9.87.202'  # 测试环境user库地址
        self.sql_blued = '10.9.196.184'  # 测试环境blued库地址
        self.sql_qa = '10.9.128.47'  # 测试环境qa库地址
        self.sql_zentao = '117.79.87.29'  # 测试环境禅道地址

    def user_info(self, num, online):
        """
        查询qa数据库用户信息
        :param num: 获取用户的数量
        :param online: 获取线上用户uid(1) or 测试环境uid(0)
        :return: 查询结果
        """
        # 打开数据库连接
        con = MySQLdb.connect(self.sql_qa, 'root', 'qatest', 'qa', charset='utf8')
        # 使用cursor()方法获取操作游标
        cur = con.cursor()
        # sql插入语句
        sql = "select username,password,uid FROM qa_load WHERE type = %d" % int(online)
        # noinspection PyBroadException
        try:
            # 执行sql语句
            cur.execute(sql)
            # 取得上个查询的结果，是单个结果
            result = cur.fetchall()[0:num]
            return result
        except:
            # 发生错误时回滚
            con.rollback()
        con.close()
