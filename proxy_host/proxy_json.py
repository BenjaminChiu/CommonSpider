"""
@Desc   : 测试代理链接
@Time   : 2021-05-02 21:51
@Author : tank boy
@File   : proxy_json.py
@coding : utf-8
"""
import json
import random

import requests

import cfg


def info_proxy_dict(proxy):
    """
    提取字典，给定的键值信息
    没有解析id、hp，是因为在.list中文件没有这些
    @param proxy:解析字典
    @return:返回三个值
    """
    type = proxy['type']
    host = proxy['host']
    port = proxy['port']
    return type, host, port


def json_to_request(dict):
    """
    将json proxy格式   转为    request proxy格式
    @param dict:
    @return:
    """
    type, host, port = info_proxy_dict(dict)
    proxy_string = type + '://' + host + ':' + str(port)
    proxy = {type: proxy_string}
    return proxy


def request_to_json(dict):
    """
    将request proxy格式   转为    json proxy格式
    @param dict:
    @return:
    """
    str = dict['http']
    type, host_port = str.split('://')
    host, port = host_port.split(':')
    proxy = {'type': type, 'host': host, 'port': port}
    return proxy


def read_proxy_json():
    """
    读取json缓存池中的代理到内存cfg.Proxy_Pool。Proxy_Pool由一个个字典组成
    """
    # data_path = os.path.abspath('proxy.json')  # 获取文件的路径
    with open('./proxy.json', 'r') as f:
        # dict_ip = json.load(f)
        content = f.readlines()
        for line in content:
            proxy = json.loads(line)
            cfg.Proxy_Pool.append(proxy)  # 添加到全局变量中


# 验证方式：1.使用telnet，2.使用下面这个网址
def verify_proxy(dict):
    """
    :param dict: 一个字典。可能为json格式、可能为request模式
    :@return pass with True,or False
    """
    proxy = dict
    if 'id' in dict:
        proxy = json_to_request(dict)
    try:
        response = requests.get(url="http://icanhazip.com/", timeout=cfg.TIMEOUT, proxies=proxy)  # timeout越小，得到ip越少、质量越高
        proxy_ip = response.text.replace("\n", "")
        if proxy_ip == dict['host']:
            print("测试代理：%s" % dict + '有效')
            return True
        else:
            print("测试代理：%s" % dict + '无效')
            return False
    except Exception as e:
        print("测试代理：%s" % dict + "出现未知错误")
        return False


def get_proxy():
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


# 修改对应缓冲区中json的hp值，避免下次脏读
def proxy_false(request_proxy):
    """
    当request请求失败，将代理打回来的情况下。判断是代理问题，还是其他问题，如网关拦截、网络波动、反爬拦截
    1.先进行代理测试。参数来自
    2.代理确实不通过，减hp
    @param request_proxy: request中的代理
    @return:
    """
    if not verify_proxy(request_proxy):
        proxy = request_to_json(request_proxy)
        for i in cfg.Proxy_Pool:
            if i['type'] == proxy['type'] and i['host'] == proxy['host'] and str(i['port']) == proxy['port']:
                if i['hp'] == 0:
                    cfg.Proxy_Pool.remove(i)
                    print("移除代理：%s" % i)
                else:
                    i['hp'] = i['hp'] - 1
                    print("修改代理HP：%s" % i)


if __name__ == '__main__':
    read_proxy_json()
    proxy = get_proxy()  # {'http': 'http://159.8.114.37:8123'}

    proxy_false(proxy)
