# encoding: utf-8
"""
    __auth__: 焦淑鹏
    __require__: 设置文件
    __version__: 配置各种环境变量
"""
import platform
import os

# 平台
device_platform = platform.platform().split("-")[0]
fil = os.getcwd().split('script')
path = fil[0] + 'script'

# 接口相关
ONLINE_HTTP_HOST = "https://argo.blued.cn"
TEST_HTTP_HOST = "http://106.75.100.161"
TEST_HB_HOST = "https://106.75.73.234"
TEST_PAY_HOST = "https://pay-test.blued.cn"
ONLINE_PAY_HOST = "https://pay.blued.cn"

# IM相关
ONLINE_IM_HOST = "h4.blued.cn"
TEST_IM_HOST = "106.75.109.100"

# charon相关
TEST_CHARON_HOST = "http://10.9.159.109:1766"
ONLINE_CHARON_HOST = "http://10.10.242.199:1069"

# redis host相关,通过线上用户uid获取线上用户session_id
TEST_REDIS_HOST = "10.9.87.202"
ONLINE_REDIS_HOST = "10.6.12.180"

# android UA
USER_AGENT_ANDROID = 'Mozilla/5.0 (Linux; U; Android 5.1.1; SM-N9200 Build/LMY47X) ' \
                     'Android/000206_0.2.6_4331_057 (Asia/Shanghai) Dalvik/2.1.0 app/1'
# ios UA
# USER_AGENT_IOS = 'Mozilla/5.0 (iPhone; iOS 11.1.2; Scale/2.00)' \
#                  ' iOS/000206_0.2.6_4331_057 (Asia/Shanghai)'

USER_AGENT_IOS = 'Mozilla/5.0 (iPhone; iOS 11.3; Scale/2.00) iOS/100306_0.3.6_4331_057 (Asia/Shanghai) app/1'

# robot_host
ROBOT_URL = "http://10.9.128.47:8004/robot/msg_signature/"
# ROBOT_URL = "http://127.0.0.1:8000/robot/msg_signature/"
# USER_AGENT_IOS = "Mozilla/5.0 (iPhone; iOS 11.1.2; Scale/3.00) iOS/130106_3.1.6_8022_2421 (Asia/Shanghai)"

# hermes redis
HERMES_REDIS_HOST = "10.10.49.217"
