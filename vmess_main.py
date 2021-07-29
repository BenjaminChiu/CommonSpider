"""
@Desc   : 爬取翻墙链接
@Time   : 2021-05-10 10:55
@Author : tank boy
@File   : vmess_main.py
@coding : utf-8
"""
import re

from lxml import etree

import cfg
from model.request_model import MyRequest, MySession

# 正则表达式匹配vmess，匹配可能出现的空格
pattern_vmess = re.compile(r'^(vmess://)\w')
pattern_ssr = re.compile(r'^(ss://|ssr://)\w')
pattern_trojan = re.compile(r'^(trojan://)\w')


def init():
    session = MySession()
    response = MyRequest(session, cfg.vmess_web).my_get()
    print("监测点1：链接成功")
    selector = etree.HTML(response.text)
    day = selector.xpath("//div[@class='post-outer']/div[@class='post']/article/font/h2/a/@href")  # day是一个list  div[@class='post-outer' and position()=1]

    data_vmess = []
    data_ssr = []
    data_trojan = []
    for i in range(len(day)):
        response_2 = MyRequest(session, day[i]).my_get()
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
    # s = 'trojan://1f3f9b92-7945-5efb-937a-90ce6040ac8b@tw-cn-hk-relay-1-97861a.dukou.info:5301?sni=tw-1-544.dukouplan3.dev#https%3a%2f%2fwww.mattkaydiary.com%7c%e4%b8%ad%e5%9b%bd%e9%a6%99%e6%b8%af%2f%e4%b8%ad%e5%9b%bd%e5%8f%b0%e6%b9%be%e4%b8%ad%e5%9b%bd(CN)China%2fGuangzhou%2f%e5%b0%8f%e4%b8%9c%e7%9a%84%e7%a8%8b%e5%ba%8f%e6%9c%aa%e8%83%bd%e7%b2%be%e5%87%86%e8%af%86%e5%88%ab(%e5%8f%af%e8%83%bd%e6%98%af%e4%b8%ad%e8%bd%ac%e8%8a%82%e7%82%b9)'
    # s1 = ' vmess://ew0KICAidiI6ICIyIiwNCiAgInBzIjogImh0dHBzOi8vd3d3Lm1hdHRrYXlkaWFyeS5jb2185Lit5Zu96aaZ5rivL+S4reWbveWPsOa5vihDTilDaGluYS9TaGVuemhlbi/lsI/kuJznmoTnqIvluo/mnKrog73nsr7lh4bor4bliKso5Y+v6IO95piv5Lit6L2s6IqC54K5KSIsDQogICJhZGQiOiAiaGsudGNwYmJyLm5ldCIsDQogICJwb3J0IjogIjgzODgiLA0KICAiaWQiOiAiNjRlMmYyNjQtNWQzZi0xMWViLWE4YmYtZjIzYzkxY2ZiYmM5IiwNCiAgImFpZCI6ICIyIiwNCiAgInNjeSI6ICJhdXRvIiwNCiAgIm5ldCI6ICJ0Y3AiLA0KICAidHlwZSI6ICJub25lIiwNCiAgImhvc3QiOiAiIiwNCiAgInBhdGgiOiAiIiwNCiAgInRscyI6ICJ0bHMiLA0KICAic25pIjogIiINCn0='
    # # result = pattern_trojan.match(s)
    #
    # result1 = pattern_vmess.match(s1.strip())
    # print('%s' % result1.string)
