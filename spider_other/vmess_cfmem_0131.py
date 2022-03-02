"""
@Desc   : 爬取翻墙链接
@Time   : 2021-05-10 10:55
@Author : tank boy
@File   : vmess_mattkay.py
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

proxy_url = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
vmess_web = "https://www.cfmem.com/"

# 正则表达式匹配vmess，匹配可能出现的空格
pattern_ssr = re.compile(r'^(ss:/|ss://|ssr://)\w')
pattern_vmess = re.compile(r'^(vmess://)\w')
pattern_trojan = re.compile(r'^(trojan://)\w')

pattern_google_drive = re.compile(r'^(https://drive.google.com/)\w')
pattern_pCloud = re.compile(r'^(https://u.pcloud.link/)\w')
pattern_youtube = re.compile(r'^(https://www.youtube.com/)\w')


def step_1(session):
    day = []
    response = MyRequest(session, vmess_web, proxy_flag=False).get()
    if response.status_code == 200:
        print("监测点1：链接成功")
        selector = etree.HTML(response.text)
        day = selector.xpath("//div[@class='blog-posts index-post-wrap flex-col']/article/div[@class='entry-header']/h2/a/@href")
        # day是一个list  div[@class='post-outer' and position()=1]
        # print("Test: %s" % day)
    return day



def filter_v3(data_list, **kwargs):
    """
    通用正则表达式 提取流程
    @param data_list:
    @param kwargs:
    @return: 一个二维数组
    def step_1(session):
    day = []
    response = MyRequest(session, vmess_web, proxy_flag=True).get()
    if response.status_code == 200:
        print("监测点1：链接成功")
        selector = etree.HTML(response.text)
        day = selector.xpath("//div[@class='post-outer']/div[@class='post']/article/font/h2/a/@href")  # day是一个list  div[@class='post-outer' and position()=1]
    return day
    """
    p_list = kwargs['pattern']
    num_p_list = len(p_list)
    v_list = [list() for i in range(num_p_list)]

    for i in range(len(data_list)):
        data_list[i] = data_list[i].strip()  # 去除字符串首尾空格
        for j in range(num_p_list):
            if p_list[j].match(data_list[i]):
                data_list[i] = data_list[i].replace('https%3a%2f%2fwww.mattkaydiary.com%7c', '').replace('mattkaydiary.com%7c', '')
                v_list[j].append(data_list[i])
    return v_list


def step_2(session, day):
    server_data_list = []

    for i in range(len(day)):
        response = MyRequest(session, day[i], proxy_flag=False).get()
        if response.status_code == 200:
            print("监测点2：链接成功。当前链接为=%s" % day[i])
            selector = etree.HTML(response.text)
            # 注意使用'//text()' 和 '/text()'。   //text获取到了整个div的所有text，用于后面筛选。
            span_data = selector.xpath("//pre[@cid='n0']/span//text()")

            # print("step_2: %s" % span_data)

            server_data = ''  # 该变量用于合成一个节点数据

            for i in span_data:
                if pattern_vmess.match(i) or pattern_ssr.match(i) or 'ss:/' == i:
                    server_data_list.append(server_data)
                    server_data = ''

                server_data = server_data + i

            if len(server_data_list):
                # print("今日链接为：%s" % day[i])
                print("当前链接的顺位是 %s" % i)
                break

    server_data_list.pop(0)
    return server_data_list


def print2json(server_data_list, filename='total.json'):
    print("爬取到的节点数量为：%s" % len(server_data_list))
    # 使用print写文件，不会有引号问题。三引号可以保留换行格式
    with open('C:/Users/Administrator/Desktop/' + filename, 'w') as f:
        for i in range(len(server_data_list)):
            print(server_data_list[i], file=f)
        f.close()
    print("节点写入完成！")


if __name__ == '__main__':
    session = MySession()
    days = step_1(session)

    server_data_list = step_2(session, days)
    print2json(server_data_list)
