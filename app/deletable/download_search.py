import os
import re
import time

import requests
from requests_html import HTMLSession
import logging
from logging import handlers

class Logger:
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self,filename,level='error',when='D',backCount=3,fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        sh = logging.StreamHandler()#往屏幕上输出
        sh.setFormatter(format_str) #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(th)


class Config:
    # 这里不用 def __init__(self) 的原因是为了方便，只是存储一下公共变量。
    dir_work_path = "/home/youmi/gitlab-youmi/AG/"
    dir_err_log = dir_work_path + "err_log/"
    dir_html_page = dir_work_path + "html-page/"

    file_sql_html = dir_work_path + "sql_html.txt"
    file_err_log = dir_err_log + "err_log"

    only_goods = dir_work_path + "only_goods"
    only_address = dir_work_path + "only_address"
    both_goods_and_address = dir_work_path + "both_goods_and_address"
    either_goods_or_address = dir_work_path + "either_goods_or_address"

    dir_filtered = dir_work_path + "filtered/"

    file_filtered_err_log = dir_filtered + "err_log"
    filtered_only_goods = dir_filtered + "only_goods"
    filtered_only_address = dir_filtered + "only_address"
    filtered_both_goods_and_address = dir_filtered + "both_goods_and_address"
    filtered_either_goods_or_address = dir_filtered + "either_goods_or_address"

    id_to_url_map = {}


def download_html(id_url_map):
    # 下载这些url的html页面并保存
    id_url = [x for x in id_url_map.items()]
    download_all(id_url)


def download_one(title, site):
    download_save_path = Config.dir_html_page

    save_path = download_save_path + str(title)

    error_log_path = Config.file_err_log

    try:
        r = session.get(site)
        r_html = r.html.html
        with open(save_path, 'a') as f:
            f.write(r_html)
    except Exception as e:
        with open(error_log_path, 'a') as fe:
            err_content = "\n e={}, line={} \n".format(e, title)
            fe.write(err_content)


def download_all(id_url):
    before_download = time.time()
    for item in id_url:
        title = item[0]
        site = item[1]
        download_one(title, site)
    finish_download = time.time()
    print("下载总共耗时：{}".format(before_download-finish_download))
    # 单进程、单线程，2.5W的url，下载总共耗时3.9小时


def html_search_word(dir_path, id_url_map):
    """
    dir_path是个目录，该目录下有许多已经下载好的html文件，从这些文件中进行匹配
    匹配成功，则写入相应的列表里
    匹配失败，则写入错误日志中，继续执行
    :param dir_path:
    :param id_url_map:
    :return: 四个列表： only_goods、 only_address、 both_goods_and_address、either_goods_or_address
    """
    only_goods = []
    only_address = []
    both_goods_and_address = []
    either_goods_or_address = []

    for each_file in os.listdir(dir_path):
        try:
            with open(dir_path + each_file, 'r') as f:
                content = f.read()
            include_goods = re.search(r"货到付款", content)
            include_address = re.search(r"地址", content)
            if include_goods and not include_address:
                only_goods.append([each_file, id_url_map[each_file]])
            if (not include_goods) and include_address:
                only_address.append([each_file, id_url_map[each_file]])
            if include_goods and include_address:
                both_goods_and_address.append([each_file, id_url_map[each_file]])
            if include_goods or include_address:
                either_goods_or_address.append([each_file, id_url_map[each_file]])
        except Exception as e:
            # 因为有些html下载失败的原因，所以在id_url_map里没有对应的key，所以这里try多一次是因为会引起KeyError
            # 其实也可以进行一次if判断，或者使用id_url_map.get(each_file,0)等等..
            try:
                with open(Config.file_err_log, 'a') as f:
                    err_content = "e={}, line={} {}".format(e, each_file, id_url_map[each_file])
                    f.write(err_content)
            except Exception as ee:
                print("{}有问题".format(each_file))
                # 第一次跑需要3.9个小时..2.5W的数据里有3K个抛出了有问题

    return only_goods, only_address, both_goods_and_address, either_goods_or_address


def build_id_url_map(sql_html):
    id_url_map = {}
    with open(sql_html, 'r') as f:
        # 连续读两次是为了要跳过第一行
        line = f.readline()
        line = f.readline()
        while line:
            split_list = list(line.strip().split())
            the_id = split_list[0]
            url = "".join(split_list[1:])
            id_url_map[the_id] = url
            line = f.readline()
    return id_url_map


def match():
    id_url_map = Config.id_to_url_map
    only_goods, only_address, both_goods_and_address, either_goods_or_address = html_search_word(Config.dir_html_page, id_url_map)
    with open(Config.only_goods, 'a') as f:
        for item in only_goods:
            f.writelines("{} {}\n".format(item[0], item[1]))
    with open(Config.only_address, 'a') as f:
        for item in only_address:
            f.writelines("{} {}\n".format(item[0], item[1]))
    with open(Config.both_goods_and_address, 'a') as f:
        for item in both_goods_and_address:
            f.writelines("{} {}\n".format(item[0], item[1]))
    with open(Config.either_goods_or_address, 'a') as f:
        for item in either_goods_or_address:
            f.writelines("{} {}\n".format(item[0], item[1]))
    return


def build_map():
    Config.id_to_url_map = build_id_url_map(Config.file_sql_html)
    id_url_map = Config.id_to_url_map
    return id_url_map


def the_request_without_words(url, the_id):
    """
    发送url请求，进行判断是否包含words=
    :param url:
    :return: True 或者　False
    """
    log = Logger(Config.file_filtered_err_log, level='error')
    try:
        the_request = requests.get(url)
        print("-------真实：-------")
        real_url = the_request.url
    except Exception as e:
        # file_filtered_err_log
        with open(Config.file_filtered_err_log, 'a') as fe:
            err_content = "{}, id={} url={}\n".format(log.logger.error(e), the_id, url)
            fe.write(err_content)
        return False
    print(real_url)
    if re.search(r"word=", real_url) or re.search(r"words=", real_url):
        print("-------完成,有word　或者 words---------")
        return False
    print("-------完成, 无---------")
    return True


def filter_url_without_words(origin_file_path, save_file_path):
    """
    由于有些原始url(称为origin_url)会302重定向，所以要进行一次请求，获取最终的url(称为final_url)，过滤掉final_url里包含words=的url,
    返回所有不包含words=的final_url的原始id_url列表
    :param origin_file_path: 原始文件路径
    :param save_file_path: 要保存的新文件的路径
    :return: 无
    """
    id_url_map = {}
    with open(origin_file_path, 'r') as f:
        line = f.readline()
        while line:
            split_list = list(line.strip().split())
            the_id = split_list[0]
            url = "".join(split_list[1:])
            # 如果这个请求的url的请求参数里没有words=这个字段，就符合要求
            print("-------原始：-------")
            print(url)
            if the_request_without_words(url,the_id):
                id_url_map[the_id] = url
            line = f.readline()
    with open(save_file_path, 'a') as f:
        for item in id_url_map.items():
            f.writelines("{} {}\n".format(item[0], item[1]))


def url_filter():
    filter_url_without_words(Config.only_goods, Config.filtered_only_goods)
    filter_url_without_words(Config.only_address, Config.filtered_only_address)
    filter_url_without_words(Config.either_goods_or_address, Config.filtered_either_goods_or_address)
    filter_url_without_words(Config.both_goods_and_address, Config.filtered_both_goods_and_address)


if __name__ == '__main__':
    session = HTMLSession()
    # 先建id --> 的映射字典
    id_url_map = build_map()

    # 根据字典的key, value去下载html，保存的名字是key，内容是value里提取的url下载的html页面
    # 因为已经下载过一次了，所以我这里注释掉，直接进行匹配
    # download_html(id_url_map)

    # 进行匹配
    # match()

    # url筛选，将筛选后的url放入新文件中
    url_filter()


# 第一次实验后，根据四个文件的行数可以得到结果：
# 只包含”货到付款“的有27条
# 只包含”地址“的有3352条
# 同时包含”货到付款“和”地址“的有299条
# 包含”货到付款“或者”地址“的有3678条