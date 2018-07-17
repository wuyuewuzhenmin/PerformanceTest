# -*-coding:utf8-*-
# import performance_test


from lib import performance_h5
from lib.hashid import get_hashid
from lib.performance_h5 import Performance

#
def get_percent_time(data_list, percent):
    data_list = sorted(data_list)
    if len(data_list)*(1-percent) <= 1:
        r_length = 1
    else:
        r_length = len(data_list)*(1-percent)
        r_length = int(round(r_length))
    data_list = data_list[:len(data_list)-r_length]
    return data_list[-1]

def h5_performacn(is_url,is_get,is_data,is_num):



    # 设置并发数
    thread_count = 3
    # 所有线程花费时间列表
    spend_time_list = []
    # 最大响应时间
    max_time = 0
    # 最小响应时间
    min_time = 3600
    # 小于3秒的请求数
    less_than_3_total = 0
    # 大于3秒的请求数
    more_than_3_total = 0
    # 成功的请求数
    success_total = 0
    # 失败的请求数
    fail_total = 0
    # 异常的请求数
    except_total = 0
    # 总请求数
    total = 0
    # 用户
    linea=[]

    i = 0
    # 所有线程总花费时间
    time_total = 0
    for a in range(is_num):
        # url = "http://activity-test.blued.cn/hd/2018-member/receive/ZV6r6p/%s" %get_hashid(a)
        url="https://pay-test.blued.cn/activity/buildbox/open?box_id=710&live_id=150162"
        # pf = performance_h5.Performance(url=url)
        data={

        }
        pf = performance_h5.Performance(url=is_url, method=is_get, body_type= is_data )

        status, spend_time = pf.test_performance()
        spend_time_list.append(spend_time)
        total += 1
        if status == "success":
            success_total += 1
        elif status == "fail":
            fail_total += 1
        elif status == "except":
            except_total += 1
        if spend_time > max_time:
            max_time = spend_time
        if spend_time < min_time:
            min_time = spend_time
        if spend_time > 3:
            more_than_3_total += 1
        else:
            less_than_3_total += 1
        time_total += spend_time
        pf.start()
        i += 1


    # 平均响应时间
    avg_time = time_total/thread_count
    # 响应时间列表从小到大排序
    spend_time_list = sorted(spend_time_list)
    avg_timea = u"平均响应时间：%s" % avg_time
    max_timea = u"最大响应时间：%s" % max_time
    min_timea = u"最小响应时间：%s" % min_time
    get_percent9 = u"99%%响应时间：%s" % (get_percent_time(spend_time_list, 0.9))
    get_percent99 = u"99%%响应时间：%s" % (get_percent_time(spend_time_list, 0.99))
    get_percent8 = u"80%%响应时间：%s" % (get_percent_time(spend_time_list, 0.8))
    totala = u"总请求数：%s" % total
    success_totala = u"成功请求数：%s" % success_total
    fail_totala = u"失败请求数：%s" % fail_total
    except_totala = u"异常请求数：%s" % except_total
    more_3_total = u"大于3秒的请求数：%s" % more_than_3_total
    less_3_total = u"小于3秒的请求数：%s" % less_than_3_total
    print u"平均响应时间：%s" % avg_time
    print u"最大响应时间：%s" % max_time
    print u"最小响应时间：%s" % min_time
    print u"90%%响应时间：%s" % (get_percent_time(spend_time_list, 0.9))
    print u"99%%响应时间：%s" % (get_percent_time(spend_time_list, 0.99))
    print u"80%%响应时间：%s" % (get_percent_time(spend_time_list, 0.8))
    print u"总请求数：%s" % total
    print u"成功请求数：%s" % success_total
    print u"失败请求数：%s" % fail_total
    print u"异常请求数：%s" % except_total
    print u"大于3秒的请求数：%s" % more_than_3_total
    print u"小于3秒的请求数：%s" % less_than_3_total

    return avg_timea+'\n'+max_timea+'\n'+min_timea+'\n'+get_percent9+'\n'+get_percent99+'\n'+get_percent8+'\n'+totala+'\n'+success_totala+'\n'+fail_totala+'\n'+except_totala+'\n'+more_3_total+'\n'+less_3_total