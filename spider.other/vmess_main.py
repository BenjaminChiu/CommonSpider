"""
@Desc   : 爬取翻墙链接
@Time   : 2021-05-10 10:55
@Author : tank boy
@File   : vmess_main.py
@coding : utf-8
"""
import os
import re
import sys

from lxml import etree

project_name = 'CommonSpider'
cur_path = os.path.abspath(__file__)
root_path = cur_path[:cur_path.find(project_name) + len(project_name)]
sys.path.append(root_path)

from util.my_request import MySession, MyRequest

vmess_web = "https://www.mattkaydiary.com/"

# 正则表达式匹配vmess，匹配可能出现的空格
pattern_vmess = re.compile(r'^(vmess://)\w')
pattern_ssr = re.compile(r'^(ss://|ssr://)\w')
pattern_trojan = re.compile(r'^(trojan://)\w')


def init():
    session = MySession()
    response = MyRequest(session, vmess_web).get()
    print("监测点1：链接成功")
    selector = etree.HTML(response.text)
    day = selector.xpath("//div[@class='post-outer']/div[@class='post']/article/font/h2/a/@href")  # day是一个list  div[@class='post-outer' and position()=1]

    data_vmess = []
    data_ssr = []
    data_trojan = []
    for i in range(len(day)):
        response_2 = MyRequest(session, day[i]).get()
        print("监测点2：链接成功")
        selector_2 = etree.HTML(response_2.text)
        # 获取到了整个div的所有text，用于后面筛选
        div_data = selector_2.xpath("//div[@style='-webkit-text-stroke-width: 0px;']/div//text()")

        for j in range(len(div_data)):
            div_data[j] = div_data[j].strip()  # 去除字符串首尾空格
            if pattern_vmess.match(div_data[j]):
                data_vmess.append(div_data[j])
            elif pattern_trojan.match(div_data[j]):
                data_trojan.append(div_data[j])
            elif pattern_ssr.match(div_data[j]):
                data_ssr.append(div_data[j])

        # 能拿到信息，即结束
        if len(data_vmess) or len(data_ssr) or len(data_trojan):
            print("今日链接为：%s" % day[i])
            print("当前链接的顺位是 %s" % i)
            break

    print("爬取到的vmess节点数量为：%s" % len(data_vmess))
    print("爬取到的ssr节点数量为：%s" % len(data_ssr))
    print("爬取到的trojan节点数量为：%s" % len(data_trojan))
    # 使用print写文件，不会有引号问题。三引号可以保留换行格式
    with open('C:/Users/Administrator/Desktop/vmess.json', 'w') as f:
        for i in range(len(data_vmess)):
            print(data_vmess[i], file=f)
        f.close()
    with open('C:/Users/Administrator/Desktop/trojan.json', 'w') as f:
        for i in range(len(data_trojan)):
            print(data_trojan[i], file=f)
        f.close()
    with open('C:/Users/Administrator/Desktop/ssr.json', 'w') as f:
        for i in range(len(data_ssr)):
            print(data_ssr[i], file=f)
        f.close()
    print("三种节点均写入完成！")


if __name__ == '__main__':
    init()
