"""
@Desc   : 测试代理链接
@Time   : 2021-05-02 21:51
@Author : tank boy
@File   : test_proxy.py
@coding : utf-8
"""
import json
import os

import requests


# 验证方式：1.使用telnet，2.使用下面这个网址
# 返回当前的访问ip，差不多都是这样的，所以我就写了这两个验证的方法，
def verify_proxy(type, host, port):
    """
    :param type:http or https
    :param host:ip地址
    :param port:端口
    :@return pass with True,or False
    """
    try:
        this_proxy = str(type) + '://' + str(host) + ':' + str(port)
        res = requests.get(url="http://icanhazip.com/", timeout=3, proxies={type: this_proxy})  # timeout越小，得到ip越少、质量越高
        proxy_ip = res.text.replace("\n", "")
        if proxy_ip == host:
            print(this_proxy + '有效')
            return True
        else:
            print(this_proxy + '无效')
            return False
    except Exception as e:
        print("测试代理：" + str(type) + '://' + str(host) + ':' + str(port) + "出现未知错误")


def test_proxy_json():
    """
    测试已经加入到json文件中的代理
    """
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("CommonSpider\\") + len("CommonSpider\\")]  # 获取myProject，也就是项目的根路径
    dataPath = os.path.abspath(rootPath + 'model\\proxy_ip.json')  # 获取tran.csv文件的路径

    with open(dataPath, 'r', encoding='utf8') as f:
        # dict_ip = json.load(f)
        content = f.readlines()
        for line in content:
            data = json.loads(line)
            data_host, data_port, data_type = data['host'], data['port'], data['type']
            try:
                verify_proxy(data_type, data_host, data_port)
            except Exception as e:
                print('当前代理：' + str(data_type) + '://' + str(data_host) + str(data_port) + '失效')
