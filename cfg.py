"""
@Desc   : 项目的配置文件
@Time   : 2021-01-27 18:30
@Author : tank boy
@File   : cfg.py
@coding : utf-8
"""
import os

# 配置被爬取网站域名
WEBSITE = "http://www.dy1234.net/"

# 请求网络线程总数, 线程不要调太多, 不然会返回很多 400
THREAD_SUM = 128

# 统一设置 中断时间
TIMEOUT = 6

RootPath = os.path.abspath(os.path.dirname(__file__))
# RootPath = curPath[:curPath.find("CommonSpider\\") + len("CommonSpider\\")]  # 获取myProject，也就是项目的根路径


# 代理池，两种类型 使用字典 不使用列表，列表无法表达较为复杂的代理
Proxy_Pool = []
Proxy_Pool_http = []
Proxy_Pool_https = []
