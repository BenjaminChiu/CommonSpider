"""
@Desc   : 爬取翻墙链接
@Time   : 2021-05-10 10:55
@Author : tank boy
@File   : vmess_main.py
@coding : utf-8
"""

from lxml import etree

import cfg
from model.request_model import MyRequest, MySession


def init():
    session = MySession()
    response = MyRequest(session, cfg.vmess_web).my_get()
    response.close()
    response.connection
    selector = etree.HTML(response.text)
    day = selector.xpath("//div[@class='post-outer' and position()=1]/div[@class='post']/article/font/h2/a/@href")  # day是一个list

    response_2 = MyRequest(session, day[0]).my_get()
    selector_2 = etree.HTML(response_2.text)
    data = selector_2.xpath("//div[@style='-webkit-text-stroke-width: 0px;']/div[4]/div/text()")  # 注意脚标是1开始，而非0

    # 使用print写文件，不会有引号问题。三引号可以保留换行格式
    with open('C:/Users/Administrator/Desktop/vmess.json', 'w') as f:
        for i in range(len(data)):
            print(data[i], file=f)
        f.close()


if __name__ == '__main__':
    init()
