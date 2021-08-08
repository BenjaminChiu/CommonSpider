"""
@Desc   : 项目的配置文件
@Time   : 2021-01-27 18:30
@Author : tank boy
@File   : cfg.py
@coding : utf-8
"""
# 请求网络线程总数, 线程不要调太多, 不然会返回很多 400
THREAD_SUM = 128

# timeout是用作设置响应时间的，响应时间分为连接时间和读取时间，timeout(3,7)表示的连接时间是3，响应时间是7
# 连接超时指的是在你的客户端实现到远端机器端口的连接时（对应的是 connect() ），Request 会等待的秒数。
# 一个很好的实践方法是把连接超时设为比 3 的倍数略大的一个数值，因为 TCP 数据包重传窗口 (TCP packet retransmission window) 的默认大小是 3。
TIMEOUT = (10, 16)

# 热更新代理池，存在于内存中。由MySession()启动
# 两种类型 使用字典 不使用列表，列表无法表达较为复杂的代理（id、hp...）
# {
#     'http': 'http://127.0.0.1:10809',
#     'https': 'http://127.0.0.1:10809'
# }
Proxy_Pool = [
    # {"type": "http", "host": "127.0.0.1", "port": "10809", "hp": 8888, "id": 8888},
    # {"type": "https", "host": "127.0.0.1", "port": "10809", "hp": 8888, "id": 7777}
]
