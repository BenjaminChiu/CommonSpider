"""
@Desc   : 获取代理，存放到ip代理池。1.从json文件中获取，2.从数据库中获取（暂时不用数据库，太重）
@Time   : 2021-01-28 19:10
@Author : tank boy
@File   : io_proxy.py
@coding : utf-8

整个代理模块的工作流程如下：

手动下载.list文件到桌面，info_proxy_from_list()读入，将代理处理成可供request使用的shape
使用多线程对代理进行测试，对测试通过的代理，将其写入同目录的proxy.json


拿数据
request.get_proxy()  从全局变量cfg.Proxy_Pool 获取

"""

from my_proxy.util_proxy import *
from util import cfg

proxy_url = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'


# ============================Proxy==Out======Start=================================
# 热更新输出，直接在my_request中 random.choice(cfg.Proxy_Pool)


# 冷备份 到 热更新，只需启动一次
def cold_proxy_out():
    data_list = read_json_my('C:/A.Drive/Develop/WorkSpace/PC.Spider.Web/CommonSpider/my_proxy/proxy.json')
    for line in data_list:
        cfg.Proxy_Pool.append(line)


# ============================Proxy==Out======Start=================================


# ============================Proxy==In======Start=================================
# 为每个代理添加一个生命值，并初始化赋值如100，（磁盘 持久化）
# 没请求失败一次就-1，直至为0，从文件中删除（内存 内存中删除）
def info_proxy_from_list():
    """
    从.list文件中读取代理信息，获取ip，port ，type
    未用request请求.list文件的原因：需要翻墙才能下载。只能手动翻墙，手动下载
    """
    proxy_list = read_json_my("C:/Users/Administrator/Desktop/proxy.list")
    proxy_list_pass = []
    for line in proxy_list:
        type, host, port = info_proxy_dict(line)  # 提取字典信息，重新赋值
        proxy = {type: host + ':' + str(port)}  # 封装为一个request形式的proxy
        proxy_list.append(proxy)
    return proxy_list_pass


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


def v1_in_proxy():
    # session = MySession()
    # response = MyRequest(session, proxy_url, proxy_flag=True, allow_redirects=True).get()
    # proxy_list = response.text.split('\n')
    # proxy_list.pop()

    proxy_list = []

    with open("C:/Users/Administrator/Desktop/proxy.list", 'r') as f:
        content = f.readlines()
        for line in content:
            line_data = json.loads(line)
            proxy_list.append(line_data)
        f.close()

    # input('获取代理完毕！关闭翻墙软件！')

    for proxy in proxy_list:
        # proxy = json.loads(i)
        type = proxy['type']
        host = proxy['host']
        port = proxy['port']
        proxy_dict = {type: host + ':' + str(port)}
        # type + '://' +
        verify_proxy(proxy_dict)

        # write_proxy_json(proxy_dict)


if __name__ == '__main__':
    v1_in_proxy()
