import os
import re
import time

from requests_html import HTMLSession


class Config:
    def __init__(self):
        self.dir_work_path = "/home/youmi/gitlab-youmi/AG/"
        self.dir_err_log = self.dir_work_path + "err_log/"
        self.dir_html_page = self.dir_work_path + "html-page/"

        self.file_sql_html = self.dir_work_path + "sql_html.txt"
        self.file_err_log = self.dir_err_log + "err_log"

        self.only_goods = self.dir_work_path + "only_goods"
        self.only_address = self.dir_work_path + "only_address"
        self.both_goods_and_address = self.dir_work_path + "both_goods_and_address"
        self.either_goods_or_address = self.dir_work_path + "either_goods_or_address"

        self.id_to_url_map = {}


def download_one(title, site):
    config = Config()
    download_save_path = config.dir_html_page

    save_path = download_save_path + str(title)

    error_log_path = config.file_err_log

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
    print("下载总共耗时：{}".format(before_download - finish_download))


def html_search_word(dir_path, id_url_map):
    """
    dir_path是个目录，该目录下有许多已经下载好的html文件，从这些文件中进行匹配
    匹配成功，则写入相应的列表里
    匹配失败，则写入错误日志中，继续执行
    :param dir_path:
    :param id_url_map:
    :return: 四个列表： only_goods、 only_address、 both_goods_and_address、either_goods_or_address
    """
    config = Config()

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
            try:
                with open(config.file_err_log, 'a') as f:
                    err_content = "e={}, line={} {}".format(e, each_file, id_url_map[each_file])
                    f.write(err_content)
            except Exception as ee:
                print("{}有问题".format(each_file))
    return only_goods, only_address, both_goods_and_address, either_goods_or_address


def download_html(id_url_map):
    # 下载这些url的html页面并保存
    id_url = [x for x in id_url_map.items()]
    download_all(id_url)


def build_id_url_map(sql_html):
    id_url_map = {}
    with open(sql_html, 'r') as f:
        # 连续读两次是为了要跳过第一行
        line = f.readline()
        line = f.readline()
        while line:
            # the_id, url = list(line.strip().split())
            split_list = list(line.strip().split())
            the_id = split_list[0]
            url = "".join(split_list[1:])
            id_url_map[the_id] = url
            line = f.readline()
    return id_url_map


def match():
    config = Config()
    id_url_map = config.id_to_url_map
    only_goods, only_address, both_goods_and_address, either_goods_or_address = html_search_word(config.dir_html_page,
                                                                                                 id_url_map)
    with open(config.only_goods, 'a') as f:
        f.write(str(only_goods))
    with open(config.only_address, 'a') as f:
        f.write(str(only_address))
    with open(config.both_goods_and_address, 'a') as f:
        f.write(str(both_goods_and_address))
    with open(config.either_goods_or_address, 'a') as f:
        f.write(str(either_goods_or_address))
    return


def build_map():
    config = Config()
    config.id_to_url_map = build_id_url_map(config.file_sql_html)
    id_url_map = config.id_to_url_map
    return id_url_map


if __name__ == '__main__':
    session = HTMLSession()
    # 先建id --> 的映射字典
    id_url_map = build_map()

    # 根据字典的key, value去下载html，保存的名字是key，内容是value里提取的url下载的html页面
    download_html(id_url_map)

    # 进行匹配
    match()
