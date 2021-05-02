"""
@Desc   : 一个类 关于 代理，之所以使用类是为了以后的拓展性
@Time   : 2021-02-03 20:34
@Author : tank boy
@File   : proxy_model.py
@coding : utf-8
"""


class ProxyModel(object):
    def __init__(self, proxy_type, host, port):
        super().__init__()
        self.proxy_type = proxy_type
        self.host = host
        self.port = port
        self.hp = 10        # 每个代理默认生命值=10
