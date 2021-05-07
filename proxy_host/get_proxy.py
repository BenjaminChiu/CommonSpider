"""
@Desc   : 获取代理，存放到ip代理池。1.从json文件中获取，2.从数据库中获取
@Time   : 2021-01-28 19:10
@Author : tank boy
@File   : get_proxy.py
@coding : utf-8
"""

import json

import requests

import cfg


# 为每个代理添加一个生命值，并初始化赋值如100，（磁盘 持久化）
# 没请求失败一次就-1，直至为0，从文件中删除（内存 内存中删除）

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


def info_proxy_dict(proxy):
    """
    @param proxy:解析字典
    @return:返回三个值
    """
    type = proxy['type']
    host = proxy['host']
    port = proxy['port']
    return type, host, port


def verify_proxy(proxy):
    """
    :param proxy: type host port
    :@return pass with True,or False
    """
    type, host, port = info_proxy_dict(proxy)
    this_proxy = type + '://' + host + ':' + str(port)
    try:
        response = requests.get(url="http://icanhazip.com/", timeout=cfg.TIMEOUT, proxies={type: this_proxy})  # timeout越小，得到ip越少、质量越高
        proxy_ip = response.text.replace("\n", "")
        if proxy_ip == host:
            print("测试代理：" + this_proxy + '有效')
            return True
        else:
            print("测试代理：" + this_proxy + '无效')
            return False
    except Exception as e:
        print("测试代理：" + this_proxy + "出现未知错误")


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
        proxies_list = data.split('\n')  # 拆分开返回的数据

        clean_json()  # 手动清空json文件

        # 总数-1的目的是，读文件的时候，总会多读1行
        for i in range(len(proxies_list) - 1):
            proxy_json = json.loads(proxies_list[i])  # print(str(i) + proxies_list[i])
            type, host, port = info_proxy_dict(proxy_json)  # 解析字典，重新赋值
            proxy = {'type': type, 'host': host, 'port': port}

            # 代理测试通过，就写入到json文件
            if verify_proxy(proxy):
                proxy['hp'] = 10  # 新增一个hp键
                write_proxy(proxy)

        f.close()  # 关闭文件


if __name__ == '__main__':
    get_proxy('')  # 获取代理，存入json
