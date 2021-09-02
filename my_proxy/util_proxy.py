"""
@Desc   : 测试代理链接
@Time   : 2021-05-02 21:51
@Author : tank boy
@File   : util_proxy.py
@coding : utf-8
"""
import json

# ================================json 操作===Start===========================
import requests

from util import cfg


def clean_proxy_json():
    """
    清空json文件
    """
    with open('proxy.json', 'w') as f:
        f.seek(0)
        f.truncate()
        f.close()
    print("json已清空数据")


def write_proxy_json(pass_proxy):
    """
    将测试通过的代理写入json文件
    """
    temp_json = json.dumps(pass_proxy)
    with open('proxy.json', 'a+') as f:
        f.write(temp_json + '\n')
        f.close()
    print("已写入：%s" % pass_proxy)
    # 不使用下面这种方法，是因为pass_proxy是一个Python对象，无法与一个字符串相加
    # with open('proxy.json', 'w') as f:
    #     json.dump(pass_proxy + '\n', f)


def read_json(url):
    """
    通用读取json函数
    @return: 列表，内容是一行的内容 为 一个元素
    """
    data_list = []
    with open(url, 'r') as f:
        content = f.readlines()
        for line in content:
            line_data = json.loads(line)
            data_list.append(line_data)
        f.close()
    return data_list


# ================================json 操作===End==============================
# =============================格式转化 操作===Start===========================


def request_to_json(dict):
    """
    将request proxy格式   转为    json proxy格式
    @param dict:
    @return:
    """
    try:
        str = dict['http']
    except KeyError as e:
        str = dict['https']
        print("出现了dict['https'] %s" % dict)
    type, host_port = str.split('://')
    host, port = host_port.split(':')
    proxy = {'type': type, 'host': host, 'port': port}
    return proxy


# =============================格式转化 操作===End===========================

# 验证方式：1.使用telnet，2.使用下面这个网址
def verify_proxy(proxy, *id):
    """
    :param dict: 一个字典。可能为json格式、可能为request模式
    :@return pass with True,or False
    """
    # proxy = dict
    # if 'id' in dict:
    #     proxy = json_to_request(dict)
    try:
        response = requests.get(url="http://icanhazip.com/", timeout=cfg.TIMEOUT, proxies=proxy)  # timeout越小，得到ip越少、质量越高
        proxy_ip = response.text.replace("\n", "")
        if proxy_ip == proxy['host']:
            print("测试代理%s" % proxy + "_code=%s" % response.status_code + '_有效')
            return True
        else:
            print("测试代理%s" % proxy + "_code=%s" % response.status_code + '_无效')
            return False
    except Exception as e:
        print("测试代理%s" % proxy + "出现未知错误")
        return False


# 要想在代理池中修改用过的代理
# 1. 拿着自己的信息，到池中比对，找到后再修改池中代理的hp值
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

    else:
        print("没参数？：%s" % request_proxy)
