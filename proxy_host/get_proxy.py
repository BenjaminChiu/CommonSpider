"""
@Desc   : 获取代理，存放到ip代理池。1.从json文件中获取，2.从数据库中获取（暂时不用数据库，太重）
@Time   : 2021-01-28 19:10
@Author : tank boy
@File   : get_proxy.py
@coding : utf-8
"""

import json

from proxy_host.proxy_json import info_proxy_dict, verify_proxy


def clean_json():
    """
    清空json文件
    """
    with open('proxy.json', 'w') as f:
        f.seek(0)
        f.truncate()
        f.close()
    print("json已清空数据")


def write_proxy(pass_proxy):
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


# 为每个代理添加一个生命值，并初始化赋值如100，（磁盘 持久化）
# 没请求失败一次就-1，直至为0，从文件中删除（内存 内存中删除）
def get_proxy_from_list():
    """
    从.list文件中读取代理信息，获取ip，port ，type
    未用request请求.list文件的原因：需要翻墙才能下载。只能手动翻墙，手动下载
    """
    with open("C:/Users/Administrator/Desktop/proxy.list", "r") as f:
        data = f.read()
        proxies_list = data.split('\n')  # 拆分开返回的数据

        clean_json()  # 手动清空json文件

        # 总数-1的目的是，读文件的时候，总会多读1行
        for i in range(len(proxies_list) - 1):
            proxy_json = json.loads(proxies_list[i])  # print(str(i) + proxies_list[i])
            type, host, port = info_proxy_dict(proxy_json)  # 提取字典信息，重新赋值
            proxy = {'type': type, 'host': host, 'port': port}

            # 代理测试通过，就写入到json文件
            if verify_proxy(proxy):
                proxy['hp'] = 9  # 新增一个hp键，0开始计数
                proxy['id'] = i  # 新增一个id键，方便回溯修改
                write_proxy(proxy)

        f.close()  # 关闭文件


if __name__ == '__main__':
    get_proxy_from_list()  # 获取代理，存入json
