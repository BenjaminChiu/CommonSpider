"""
@Desc   : 项目的配置文件
@Time   : 2021-01-27 18:30
@Author : tank boy
@File   : cfg.py
@coding : utf-8
"""
import os

# 配置被爬取网站域名
WEBSITE = 'http://www.dy1234.net/'

# 请求网络线程总数, 线程不要调太多, 不然会返回很多 400
THREAD_SUM = 128

# 统一设置 中断时间
TIMEOUT = 8000

RootPath = os.path.abspath(os.path.dirname(__file__))
# RootPath = curPath[:curPath.find("Spider_MovieHome\\") + len("Spider_MovieHome\\")]  # 获取myProject，也就是项目的根路径
