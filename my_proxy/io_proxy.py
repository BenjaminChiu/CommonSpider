"""
@Desc   : 获取代理，存放到ip代理池。1.从json文件中获取，2.从数据库中获取（暂时不用数据库，太重）
@Time   : 2021-01-28 19:10
@Author : tank boy
@File   : io_proxy.py
@coding : utf-8

整个代理模块的工作流程如下：

手动下载.list文件到桌面，由get_proxy_from_list()读入，将代理处理成可供request使用的shape
使用多线程对代理进行测试，对测试通过的代理，将其写入同目录的proxy.json


拿数据
request.get_proxy()  从全局变量cfg.Proxy_Pool 获取

"""

import random

import requests

from my_proxy.util_proxy import json_to_request, read_json, info_proxy_dict, verify_proxy, request_to_json, write_proxy_json
from util import cfg


# proxy_url = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'


# 热更新输出
def proxy_out():
    """
    返回一个代理，供MyRequest使用
    json代理池proxy格式：{'type': type, 'host': host, 'port': port, 'hp': hp, 'id': id}
    request需要的proxy格式：{type:"type://host:port"}
    二者特点，一个有hp、id的key
    @return:一个字典，内容为代理
    """
    if cfg.Proxy_Pool:
        pre_data = random.choice(cfg.Proxy_Pool)  # 随机筛选一个
        proxy = json_to_request(pre_data)
        print('Request使用代理：%s' % pre_data)
        return proxy
    else:
        return None


# 冷备份 到 热更新，只需启动一次
def cold_proxy_out():
    data_list = read_json('C:\A.Drive\Develop\WorkSpace\PC.Spider.Web\CommonSpider\my_proxy\proxy.json')
    for line in data_list:
        cfg.Proxy_Pool.append(line)


# ============================Proxy==In======Start=================================
# 为每个代理添加一个生命值，并初始化赋值如100，（磁盘 持久化）
# 没请求失败一次就-1，直至为0，从文件中删除（内存 内存中删除）
def info_proxy_from_list():
    """
    从.list文件中读取代理信息，获取ip，port ，type
    未用request请求.list文件的原因：需要翻墙才能下载。只能手动翻墙，手动下载
    """
    data_list = read_json("C:/Users/Administrator/Desktop/proxy.list")
    proxy_list = []
    for line in data_list:
        type, host, port = info_proxy_dict(line)  # 提取字典信息，重新赋值
        proxy = {type: type + '://' + host + ':' + str(port)}  # 封装为一个request形式的proxy
        proxy_list.append(proxy)
    return proxy_list


def get_verify_proxy(proxy_list):
    pass_proxy_list = []
    session = requests.session()
    for i in range(len(proxy_list)):
        if verify_proxy(proxy_list[i]):
            pass_proxy = request_to_json(proxy_list[i])
            pass_proxy['hp'] = 9  # 新增一个hp键，0开始计数
            pass_proxy['id'] = i
            pass_proxy_list.append(pass_proxy)
    return pass_proxy_list


# ============================Proxy==In======End=================================
if __name__ == '__main__':
    proxy_list = info_proxy_from_list()
    pass_proxy_list = get_verify_proxy(proxy_list)
    # write_proxy_json(pass_proxy_list)
    for proxy in pass_proxy_list:
        write_proxy_json(proxy)
        cfg.Proxy_Pool.append(proxy)
    print("success")
