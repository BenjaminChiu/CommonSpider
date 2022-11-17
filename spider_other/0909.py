"""
@Desc   : 
@Time   : 2021-09-03 15:56
@Author : tank boy
@File   : vmess_json.py
@coding : utf-8
"""
from spider_other.vmess_mattkay import *


def read_txt(url):
    with open(url, 'r') as f:
        data_list = f.readlines()
        f.close()
    return data_list


def step_1():
    url = 'C:/A.Drive/Download/0901/0901.txt'
    ssr_list = read_txt(url)

    for i in ssr_list:
        print(i)

    p_list = [pattern_vmess, pattern_ssr, pattern_trojan]
    v_list = filter_v3(ssr_list, pattern=p_list)
    return v_list[0], v_list[1], v_list[2]


if __name__ == '__main__':
    v1, v2, v3 = step_1()
    print2json(v1, v2, v3, filename='total_v2.json')
