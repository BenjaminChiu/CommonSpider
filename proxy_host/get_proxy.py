"""
@Desc   : 获取代理，存放到ip代理池。1.从json文件中获取，2.从数据库中获取
@Time   : 2021-01-28 19:10
@Author : tank boy
@File   : get_proxy.py
@coding : utf-8
"""

import json

import cfg
from proxy_host import test_proxy


# 为每个代理添加一个生命值，并初始化赋值如100，（磁盘 持久化）
# 没请求失败一次就-1，直至为0，从文件中删除（内存 内存中删除）

def get_proxy(proxy_url):
    """
    从.list文件中读取代理信息
    获取ip，port ，type
    :param proxy_url:
    :return:
    """
    # response = requests.get(proxy_url, headers=header)
    # print(response)
    # proxies_list = response.text.split('\n')
    # for proxy_str in proxies_list:
    #     proxy_json = json.loads(proxy_str)
    #     host = proxy_json['host']
    #     port = proxy_json['port']
    #     type = proxy_json['type']

    with open("C:/Users/Administrator/Desktop/proxy.list", "r") as f:
        data = f.read()
        # 拆分开返回的数据
        proxies_list = data.split('\n')
        print(len(proxies_list))
        print(proxies_list)

        clean_json()  # 手动清空json文件

        # 总数-1的目的是，读文件的时候，总会多读1行
        for i in range(len(proxies_list) - 1):
            print(str(i) + proxies_list[i])
            proxy_json = json.loads(proxies_list[i])
            type = proxy_json['type']
            host = proxy_json['host']
            port = proxy_json['port']

            # 代理测试通过，就写入到json文件
            if test_proxy.verify_proxy(type, host, port):
                pass_proxy = {'type': type, 'host': host, 'port': port, 'hp': 10}
                write_proxy(pass_proxy)
                cfg.Proxy_Pool.append(pass_proxy)  # 添加到全局变量中

        f.close()  # 关闭文件


def clean_json():
    """
    清空json文件
    """
    with open('proxy_ip.json', 'w') as f:
        f.seek(0)
        f.truncate()
        print("json已清空数据")
        f.close()


def write_proxy(pass_proxy):
    """
    将测试通过的代理写入json文件
    """
    proxies_json = json.dumps(pass_proxy)

    with open('proxy_ip.json', 'a+') as f:
        f.write(proxies_json + '\n')
    print("已写入：%s" % pass_proxy)


if __name__ == '__main__':
    get_proxy(proxy_url)  # 获取代理
    # test_proxy_json()  # 测试成功的代理
