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

proxy_url = 'https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list'
vmess_web = "https://www.mattkaydiary.com/"

# 正则表达式匹配vmess，匹配可能出现的空格
pattern_vmess = re.compile(r'^(vmess://)\w')
pattern_ssr = re.compile(r'^(ss://|ssr://)\w')
pattern_trojan = re.compile(r'^(trojan://)\w')

pattern_google_drive = re.compile(r'^(https://drive.google.com/)\w')
pattern_pCloud = re.compile(r'^(https://u.pcloud.link/)\w')
pattern_youtube = re.compile(r'^(https://www.youtube.com/)\w')


def step_1(session):
    day = []
    response = MyRequest(session, vmess_web, proxy_flag=True).get()
    if response.status_code == 200:
        print("监测点1：链接成功")
        selector = etree.HTML(response.text)
        day = selector.xpath("//div[@class='post-outer']/div[@class='post']/article/font/h2/a/@href")  # day是一个list  div[@class='post-outer' and position()=1]
    return day


# def filter_v1(data_list):
#     data_vmess, data_ssr, data_trojan = [], [], []
#     for j in range(len(data_list)):
#         data_list[j] = data_list[j].strip()  # 去除字符串首尾空格
#
#         if pattern_vmess.match(data_list[j]):
#             data_vmess.append(data_list[j])
#         elif pattern_trojan.match(data_list[j]):
#             data_trojan.append(data_list[j])
#         elif pattern_ssr.match(data_list[j]):
#             data_ssr.append(data_list[j])
#
#
# def filter_v2(data_list):
#     google_drive_v, pcloud_v, youtube_v = '', '', ''
#     for j in range(len(data_list)):
#         data_list[j] = data_list[j].strip()  # 去除字符串首尾空格
#
#         if pattern_google_drive.match(data_list[j]):
#             google_drive_v = data_list[j]
#         elif pattern_pCloud.match(data_list[j]):
#             pcloud_v = data_list[j]
#         elif pattern_youtube.match(data_list[j]):
#             youtube_v = data_list[j]


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


def step_2(session, day, version):
    v_list = []
    for i in range(len(day)):
        response = MyRequest(session, day[i], proxy_flag=True).get()
        if response.status_code == 200:
            print("监测点2：链接成功。当前链接为=%s" % day[i])
            selector = etree.HTML(response.text)
            # 获取到了整个div的所有text，用于后面筛选
            div_data = selector.xpath("//div[@style='-webkit-text-stroke-width: 0px;']/div//text()")

            p_list = []
            if version == 1:
                p_list = [pattern_vmess, pattern_ssr, pattern_trojan]
            elif version == 2:
                p_list = [pattern_google_drive, pattern_pCloud, pattern_youtube]
            v_list = filter_v3(div_data, pattern=p_list)

            # 能拿到信息，即结束
            if len(v_list[0]) or len(v_list[1]) or len(v_list[2]):
                print("今日链接为：%s" % day[i])
                print("当前链接的顺位是 %s" % i)
                break
    if version == 1:
        return v_list[0], v_list[1], v_list[2]
    elif version == 2:
        print("google_drive:%s" % v_list[0][0])
        print("pcloud:%s" % v_list[1][0])
        print("youtube:%s" % v_list[2][0])
        return v_list[0][0]


def down_file(session, v_1):
    response = MyRequest(session, v_1, proxy_flag=True, allow_redirects=True).get()
    # 获取文件名
    dict_head = dict(response.headers)
    info = dict_head['Content-Disposition']
    file_name = info.split('filename=\"')[1].split('\";filename*=')[0]

    with open('C:/A.Drive/Download/' + file_name, 'wb') as file:
        file.write(response.content)
        file.close()
    print('success! The code is %s' % response.status_code)


def print2json(data_vmess, data_ssr, data_trojan, filename='total.json'):
    print("爬取到的vmess节点数量为：%s" % len(data_vmess))
    print("爬取到的ssr节点数量为：%s" % len(data_ssr))
    print("爬取到的trojan节点数量为：%s" % len(data_trojan))
    # 使用print写文件，不会有引号问题。三引号可以保留换行格式
    with open('C:/Users/Administrator/Desktop/' + filename, 'w') as f:
        for i in range(len(data_ssr)):
            print(data_ssr[i], file=f)
        print('\n\n\n', file=f)
        for i in range(len(data_vmess)):
            print(data_vmess[i], file=f)
        print('\n\n\n', file=f)
        for i in range(len(data_trojan)):
            print(data_trojan[i], file=f)
        f.close()
    print("三种节点均写入完成！")


if __name__ == '__main__':
    session = MySession()
    days = step_1(session)

    v1, v2, v3 = step_2(session, days, 1)
    print2json(v1, v2, v3)

    # google_drive = step_2(session, days, 2)
    # down_file(session, google_drive)
