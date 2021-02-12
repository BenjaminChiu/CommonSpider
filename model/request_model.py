#!/usr/bin/env python
# coding=utf-8
import random

import requests

import cfg
import proxy_host.get_proxy as my_proxy


class RequestModel(object):
    UserAgent_List = [
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36 Edg/88.0.705.56",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.67 Safari/537.36",
        "Mozilla/5.0 (X11; OpenBSD i386) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1944.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2309.372 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.2117.157 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/4E423F",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
        "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
        "Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0",
        "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
        "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
        "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
        "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00"
    ]

    def __init__(self):
        pass

    # 获取不同的请求头
    def get_headers(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache - Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'www.dy1234.net',
            'DNT': '1',
            'Pragma': 'no-cache',
            # 'Referer': 'http: //www.dytt8.net/html/gndy/dyzz/index.html',
            'Cookie': 'UM_distinctid=174c60df6f4807-070d6885205e05-7e647b65-1fa400-174c60df6f5955; CNZZDATA1276470129=299915948-1601046745-%7C1606627666; '
                      'Hm_lvt_b12979e4e40bb5a6bba9824601810548=1606542703,1606561256,1606625698,1606631576; ASPSESSIONIDSQAARADT=MHHHEIMDLCDMDBPCELHDFMGC',
            'User-Agent': random.choice(self.UserAgent_List),
        }
        return headers

    def get_proxies(self, flag):
        """
        验证、获取代理
        @param flag:根据flag来判断是否使用代理。flag为false时，直接返回一个空的字典
        @return:字典，内容为代理
        """
        proxies = {}
        if flag:
            pre_data = random.choice(cfg.Proxy_Pool_http)  # 随机筛选一个
            host, port, hp = pre_data.host, pre_data.port, pre_data.hp
            # 当前代理通过的话
            if my_proxy.test_proxy(host, port, 'http'):
                proxies = {
                    'http': str(pre_data.host) + ':' + str(pre_data.port)
                    # 'http':'web-proxy.oa.com:8080',
                    # 'https': random.choice(cls.Proxy_Pool)
                }
                print('使用代理:' + str(pre_data.host) + ':' + str(pre_data.port) + ':hp=' + str(pre_data.hp))
            # 当前代理验证失败，减生命值
            else:
                if pre_data.hp != 0:
                    pre_data.hp = pre_data.hp - 1  # -1只是针对当前这个变量
                    print('失效代理:' + str(pre_data.host) + ':' + str(pre_data.port) + ':hp=' + str(pre_data.hp))
                    self.get_proxies(flag)  # 简单的递归，直至选出有效的代理。但当代理全部无效的时候，将陷入死循环
                # 该项生命值为0
                else:
                    print('正在移除代理:' + str(pre_data.host) + ':' + str(pre_data.port) + ':hp=' + str(pre_data.hp))
                    cfg.Proxy_Pool_http.remove(pre_data)
        return proxies

    # 返回一个request连接
    def new_request(self, url):
        requests.adapters.DEFAULT_RETRIES = 20  # 增加重连次数
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        return s.get(url, headers=self.get_headers(), proxies=self.get_proxies(True), timeout=cfg.TIMEOUT + 1500)


if __name__ == '__main__':
    temp = RequestModel()
    temp.get_proxies(True)
    # response = temp.new_request(cfg.WEBSITE + 'w.asp?p=1&f=3&l=t')
    # print(response)
