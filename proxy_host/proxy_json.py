"""
@Desc   : 测试代理链接
@Time   : 2021-05-02 21:51
@Author : tank boy
@File   : proxy_json.py
@coding : utf-8
"""
import json
import os

# 验证方式：1.使用telnet，2.使用下面这个网址
import cfg
from proxy_host.get_proxy import verify_proxy


def read_proxy_json():
    """
    测试已经加入到json文件中的代理
    """
    data_path = os.path.abspath('.\\proxy.json')  # 获取tran.csv文件的路径
    with open(data_path, 'r', encoding='utf8') as f:
        # dict_ip = json.load(f)
        content = f.readlines()
        for line in content:
            proxy = json.loads(line)
            cfg.Proxy_Pool.append(proxy)  # 添加到全局变量中


# 当request请求失败，将代理打回来的情况下。判断是代理问题，还是其他问题，如网关拦截、网络波动、反爬拦截
def proxy_false(proxy):
    # 1.先进行代理测试  2.代理确实不通过，减hp
    if not verify_proxy(proxy):
        if proxy['hp'] == 0:
            cfg.Proxy_Pool.remove(proxy)
            print(proxy['type'] + proxy['host'] + str(proxy['port']) + '_hp=0，已被移除')
        else:
            proxy['hp'] = proxy['hp'] - 1
            print(proxy['type'] + proxy['host'] + str(proxy['port']) + '_hp=' + str(proxy['hp']))
